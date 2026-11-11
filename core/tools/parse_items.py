with open('core/tools/pedido_professor_full.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(\n(?:PARTE \d|[0-9]\.[0-9]+|CRITÉRIOS DE ACEITE).*?)(?=\n(?:PARTE \d|[0-9]\.[0-9]+|CRITÉRIOS DE ACEITE)|\Z)', text, re.DOTALL)
print(f"Total de itens encontrados: {len(matches)}")
for m in matches[:35]:
    lines = m.strip().splitlines()
    print("Item:", lines[0][:80])
