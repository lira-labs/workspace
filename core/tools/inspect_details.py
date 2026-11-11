import urllib.request
import re

def inspect_site(name, url):
    print(f"\n==========================================")
    print(f"=== DETALHES DE: {name} ({url}) ===")
    print(f"==========================================")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            # Print entire html if small, or key sections
            if len(html) < 2000:
                print("RAW HTML (small site):")
                print(html)
            else:
                # search for sections, nav, headings, links
                print("Search sections & keywords:")
                for match in re.finditer(r'<(h[1-4]|section|nav|header|footer|div\s+id=[\'"][^\'"]+[\'"])[^>]*>(.*?)</\1>', html, re.I | re.S):
                    tag_info = match.group(0)[:150].replace('\n', ' ')
                    # print snippet
                    # print(f"  Tag: {tag_info}...")
                
                # Look for all links and text around them
                links = re.findall(r'<a[^>]+href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>', html, re.I | re.S)
                print("\nAll Links in <a> tags:")
                for href, text in links:
                    clean_text = re.sub(r'<[^>]+>', '', text).strip()
                    if clean_text or 'http' in href:
                        print(f"  [{clean_text}] -> {href}")
                        
                # Look for iframes
                iframes = re.findall(r'<iframe[^>]+src=[\'"]([^\'"]+)[\'"][^>]*>', html, re.I | re.S)
                print("\nAll Iframes:")
                for src in iframes:
                    print(f"  src -> {src}")
                    
    except Exception as e:
        print(f"Erro: {e}")

inspect_site('Marcio Antonio', 'https://marcio-vercel.vercel.app/')
inspect_site('Lucas Aurelio', 'https://minicurso-pandas.vercel.app/')
