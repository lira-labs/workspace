import urllib.request
import re

req = urllib.request.Request('https://minicurso-pandas.vercel.app/assets/index-CjTvtcvA.js', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    js = resp.read().decode('utf-8', errors='ignore')
    
    # search for strings mentioning quiz, avaliacao, colab, notebook
    print("Matches for Lucas:")
    for m in re.finditer(r'[\'"`]([^\'"`]{10,120})[\'"`]', js):
        text = m.group(1)
        if any(w in text.lower() for w in ['avalia', 'quiz', 'colab', 'notebook', 'genially', 'exercício', 'pandas', 'etapa']):
            print("  -", text)
