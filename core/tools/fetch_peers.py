import urllib.request
import re
import json

sites = {
    'Marcio Antonio': 'https://marcio-vercel.vercel.app/',
    'Jovelino Gomes': 'https://minicurso-ead.vercel.app/',
    'Aecio Jose': 'https://minicurso-estude-com-ia.vercel.app/',
    'Lucas Aurelio': 'https://minicurso-pandas.vercel.app/'
}

for name, url in sites.items():
    print(f"\n==========================================")
    print(f"=== {name} ({url}) ===")
    print(f"==========================================")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw = resp.read()
            html = raw.decode('utf-8', errors='ignore')
            print(f"HTTP Status: {resp.status} | Size: {len(html)} bytes")
            
            # Title
            title_m = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
            print("Title:", title_m.group(1).strip() if title_m else "N/A")
            
            # Headings
            h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.S)
            h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.I | re.S)
            print("H1s:", [re.sub(r'<[^>]+>', '', h).strip() for h in h1s][:4])
            print("H2s:", [re.sub(r'<[^>]+>', '', h).strip() for h in h2s][:6])
            
            # Links
            hrefs = re.findall(r'href=[\'"]([^\'"]+)[\'"]', html, re.I)
            srcs = re.findall(r'src=[\'"]([^\'"]+)[\'"]', html, re.I)
            
            external_links = [h for h in set(hrefs) if h.startswith('http')]
            media_links = [h for h in external_links if any(x in h.lower() for x in ['fliphtml5', 'genially', 'canva', 'youtube', 'drive.google', 'forms', 'podcast', 'spotify', 'anchor', 'infograf', 'docs.google'])]
            
            print("\nKey Media Links in href:")
            for l in media_links:
                print(f"  - {l}")
                
            print("\nKey Iframes / Embeds (src):")
            embeds = [s for s in set(srcs) if any(x in s.lower() for x in ['youtube', 'fliphtml5', 'genially', 'forms', 'spotify', 'anchor', 'drive'])]
            for s in embeds:
                print(f"  - {s}")
                
    except Exception as e:
        print(f"Error fetching {url}: {e}")
