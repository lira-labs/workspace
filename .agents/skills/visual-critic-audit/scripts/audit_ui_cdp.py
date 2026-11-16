"""Auditoria visual headless via Chrome CDP para o GrafoParada (Mobile 390x844 + Desktop 1280x800)."""
from __future__ import annotations

import argparse
import base64
import json
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path
from websockets.sync.client import connect as ws_connect

CHROME_PATHS = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
]

AUDIT_JS = """(() => {
    const docW = document.documentElement.scrollWidth;
    const winW = window.innerWidth;
    const winH = window.innerHeight;
    const offenders = [];
    document.querySelectorAll('*').forEach(el => {
        const st = getComputedStyle(el);
        if (st.display === 'none' || st.visibility === 'hidden' || st.opacity === '0') return;
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) return;
        if (r.right > winW + 2 || r.left < -2) {
            if (el.closest('.leaflet-pane')) return;
            offenders.push({
                tag: el.tagName,
                id: el.id || '',
                cls: (typeof el.className === 'string') ? el.className.slice(0, 60) : '',
                left: Math.round(r.left),
                right: Math.round(r.right),
                w: Math.round(r.width)
            });
        }
    });
    const sheet = document.querySelector('.mobile-bottom-sheet');
    const sheetRect = sheet ? sheet.getBoundingClientRect() : null;
    const ctm = document.getElementById('desktop-ctm-workspace');
    const lab = document.getElementById('desktop-lab-workspace');
    return {
        docW,
        winW,
        winH,
        overflowX: docW - winW,
        offenders: offenders.slice(0, 10),
        sheetH: sheetRect ? Math.round(sheetRect.height) : null,
        ctmVisible: ctm ? getComputedStyle(ctm).display !== 'none' : false,
        labVisible: lab ? getComputedStyle(lab).display !== 'none' : false,
    };
})()"""


def find_chrome() -> str:
    for p in CHROME_PATHS:
        if p.exists():
            return str(p)
    raise RuntimeError("Chrome/Edge nao encontrado nesta maquina.")


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


