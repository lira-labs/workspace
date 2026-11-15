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
            m = msg.get("method")
            if m == "Runtime.exceptionThrown":
                txt = msg.get("params", {}).get("exceptionDetails", {}).get("text", "")
                self.exceptions.append(txt)
            elif m == "Runtime.consoleAPICalled":
                p = msg.get("params", {})
                if p.get("type") == "error":
                    args = " ".join(str(a.get("value", a.get("description", ""))) for a in p.get("args", []))
                    self.console_errors.append(args)

    def eval(self, expr: str):
        res = self.call("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        if "exceptionDetails" in res:
            raise RuntimeError(f"JS exception: {res['exceptionDetails']}")
        return res.get("result", {}).get("value")

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
        cdp.call("Emulation.setDeviceMetricsOverride", {"width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True})
        cdp.call("Page.navigate", {"url": url})
        time.sleep(2.5)

        def check(label: str, filename: str) -> None:
            nonlocal failures
            m = cdp.eval(AUDIT_JS)
            cdp.screenshot(out_dir, filename)
            if m["overflowX"] > 0:
                failures += 1
            print(f"[{label}] docW={m['docW']} winW={m['winW']} overflow={m['overflowX']} sheetH={m['sheetH']} -> {filename}")
            if m["offenders"]:
                print(f"  OFFENDERS: {m['offenders']}")

        check("Mobile 1: Home", "01_home_mobile.png")
        cdp.eval("window.navigateToScreen('locate')")
        time.sleep(0.7)
        check("Mobile 2: Locate", "02_locate_mobile.png")

        cdp.eval("window.navigateToScreen('radar')")
        time.sleep(1.5)
        check("Mobile 3: Mapa ao Vivo", "03_mapa_ao_vivo_mobile.png")

        cdp.eval("window.navigateToScreen('central')")
        time.sleep(0.7)
        check("Mobile 4: Central & Seguranca", "04_central_seguranca_mobile.png")

        cdp.eval("window.openDispatchModal()")
        time.sleep(0.6)
        check("Mobile 5: Modal Central CTM", "05_modal_ctm_mobile.png")
        cdp.eval("window.closeDispatchModal()")
        time.sleep(0.3)

        cdp.call("Emulation.setDeviceMetricsOverride", {"width": 1280, "height": 800, "deviceScaleFactor": 1, "mobile": False})
        cdp.eval("window.navigateToScreen('radar'); window.setAppMode('passageiro');")
        time.sleep(1.0)
        check("Desktop 1: Modo Passageiro", "06_desktop_passageiro.png")

        cdp.eval("window.setAppMode('ctm')")
        time.sleep(0.7)
        check("Desktop 2: Modo Central CTM", "07_desktop_central_ctm.png")

        cdp.eval("window.setAppMode('lab')")
        time.sleep(0.7)
        check("Desktop 3: Modo Pesquisa & Banca", "08_desktop_pesquisa_banca.png")

        print(f"Console errors: {len(cdp.console_errors)} | JS exceptions: {len(cdp.exceptions)}")
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
