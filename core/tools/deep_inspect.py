import urllib.request
import re

# 1. Inspect Marcio's game
req = urllib.request.Request('https://marcio-vercel.vercel.app/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    # find section with id="jogo"
    jogo_match = re.search(r'<section[^>]+id=[\'"]jogo[\'"][^>]*>(.*?)</section>', html, re.I | re.S)
    if jogo_match:
        print("=== MARCIO JOGO SNIPPET ===")
        print(re.sub(r'<[^>]+>', ' ', jogo_match.group(1))[:800])
        print("...")

# 2. Inspect Lucas's React bundle
req = urllib.request.Request('https://minicurso-pandas.vercel.app/assets/index-CjTvtcvA.js', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    js = resp.read().decode('utf-8', errors='ignore')
    print("\n=== LUCAS REACT BUNDLE ===")
    print("JS size:", len(js))
    # find links inside js
    links = re.findall(r'https?://[^\s"\'`<>]+', js)
    print("Links in Lucas's JS:")
    for l in set(links):
        if any(k in l.lower() for k in ['youtube', 'fliphtml5', 'genially', 'canva', 'drive', 'forms', 'github', 'vercel', 'spotify', 'anchor', 'pdf']):
            print("  ->", l)
            
    # search for keywords like "ebook", "podcast", "jogo", "infográfico", "videoaula"
    headings = re.findall(r'["\']([A-ZÁÉÍÓÚÂÊÎÔÛÃÕÇ][^"\']{5,60})["\']', js)
    print("Some headings/titles in Lucas JS:")
    interesting = [h for h in headings if any(w in h.lower() for w in ['pandas', 'ebook', 'vídeo', 'aula', 'infogr', 'podcast', 'jogo', 'avalia', 'etapa', 'mídia'])]
    for h in interesting[:15]:
        print("  *", h)

# 3. Inspect Jovelino
req = urllib.request.Request('https://minicurso-ead.vercel.app/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    print("\n=== JOVELINO SITE ===")
    jogo_match = re.search(r'<section[^>]+id=[\'"]jogo[\'"][^>]*>(.*?)</section>', html, re.I | re.S)
    if jogo_match:
        print("Jovelino Jogo snippet:")
        print(re.sub(r'<[^>]+>', ' ', jogo_match.group(1))[:600])

# 4. Inspect Aecio
req = urllib.request.Request('https://minicurso-estude-com-ia.vercel.app/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    print("\n=== AECIO SITE ===")
    links = re.findall(r'<a[^>]+href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>', html, re.I | re.S)
    for href, text in links:
        clean = re.sub(r'<[^>]+>', '', text).strip()
        print(f"  [{clean}] -> {href}")