class CDPClient:
    def __init__(self, ws_url: str) -> None:
        self.ws = ws_connect(ws_url, max_size=32 * 1024 * 1024)
        self.msg_id = 0
        self.console_errors: list[str] = []
        self.exceptions: list[str] = []

    def _handle_event(self, pkt: dict) -> None:
        m = pkt.get("method")
        p = pkt.get("params", {})
        if m == "Runtime.exceptionThrown":
            txt = p.get("exceptionDetails", {}).get("text", "")
            self.exceptions.append(txt)
        elif m == "Runtime.consoleAPICalled":
            if p.get("type") == "error":
                args = " ".join(str(a.get("value", a.get("description", ""))) for a in p.get("args", []))
                self.console_errors.append(args)
        elif m == "Fetch.requestPaused":
            req_id = p.get("requestId")
            req = p.get("request", {})
            method = str(req.get("method", "GET")).upper()
            payload = {
                "ok": True,
                "persisted": "client_local_pending_db",
                "db_configured": False,
                "available": False,
                "storage": "client_local",
                "record": {"id": "local_audit_rec"},
            }
            body_b64 = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("ascii")
            self.msg_id += 1
            self.ws.send(json.dumps({
                "id": self.msg_id,
                "method": "Fetch.fulfillRequest",
                "params": {
                    "requestId": req_id,
                    "responseCode": 202 if method == "POST" else 200,
                    "responseHeaders": [
                        {"name": "Content-Type", "value": "application/json; charset=utf-8"},
                    ],
                    "body": body_b64,
                },
            }))

    def call(self, method: str, params: dict | None = None) -> dict:
        self.msg_id += 1
        mid = self.msg_id
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"CDP error in {method}: {msg['error']}")
                return msg.get("result", {})
            if "method" in msg:
                self._handle_event(msg)

    def wait(self, seconds: float) -> None:
        deadline = time.monotonic() + seconds
        while True:
            rem = deadline - time.monotonic()
            if rem <= 0:
                break
            try:
                raw = self.ws.recv(timeout=min(0.05, rem))
                pkt = json.loads(raw)
                if "method" in pkt:
                    self._handle_event(pkt)
            except TimeoutError:
                continue

    def eval(self, expr: str):
        res = self.call("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        if "exceptionDetails" in res:
            raise RuntimeError(f"JS exception: {res['exceptionDetails']}")
        return res.get("result", {}).get("value")

    def wait_until(self, expr: str, timeout_s: float = 8.0, err_msg: str = "Timeout aguardando condicao") -> None:
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            if self.eval(expr):
                return
            self.wait(0.15)
        raise RuntimeError(err_msg)

    def screenshot(self, out_dir: Path, filename: str) -> None:
        res = self.call("Page.captureScreenshot", {"format": "png"})
        (out_dir / filename).write_bytes(base64.b64decode(res["data"]))

    def close(self) -> None:
        self.ws.close()


def run_audit(url: str, out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    chrome = find_chrome()
    cdp_port = find_free_port()
    user_data_dir = Path(tempfile.mkdtemp(prefix="gp_cdp_audit_"))
    proc = None
    failures = 0

    try:
        proc = subprocess.Popen(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-extensions",
                f"--remote-debugging-port={cdp_port}",
                f"--user-data-dir={user_data_dir}",
                "--window-size=390,844",
                "about:blank",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        ws_url = None
        deadline = time.time() + 12.0
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{cdp_port}/json/list", timeout=1.0) as resp:
                    pages = [t for t in json.loads(resp.read().decode("utf-8")) if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]
                    if pages:
                        ws_url = pages[0]["webSocketDebuggerUrl"]
                        break
            except Exception:
                time.sleep(0.2)
        if not ws_url:
            raise RuntimeError("Falha ao conectar ao Chrome DevTools Protocol.")

        cdp = CDPClient(ws_url)
        cdp.call("Page.enable")
        cdp.call("Runtime.enable")
        cdp.call(
            "Fetch.enable",
            {
                "patterns": [
                    {"urlPattern": "http://127.0.0.1*/api/*"},
                    {"urlPattern": "http://localhost*/api/*"},
                ]
            },
        )
        cdp.call("Emulation.setDeviceMetricsOverride", {"width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True})
        cdp.call("Page.navigate", {"url": url})

        cdp.wait_until(
            "Boolean(window.RealTransit && window.RealTransit.networkData && window.RealTransit.schedulesData)",
            timeout_s=12.0,
            err_msg="RealTransit/schedulesData nao carregaram a tempo.",
        )
        cdp.wait(0.8)

        def check(label: str, filename: str) -> None:
            nonlocal failures
            m = cdp.eval(AUDIT_JS)
            cdp.screenshot(out_dir, filename)
            if m["overflowX"] > 0:
                failures += 1
            print(f"[{label}] docW={m['docW']} winW={m['winW']} overflow={m['overflowX']} sheetH={m['sheetH']} -> {filename}")
            if m["offenders"]:
                print(f"  OFFENDERS: {m['offenders']}")

        # 00: Primeiro acesso limpo (Mobile 390x844) -> Modal de Onboarding Passo 1
        check("Mobile 00: Onboarding Passo 1 (Cadastro)", "00_onboarding_step1_mobile.png")

        # Verifica .desktop-outer-bar (#mode-btn-ctm / #mode-btn-lab) visivel e nao bloqueada em 1280x800 mesmo com onboarding aberto
        cdp.call("Emulation.setDeviceMetricsOverride", {"width": 1280, "height": 800, "deviceScaleFactor": 1, "mobile": False})
        cdp.wait(0.3)
        bar_check = cdp.eval("""(() => {
            const bar = document.querySelector('.desktop-outer-bar');
            const ctm = document.getElementById('mode-btn-ctm');
            const lab = document.getElementById('mode-btn-lab');
            const onb = document.getElementById('modal-onboarding');
            const hit = (el) => {
                if (!el) return false;
                const r = el.getBoundingClientRect();
                if (r.width <= 0 || r.height <= 0) return false;
                const target = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
                return Boolean(target && (target === el || el.contains(target)));
            };
            return {
                onbOpen: Boolean(onb && getComputedStyle(onb).display !== 'none'),
                barVisible: Boolean(bar && getComputedStyle(bar).display !== 'none'),
                ctmUnblocked: hit(ctm),
                labUnblocked: hit(lab),
                overflowX: document.documentElement.scrollWidth - window.innerWidth
            };
        })()""")
        print(f"[Desktop Onboarding Bar Check] {bar_check}")
        if not (bar_check["onbOpen"] and bar_check["barVisible"] and bar_check["ctmUnblocked"] and bar_check["labUnblocked"]):
            failures += 1

        # Retorna a Mobile 390x844 e conclui Passo 1 -> Passo 2 Cascata via UI real
        cdp.call("Emulation.setDeviceMetricsOverride", {"width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True})
        cdp.wait(0.3)

        cdp.eval("""(() => {
            document.getElementById('inp-name').value = 'Maria Silva';
            const contact = document.getElementById('inp-sync-contact');
            if (contact) contact.value = 'maria@recife.pe';
            document.getElementById('btn-onb-register-continue').click();
        })()""")
        cdp.wait_until(
            "getComputedStyle(document.getElementById('onboarding-step-routine')).display !== 'none'",
            timeout_s=6.0,
            err_msg="Passo 2 do onboarding nao abriu.",
        )

        cdp.eval("""(() => {
            const inp = document.getElementById('onb-origin-place');
            inp.value = 'Camela';
            inp.dispatchEvent(new Event('input', { bubbles: true }));
        })()""")
        cdp.wait_until("document.querySelectorAll('#onb-origin-place-list .gp-place-option').length > 0")
        cdp.eval("document.querySelector('#onb-origin-place-list .gp-place-option').click()")
        cdp.wait_until("document.querySelectorAll('#onb-origin-stops-list .gp-stop-card').length > 0")
        cdp.eval("document.querySelector('#onb-origin-stops-list .gp-stop-card').click()")

        cdp.eval("""(() => {
            const inp = document.getElementById('onb-dest-place');
            inp.value = 'TI Cabo';
            inp.dispatchEvent(new Event('input', { bubbles: true }));
        })()""")
        cdp.wait_until("document.querySelectorAll('#onb-dest-place-list .gp-place-option').length > 0")
        cdp.eval("document.querySelector('#onb-dest-place-list .gp-place-option').click()")
        cdp.wait_until("document.querySelectorAll('#onb-dest-stops-list .gp-stop-card').length > 0")
        cdp.eval("document.querySelector('#onb-dest-stops-list .gp-stop-card').click()")

        cdp.wait_until(
            "document.querySelectorAll('#onb-suggested-lines-box .gp-suggested-line-card').length > 0",
            timeout_s=6.0,
            err_msg="Linhas sugeridas GTFS nao apareceram no onboarding.",
        )
        cdp.eval("""(() => {
            document.getElementById('inp-custom-time').value = '06:15';
            document.getElementById('inp-custom-return').value = '18:10';
        })()""")
        cdp.wait(0.3)

        # 00b: Passo 2 preenchido com autocomplete + paradas + linhas/horarios GTFS antes de salvar
        cdp.eval("const s2 = document.getElementById('onboarding-step-routine'); if (s2) s2.scrollTop = 0;")
        cdp.wait(0.15)
        check("Mobile 00b: Onboarding Passo 2 (Cascata GTFS)", "00b_onboarding_cascade_mobile.png")

        # 00c: Passo 2 rolado ate o bloco de linhas GTFS, horarios e botao salvar
        cdp.eval("""(() => {
            const s2 = document.getElementById('onboarding-step-routine');
            if (s2) s2.scrollTop = s2.scrollHeight;
            const saveBtn = document.getElementById('btn-onb-save-routine');
            if (saveBtn) saveBtn.scrollIntoView({ block: 'end' });
        })()""")
        cdp.wait(0.25)
        check("Mobile 00c: Onboarding Passo 2 (Horarios GTFS + Salvar)", "00c_onboarding_step2_bottom.png")

        # Salva clicando na UI real (sem injetar localStorage artificial)
        cdp.eval("document.getElementById('btn-onb-save-routine').click()")
        cdp.wait_until(
            "getComputedStyle(document.getElementById('modal-onboarding')).display === 'none'",
            timeout_s=6.0,
            err_msg="Modal onboarding nao fechou ao salvar rotina.",
        )
        cdp.wait(0.6)

        check("Mobile 1: Home", "01_home_mobile.png")
        cdp.eval("window.navigateToScreen('locate')")
        cdp.wait(0.7)
        check("Mobile 2: Locate", "02_locate_mobile.png")

        cdp.eval("window.navigateToScreen('radar')")
        cdp.wait(1.5)
        check("Mobile 3: Mapa ao Vivo", "03_mapa_ao_vivo_mobile.png")

        cdp.eval("window.openLayaModal()")
        cdp.wait(0.5)
        check("Mobile 3b: Modal Laya IA", "03b_laya_mobile.png")
        cdp.eval("window.closeLayaModal()")
        cdp.wait(0.3)

        cdp.eval("window.navigateToScreen('central')")
        cdp.wait(0.7)
        check("Mobile 4: Central & Seguranca", "04_central_seguranca_mobile.png")

        cdp.eval("window.openRoutineModal()")
        cdp.wait(0.6)
        check("Mobile 4b: Modal Rotina Diaria (Hidratacao)", "04b_rotina_mobile.png")
        cdp.eval("window.closeRoutineModal()")
        cdp.wait(0.3)

        cdp.eval("window.openDispatchModal()")
        cdp.wait(0.6)
        check("Mobile 5: Modal Central CTM", "05_modal_ctm_mobile.png")
        cdp.eval("window.closeDispatchModal()")
        cdp.wait(0.3)

        cdp.eval("openProfileModal()")
        cdp.wait(0.5)
        check("Mobile 5b: Modal Perfil Passageiro", "05b_perfil_mobile.png")
        cdp.eval("closeProfileModal()")
        cdp.wait(0.3)

        cdp.call("Emulation.setDeviceMetricsOverride", {"width": 1280, "height": 800, "deviceScaleFactor": 1, "mobile": False})
        cdp.eval("window.navigateToScreen('radar'); window.setAppMode('passenger');")
        cdp.wait(1.0)
        check("Desktop 1: Modo Passageiro", "06_desktop_passageiro.png")

        cdp.eval("window.setAppMode('ctm')")
        cdp.wait(0.7)
        check("Desktop 2: Modo Central CTM", "07_desktop_central_ctm.png")

        cdp.eval("window.setAppMode('lab')")
        cdp.wait(0.7)
        check("Desktop 3: Modo Pesquisa & Banca", "08_desktop_pesquisa_banca.png")

        print(f"Console errors: {len(cdp.console_errors)} | JS exceptions: {len(cdp.exceptions)}")
        if cdp.console_errors:
            print(f"  CONSOLE ERRORS: {cdp.console_errors}")
        if cdp.exceptions:
            print(f"  JS EXCEPTIONS: {cdp.exceptions}")
        if cdp.console_errors or cdp.exceptions:
            failures += len(cdp.console_errors) + len(cdp.exceptions)
        cdp.close()
    finally:
        if proc:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except Exception:
                proc.kill()
        shutil.rmtree(user_data_dir, ignore_errors=True)
    return 1 if failures else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8767/index.html")
    parser.add_argument("--out-dir", default="design-references/current_screenshots")
    args = parser.parse_args()
    raise SystemExit(run_audit(args.url, Path(args.out_dir)))
