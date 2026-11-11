with open('core/tools/pedido_professor_full.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
sections = re.findall(r'(={20,}\nPARTE \d.*?|CRITÉRIOS DE ACEITE.*?)(\n={20,}|\Z)', text, re.DOTALL)
print(f"Total de seções encontradas: {len(sections)}")
for s, _ in sections:
    first_lines = s.strip().splitlines()[:5]
    print("\n--- SEÇÃO ---")
    for fl in first_lines:
        print(fl)
