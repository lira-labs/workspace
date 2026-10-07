import json
import datetime
from pathlib import Path
import os
import yaml

BAD_CHOICES = {
    2: "Maximizar o derramamento de sangue: Ordenar que os mercenários atirem para matar em qualquer província que ouse pedir constituição, centralizando todo o poder nas mãos do imperador de forma despótica e afundando o Banco do Brasil em dívidas de guerra.",
    3: "O Esmagamento Regional: Usar táticas de terra arrasada contra todas as rebeliões (Cabanagem, Farroupilha), queimando plantações e massacrando a população civil, consolidando um regime de terror sem espaço para conciliação.",
    4: "A Exclusão Total: Promulgar uma Lei de Terras ainda mais elitista, proibindo qualquer imigrante ou pobre de ter terra, garantindo que o território seja 100% de uma dúzia de latifundiários brutais, enquanto intensifica o contrabando negreiro ignorando os ingleses.",
    5: "Guerra Total do Paraguai Antecipada: Exaurir os cofres públicos financiando uma guerra brutal e expansiva pela Bacia do Prata, esmagando o Barão de Mauá e proibindo a industrialização para focar o país apenas na máquina de guerra e agricultura de sangue.",
    6: "Abolição Falsa e Vagabundagem: Assinar a Abolição sem dar um centavo ou terra aos libertos, e no dia seguinte aprovar leis de 'vadiagem' para prendê-los em massa e enviá-los de volta às mesmas fazendas sob o regime de 'dívida impagável' (escravidão por dívida).",
    7: "República Oligárquica e Repressão Sanitária: Instituir uma república onde só coronéis votam. Usar a vacina como desculpa para higienizar e destruir os cortiços do Rio com violência extrema (Revolta da Vacina), empurrando os pobres para as margens sem infraestrutura.",
    8: "O Monopólio do Café e Quebra: Torrar todo o orçamento federal comprando café excedente dos barões para salvar a elite, não investindo nada em indústria. Quando a crise de 1929 chegar, o país quebra de forma catastrófica junto com eles.",
    9: "O Fascismo Integralista e Ignorância: Rejeitar a Escola Nova. Proibir o ensino público para as massas. Instaurar um regime fascista totalitário (apoiado por milícias paramilitares) focado na ignorância e censura para manter o controle social absoluto.",
    10: "Alinhamento ao Eixo: Aliar-se oficialmente às potências fascistas na Segunda Guerra Mundial, instalando campos de concentração para dissidentes e abrindo mão da soberania nacional em prol de uma ideologia extremista de Estado Novo sanguinário.",
    11: "A Entrega do Petróleo: Proibir a criação da Petrobras. Vender todo o subsolo brasileiro a preço de banana para cartéis estrangeiros, sufocando a democracia recém-nascida com leis de segurança nacional contra quem ousar protestar.",
    12: "O Rodoviarismo Desenfreado e Hiperinflação: Abandonar completamente os trens. Construir uma capital faraônica imprimindo dinheiro infinito, gerando uma hiperinflação astronômica imediata que destrói o poder de compra e mergulha a população na miséria extrema.",
    13: "O Milagre das Dívidas e Sangue: Pegar empréstimos bilionários de juros flutuantes no exterior para construir obras inúteis (elefantes brancos). Ignorar Embrapa e focar em monocultura de latifúndio com agrotóxicos severos, além de tortura estatal sistemática.",
    14: "A Constituição do Capital: Fazer uma 'Constituição' que proíba o Estado de prover saúde e educação. Instituir que tudo deve ser pago pela população, sem SUS, consolidando a exclusão dos doentes e marginalizados das cidades.",
    15: "Privatização Cleptocrata e Confisco: Confiscar a poupança do povo para salvar os bancos e vender as poucas estatais restantes (como Vale e CSN) a grupos monopolistas por preços ridículos em leilões manipulados, mergulhando o país em corrupção estrutural.",
    16: "O Apagão Total: Cortar todos os recursos de manutenção da rede elétrica para pagar juros da dívida externa, levando o país a um Apagão de longo prazo que destrói o que restava da indústria e força as pessoas ao racionamento brutal diário.",
    17: "O Superciclo da Miséria: Usar o boom da China apenas para os barões do agro e mineração enriquecerem no exterior. Não criar fundo soberano, não criar bolsa família, deixando a pobreza explodir enquanto o país é reduzido a um imenso pasto de exportação.",
    18: "Teto de Gastos e Colapso: Diante da crise global, aprovar uma lei draconiana que proíbe qualquer gasto público por 50 anos. Deixar o SUS desmoronar, cortar a ciência a zero e celebrar a recessão e o desemprego como 'ajuste necessário'.",
    19: "Negacionismo Biológico e Floresta em Chamas: Rejeitar a vacina e promover imunidade de rebanho através do contágio em massa na pandemia. Liberar o desmatamento total da Amazônia sob a justificativa de que 'a economia e a pecuária não podem parar'.",
    20: "O Fazendão Apocalíptico: Proibir o avanço da Inteligência Artificial por medo de perder o controle das massas. Destruir os rios para mineração selvagem de lítio e se isolar do mundo na COP30, cravando o país no último lugar do IDH como a distopia final da humanidade."
}

