# -*- coding: utf-8 -*-
"""
Suíte Formal de Testes Unitários Científicos, Backend PyTorch & Contratos · GrafoParada
Execução: uv run pytest code/grafoparada_tec/test_unitarios_cientificos.py -v
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest
import torch
import yaml

TEC_DIR = Path(__file__).resolve().parent
ROOT_DIR = TEC_DIR.parent.parent
sys.path.insert(0, str(TEC_DIR))

from modelo_predicao_e_abandono import (  # noqa: E402
    LIMIAR_OCUPACAO_LINHA_OCIOSA_PCT,
    LIMIAR_RENEGING_DESPACHO_EMERGENCIA,
    LIMIAR_TRAVA_HIBRIDA_MINUTOS,
    PENALIDADE_DENIED_BOARDING_YAP_CATS,
    RENEGING_TAU_MINUTOS_PADRAO,
    avaliar_gatilho_despacho_emergencial,
    avaliar_trava_hibrida_defensiva,
    calcular_probabilidade_reneging,
    calcular_tempo_percebido,
)
from stgcn_official import STGCN, compute_normalized_laplacian  # noqa: E402
from servidor_tempo_real_pe60 import haversine_m  # noqa: E402
import db_manager  # noqa: E402


# ---------------------------------------------------------------------------
# 1. TESTES UNITÁRIOS: PerceivedWaitModel (Yap & Cats, 2021)
# ---------------------------------------------------------------------------

class TestPerceivedWaitModel:
    def test_condicao_normal_mantem_tempo_cronologico(self):
        assert calcular_tempo_percebido(10.0) == 10.0
        assert calcular_tempo_percebido(0.0) == 0.0
        assert calcular_tempo_percebido(12.345) == 12.35

    def test_penalidade_denied_boarding_1_68x(self):
        esperado = round(10.0 * PENALIDADE_DENIED_BOARDING_YAP_CATS, 2)
        assert PENALIDADE_DENIED_BOARDING_YAP_CATS == pytest.approx(1.68)
        assert calcular_tempo_percebido(10.0, denied_boarding=True) == esperado
        assert calcular_tempo_percebido(15.0, crowd_critical=True) == 25.2

    def test_ambas_flags_nao_aplicam_penalidade_duplicada(self):
        unico = calcular_tempo_percebido(10.0, denied_boarding=True)
        ambos = calcular_tempo_percebido(10.0, denied_boarding=True, crowd_critical=True)
        assert ambos == unico == 16.8

    @pytest.mark.parametrize("valor_invalido", [-0.01, -1.0, -50.0])
    def test_tempo_negativo_dispara_value_error(self, valor_invalido: float):
        with pytest.raises(ValueError):
            calcular_tempo_percebido(valor_invalido)


# ---------------------------------------------------------------------------
# 2. TESTES UNITÁRIOS: PassengerRenegingModel (Kim et al., 2026)
# ---------------------------------------------------------------------------

class TestPassengerRenegingModel:
    def test_ponto_mediano_tau_exato_50_pct(self):
        prob = calcular_probabilidade_reneging(RENEGING_TAU_MINUTOS_PADRAO)
        assert prob == pytest.approx(0.5, abs=1e-4)

    def test_monotonicidade_estrita_no_tempo(self):
        tempos = [0, 2, 5, 10, 15, 20, 30, 45, 60]
        probs = [calcular_probabilidade_reneging(t) for t in tempos]
        assert all(probs[i] <= probs[i + 1] for i in range(len(probs) - 1))
        assert probs[0] < 0.05
        assert probs[-1] > 0.99

    def test_estabilidade_numerica_extremos_sem_overflow(self):
        # expoente < -60 -> satura em 1.0; expoente > 60 -> satura em 0.0
        assert calcular_probabilidade_reneging(1e6) == 1.0
        assert calcular_probabilidade_reneging(0.0, tau=1000.0) == 0.0
        p = calcular_probabilidade_reneging(500.0)
        assert 0.0 <= p <= 1.0

    def test_composicao_com_penalidade_yap_cats(self):
        p_normal = calcular_probabilidade_reneging(15.0, usar_tempo_percebido=False)
        p_percebido = calcular_probabilidade_reneging(
            15.0, usar_tempo_percebido=True, denied_boarding=True
        )
        assert p_normal == pytest.approx(0.5, abs=1e-4)
        assert p_percebido > 0.90

    def test_tempo_negativo_rejeitado(self):
        with pytest.raises(ValueError):
            calcular_probabilidade_reneging(-5.0)


# ---------------------------------------------------------------------------
# 3. TESTES UNITÁRIOS: Trava Híbrida Defensiva Anti-Oversmoothing
# ---------------------------------------------------------------------------

class TestTravaHibridaDefensiva:
    def test_fronteira_exata_15_min_nao_aciona_trava(self):
        res = avaliar_trava_hibrida_defensiva(tempo_gps_min=25.0, tempo_stgcn_min=10.0)
        assert res["trava_acionada"] is False
        assert res["discrepancy_delta"] == 15.0
        assert res["status"] == "NOMINAL_STGCN"
        assert res["tempo_exibido_min"] == 10.0

    def test_discrepancia_acima_de_15_min_forca_gps(self):
        res = avaliar_trava_hibrida_defensiva(tempo_gps_min=45.0, tempo_stgcn_min=29.99)
        assert res["trava_acionada"] is True
        assert res["status"] == "ALERTA_AMARELO_OVER_SMOOTHING"
        assert res["tempo_exibido_min"] == 45.0

    def test_simetria_delta_negativo_e_positivo(self):
        r1 = avaliar_trava_hibrida_defensiva(tempo_gps_min=40.0, tempo_stgcn_min=15.0)
        r2 = avaliar_trava_hibrida_defensiva(tempo_gps_min=15.0, tempo_stgcn_min=40.0)
        assert r1["trava_acionada"] is True
        assert r2["trava_acionada"] is True
        assert r1["discrepancy_delta"] == r2["discrepancy_delta"] == 25.0
        assert r1["tempo_exibido_min"] == 40.0
        assert r2["tempo_exibido_min"] == 15.0

    def test_threshold_customizado(self):
        res = avaliar_trava_hibrida_defensiva(tempo_gps_min=20.0, tempo_stgcn_min=12.0, threshold_min=5.0)
        assert LIMIAR_TRAVA_HIBRIDA_MINUTOS == 15.0
        assert res["trava_acionada"] is True
        assert res["tempo_exibido_min"] == 20.0


# ---------------------------------------------------------------------------
# 4. TESTES UNITÁRIOS: Despacho Emergencial CTM (Mitigação Deadheading)
# ---------------------------------------------------------------------------

class TestDespachoEmergencialCTM:
    def test_aprova_quando_ambos_limiares_atendidos(self):
        res = avaliar_gatilho_despacho_emergencial(
            tempo_espera_min=16.0,
            ocupacao_concorrente_pct=LIMIAR_OCUPACAO_LINHA_OCIOSA_PCT,
            denied_boarding=True,
        )
        assert res["probabilidade_reneging"] >= LIMIAR_RENEGING_DESPACHO_EMERGENCIA
        assert res["despacho_autorizado"] is True

    def test_bloqueia_quando_linha_concorrente_nao_esta_ociosa(self):
        res = avaliar_gatilho_despacho_emergencial(
            tempo_espera_min=20.0,
            ocupacao_concorrente_pct=15.01,
            denied_boarding=True,
        )
        assert res["despacho_autorizado"] is False

    def test_bloqueia_quando_risco_reneging_abaixo_limiar(self):
        res = avaliar_gatilho_despacho_emergencial(
            tempo_espera_min=10.0,
            ocupacao_concorrente_pct=5.0,
            denied_boarding=False,
        )
        assert res["probabilidade_reneging"] < LIMIAR_RENEGING_DESPACHO_EMERGENCIA
        assert res["despacho_autorizado"] is False


# ---------------------------------------------------------------------------
# 5. TESTES UNITÁRIOS: Arquitetura PyTorch STGCN & Geodesia RMR
# ---------------------------------------------------------------------------

class TestSTGCNAndGeodesy:
    def test_laplaciana_normalizada_simetria_e_espectro(self):
        adj = np.array([
            [0.0, 1.0, 0.0, 0.0],
            [1.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0, 1.0],
            [0.0, 0.0, 1.0, 0.0],
        ])
        lap = compute_normalized_laplacian(adj).numpy()
        assert lap.shape == (4, 4)
        assert np.allclose(lap, lap.T, atol=1e-6)
        eigvals = np.linalg.eigvalsh(lap)
        assert eigvals.min() >= -1.0 - 1e-5
        assert eigvals.max() <= 1.0 + 1e-5

    def test_stgcn_forward_e_backward_20_nos_pe60(self):
        torch.manual_seed(42)
        num_nodes = 20
        adj = np.eye(num_nodes)
        for i in range(num_nodes - 1):
            adj[i, i + 1] = 1.0
            adj[i + 1, i] = 1.0
        lap = compute_normalized_laplacian(adj)

        model = STGCN(num_nodes=num_nodes, in_channels=1, out_horizon=3)
        x = torch.randn(2, 1, 12, num_nodes, requires_grad=True)
        out = model(x, lap)

        assert out.shape == (2, 3, num_nodes)
        assert torch.isfinite(out).all()
        out.sum().backward()
        assert x.grad is not None and torch.isfinite(x.grad).all()

    def test_haversine_simetria_identidade_e_recife_camela(self):
        rec = (-8.0631, -34.8711)
        cam = (-8.5149, -35.1235)
        assert haversine_m(*rec, *rec) == pytest.approx(0.0, abs=1e-6)
        d1 = haversine_m(*rec, *cam)
        d2 = haversine_m(*cam, *rec)
        assert d1 == pytest.approx(d2, rel=1e-9)
        assert 55_000.0 <= d1 <= 62_000.0  # ~57.4 km em linha reta


# ---------------------------------------------------------------------------
# 6. TESTE DE CONTRATO: OpenAPI v2.2.0 (/contracts/api-contract.yaml)
# ---------------------------------------------------------------------------

class TestContractsOpenAPI:
    def test_openapi_v2_2_schemas_e_rotas_obrigatorias(self):
        contract_path = ROOT_DIR / "contracts" / "api-contract.yaml"
        assert contract_path.is_file()
        spec = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
        assert spec["openapi"].startswith("3.0")
        assert spec["info"]["version"] == "2.2.0"
        expected_paths = {
            "/api/v1/network/gtfs",
            "/api/v1/telemetry/line/{route_code}",
            "/api/v1/predict/corridor",
            "/api/v1/dispatch/emergency",
            "/api/register",
            "/api/routine",
            "/api/telemetry",
        }
        assert expected_paths.issubset(set(spec["paths"].keys()))
        schemas = spec.get("components", {}).get("schemas", {})
        for req_schema in [
            "Route",
            "LineTelemetry",
            "PredictedStopInfo",
            "EmergencyDispatchPayload",
            "UserRegistrationRequest",
            "UserProfileResponse",
            "RoutinePersistRequest",
            "RoutinePersistResponse",
            "DemandObservationRequest",
            "DatabaseStatusAndTrainingResponse",
        ]:
            assert req_schema in schemas


# ---------------------------------------------------------------------------
# 7. TESTES UNITÁRIOS: Persistência SQLite (db_manager.py)
# ---------------------------------------------------------------------------

class TestDatabaseManagerSQLite:
    def test_init_db_cria_quatro_tabelas_idempotente(self, tmp_path: Path):
        db_file = tmp_path / "nested" / "grafoparada_test.db"
        resolved = db_manager.init_db(db_file)
        assert resolved == db_file
        assert db_file.is_file()
        # Segunda chamada deve ser 100% idempotente
        db_manager.init_db(db_file)

        summary = db_manager.get_db_summary(db_file)
        assert summary["counts"] == {
            "users": 0,
            "routines": 0,
            "demand_observations": 0,
            "training_runs": 0,
        }

    def test_register_user_cadastro_e_upsert_lgpd(self, tmp_path: Path):
        db_file = tmp_path / "grafoparada_users.db"
        created = db_manager.register_user(
            name="Cauã Lira",
            contact_hint="whatsapp ****-1234",
            user_id="usr_teste_01",
            db_path=db_file,
        )
        assert created["id"] == "usr_teste_01"
        assert created["name"] == "Cauã Lira"
        assert created["contact_hint"] == "whatsapp ****-1234"

        updated = db_manager.register_user(
            name="Cauã Lira UFRPE",
            contact_hint="email c***@ufrpe.br",
            user_id="usr_teste_01",
            db_path=db_file,
        )
        assert updated["id"] == "usr_teste_01"
        assert updated["name"] == "Cauã Lira UFRPE"
        assert db_manager.get_db_summary(db_file)["counts"]["users"] == 1

        with pytest.raises(ValueError):
            db_manager.register_user(name="   ", db_path=db_file)

    def test_save_routine_record_observation_e_log_training_run(self, tmp_path: Path):
        db_file = tmp_path / "grafoparada_full.db"
        user = db_manager.register_user("Maria Silva", db_path=db_file)

        routine = db_manager.save_routine(
            {
                "user_id": user["id"],
                "origin_city": "Ipojuca",
                "origin_neighborhood": "Camela",
                "origin_stop_id": "030613",
                "origin_stop_name": "Praça Pedro Serafim (Terminal de Camela)",
                "origin_lat": -8.514888,
                "origin_lon": -35.123539,
                "dest_city": "Cabo de Santo Agostinho",
                "dest_neighborhood": "Centro",
                "dest_stop_id": "030001",
                "dest_stop_name": "Terminal Integrado do Cabo",
                "dest_lat": -8.2869,
                "dest_lon": -35.0355,
                "departure_time": "06:30",
                "return_time": "17:45",
                "preferred_line": "199",
                "frequency": "DUT",
            },
            db_path=db_file,
        )
        assert routine["id"].startswith("rtn_")
        assert routine["preferred_line"] == "199"

        obs = db_manager.record_observation(
            {
                "user_id": user["id"],
                "stop_id": "030613",
                "route_code": "199",
                "direction": "IDA",
                "observed_wait_min": 14.5,
                "predicted_wait_min": 12.0,
                "occupancy_est": 3,
                "source": "Horário Programado · GTFS",
            },
            db_path=db_file,
        )
        assert obs["id"] == 1
        assert obs["source"] == "Horário Programado · GTFS"

        run = db_manager.log_training_run(
            {
                "dataset_rows": 1200,
                "real_observations": 1,
                "lines_covered": 393,
                "stgcn_mae": 2.41,
                "ols_mae": 4.88,
                "persistence_mae": 5.35,
                "weights_hash": "sha256:abc123",
                "notes": "Ciclo inicial validado com dados reais locais",
            },
            db_path=db_file,
        )
        assert run["id"] == 1
        assert run["stgcn_mae"] == pytest.approx(2.41)

        dataset = db_manager.get_training_dataset(db_file)
        assert dataset["total_observations"] == 1
        assert dataset["total_routines"] == 1
        assert "199" in dataset["lines_covered"]
        assert dataset["latest_training_run"]["weights_hash"] == "sha256:abc123"

        summary = db_manager.get_db_summary(db_file)
        assert summary["counts"] == {
            "users": 1,
            "routines": 1,
            "demand_observations": 1,
            "training_runs": 1,
        }

        with pytest.raises(ValueError):
            db_manager.record_observation(
                {"route_code": "199", "source": "passenger_checkin", "observed_wait_min": -2.0},
                db_path=db_file,
            )