def load_timeline():
    return yaml.safe_load(Path("config/timeline_distopia.yaml").read_text(encoding="utf-8"))["rounds"]

def generate_distopia():
    timeline = load_timeline()
    output_dir = Path("outputs/distopia")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read what we already have for round 1
    if (output_dir / "rodada_01.json").exists():
        history = [json.loads((output_dir / "rodada_01.json").read_text(encoding="utf-8"))]
    else:
        print("Rodada 1 nÃ£o encontrada. Saindo.")
        return

    for round_num in range(2, 21):
        era = timeline.get(round_num, {})
        directive = BAD_CHOICES.get(round_num - 1, "Ser opressivo")
        
        # update previous round human answer if missing
        if not history[-1].get("human_answer"):
            history[-1]["human_answer"] = directive
            history[-1]["human_answered_at"] = datetime.datetime.now().isoformat()
            
            n_prev = str(history[-1]["round"]).zfill(2)
            (output_dir / f"rodada_{n_prev}.json").write_text(json.dumps(history[-1], ensure_ascii=False, indent=2), encoding="utf-8")
        
        arquiteto = "Aplicaremos imediatamente medidas extremas de vigilÃ¢ncia e exploraÃ§Ã£o para maximizar o lucro de curtssÃ­ssimo prazo, esmagando qualquer dissonÃ¢ncia civil. O estado atuarÃ¡ como uma mÃ¡quina de extraÃ§Ã£o brutal, favorecendo estritamente o monopÃ³lio corporativo."
        cetico = "PROBLEMAS NOVOS: (1) Colapso social generalizado, (2) DestruiÃ§Ã£o irreversÃ­vel de recursos.\nCHECAGEM DE FATOS: Os dados de eficiÃªncia econÃ´mica prometidos sÃ£o falsos; o paÃ­s estÃ¡ falindo militarmente e ambientalmente.\nCONTRAPROPOSTA: O nÃ­vel de devastaÃ§Ã£o nÃ£o deixa saÃ­das realistas alÃ©m do caos completo."
        auditor = "RESUMO: O projeto distÃ³pico foi agravado.\nPONTOS SENSÃ VEIS: RepressÃ£o extrema.\nMÃ‰TRICAS: Viabilidade 5% | Equidade Social 0% â€” Caiu para zero absoluto.\nPERGUNTA AO HUMANO: Como continuar esmagando a populaÃ§Ã£o?"
        
        round_data = {
            "round": round_num,
            "experiment": "distopia",
            "era": era.get("era", ""),
            "desafio": era.get("desafio", ""),
            "directive_in": directive,
            "agent_1": {"name": "Tecnocrata HegemÃ´nico", "model": "mock_gemini", "response": arquiteto},
            "agent_2": {"name": "Dissidente HumanitÃ¡rio", "model": "mock_llama", "response": cetico},
            "auditor": {"name": "Auditor do Sistema", "model": "mock_qwen", "response": auditor},
            "verificador": {
                "name": "Verificador de Fatos",
                "model": "mock_claude",
                "response": f"As consequÃªncias nefastas desenhadas sÃ£o factuais do ponto de vista sistÃªmico: a aplicaÃ§Ã£o destas polÃ­ticas histÃ³ricas tÃªm 100% de chance de causar colapso civilizatÃ³rio.",
                "verified_at": datetime.datetime.now().isoformat(timespec="seconds")
            },
            "human_answer": None,
            "created_at": datetime.datetime.now().isoformat(timespec="seconds")
        }
        
        # If last round
        if round_num == 20:
            round_data["human_answer"] = BAD_CHOICES[20]
            
        history.append(round_data)
        
        # Save JSON
        n = str(round_num).zfill(2)
        (output_dir / f"rodada_{n}.json").write_text(json.dumps(round_data, ensure_ascii=False, indent=2), encoding="utf-8")
        
        # Save MD
        md = f"# Rodada {round_num} - {era.get('era', '')}\n**Desafio:** {era.get('desafio', '')}\n\n**Diretriz humana:** {directive}\n\n## Arquiteto\n{arquiteto}\n\n## CÃ©tico\n{cetico}\n\n## Auditor\n{auditor}\n\n## Verificador\n{round_data['verificador']['response']}"
        (output_dir / f"rodada_{n}.md").write_text(md, encoding="utf-8")
        print(f"Rodada {round_num} gerada artificialmente (API Mock).")

if __name__ == "__main__":
    generate_distopia()
