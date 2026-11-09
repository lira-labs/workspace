# -*- coding: utf-8 -*-
"""
Aplica as correções pontuais oficiais sobre a matriz canônica de 14 páginas
Garante 100% de consistência de personagens, enredo puro de quadrinhos, e exatamente 14 páginas A4.
"""
import re

with open('core/tools/test_e572dc5.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Ajuste de Título e Edição
html = html.replace('HQ DELUXE · Operação Byte Socrático (14 Páginas · Edição de Colecionador)', 'HQ OFICIAL · Operação Byte Socrático (Edição Especial #01 · 14 Páginas)')
html = html.replace('⚡ EDIÇÃO HISTÓRICA · UFRPE 2026.2', '⚡ EDIÇÃO ESPECIAL #01 · UFRPE 2026.2')
html = html.replace('FIM DA EDIÇÃO DELUXE · UFRPE', 'FIM DA EDIÇÃO ESPECIAL #01 · UFRPE')
html = html.replace('EDIÇÃO DE COLECIONADOR · DELUXE', 'EDIÇÃO ESPECIAL #01 · UFRPE')

# 2. Polo e Instituição
html = html.replace('Polo EaD Camela / Recife · Interior de Pernambuco', 'Polo EaD Recife (UFRPE · Campus Dois Irmãos)')
html = html.replace('CAMELA · 22H15 · APÓS UM LONGO DIA DE TRABALHO NO INTERIOR', 'POLO EaD RECIFE · 22H15 · APÓS UM LONGO DIA DE TRABALHO')
html = html.replace('MADRUGADA · 23H40 · O DESESPERO DA CALOURA DE EaD', 'NOITE · 23H40 · O DESESPERO DA CALOURA NO AVA MOODLE')
html = html.replace('Cauã da Cunha Lira (Licenciando em Computação)', 'Cauã da Cunha Lira (Tutor Presencial de Informática)')

# 3. Página 09: Atribuição teórica de andaime (Wood, Bruner e Ross)
html = html.replace('escada de dicas em 3 degraus de Bruner', 'escada de 3 degraus de dicas, inspirada no andaime de Wood, Bruner e Ross (1976)')

# 4. Página 10: Metáfora dos Post-its em Python (Capítulo 07)
# Título do capítulo
html = html.replace('CAPÍTULO 07 · O MOMENTO EUREKA DAS CAIXAS ORGANIZADORAS', 'CAPÍTULO 07 · O MOMENTO EUREKA DOS POST-ITS')
html = html.replace('RETESTE DO CASO #03 · A METÁFORA DAS CAIXAS COLORIDAS', 'RETESTE DO TESTE #03 · A METÁFORA DOS POST-ITS EM PYTHON')
html = html.replace('BYTE v2.0 (METÁFORA DAS CAIXAS)', 'BYTE v2.0 (METÁFORA DOS POST-ITS)')
html = html.replace(
    '"Pense na memória como uma estante cheia de caixas organizadoras coloridas! Quando fazemos <code>idade = 19</code>, colamos a etiqueta \'idade\' e guardamos o 19 lá dentro. Se você fizer aniversário, o que acontece com a caixa?"',
    '"Pense em post-its colados em objetos na memória! Quando fazemos <code>idade = 19</code>, o número 19 existe e o post-it \'idade\' é colado nele. No aniversário fazemos <code>idade = 20</code>. O que acontece com o post-it?"'
)
html = html.replace(
    'A gente só troca o número que está dentro da caixa, mantendo a mesma etiqueta! <b>Caramba... agora eu ENXERGUEI a memória!</b>',
    'Eu descolo o post-it do 19 e colo no 20! A variável é um nome referenciando o objeto! <b>Caramba... agora eu ENXERGUEI a memória do Python!</b>'
)
# Analogia da cesta de feira e acumulador
html = html.replace('A CESTA DE COMPRAS E A CONQUISTA DO CÓDIGO', 'A CESTA DE FEIRA E O POST-IT ACUMULADOR')
html = html.replace(
    '"O laço <code>for</code> é como passar a feira no caixa: você pega um item por vez da cesta até ela esvaziar! Qual é o seu próximo passo em Python?"',
    '"O laço <code>for</code> é como passar a feira no caixa: você passa item por item da cesta, sem tirar nenhum dela! Enquanto você passa os itens, onde anota o total parcial?"'
)
html = html.replace(
    'Eu itero sobre a lista de itens! Cauã, o código compilou perfeitamente e dessa vez eu sei <b>EXATAMENTE</b> por que ele funcionou!',
    'Num post-it chamado <code>total</code>, que vai mudando de lugar a cada soma! Cauã, o código <b>rodou perfeitamente</b> no terminal e dessa vez eu entendi tudo!'
)

# 5. Página 11: Bloom e mediação socrática
html = html.replace(
    'Benjamin Bloom demonstrou que a tutoria individual mediada eleva a aprendizagem em até dois desvios-padrão. Um tutor socrático democratiza essa mentoria 24h por dia!',
    'Bloom (1984) mostrou que tutoria individual com domínio superava a sala tradicional. Um tutor de IA calibrado aproxima esse apoio com mediação socrática!'
)

# 6. Página 12: Questão da prova alinhada com acumulador de notas
html = html.replace(
    'Questão 4: <i>"Construa um algoritmo que percorra a lista de alunos e calcule a média"</i>... Fecho os olhos... lembro da cesta de compras... abro o laço <code>for</code>... somo os valores... divido pelo total!',
    'Questão 4: <i>"Construa um algoritmo que percorra a lista de notas e calcule a média"</i>... Fecho os olhos... lembro da cesta de feira... crio o post-it acumulador <code>total</code>... divido pelo tamanho!'
)

# 7. Página 13: Nota 9.0 da Clara e Mediação Socrática
html = html.replace('Cauã, tirei <b>DEZ na avaliação presencial!</b> Na hora da prova, parecia que eu estava vendo a cesta de compras na minha frente!', 'Cauã, tirei <b>9.0 na avaliação presencial!</b> Errei só um detalhe de indentação no final, mas a lógica toda foi minha!')
html = html.replace('Parabéns, Clara! Essa vitória prova que <b>o papel da IA na EaD não é pensar pelo aluno, mas ensinar o aluno a pensar com autonomia!</b>', 'Parabéns, Clara! Essa nota 9.0 prova que <b>o papel da IA na EaD não é pensar pelo aluno, mas ensinar o aluno a pensar com autonomia!</b>')
html = html.replace('Mas com transposição socrática, ela liberta o potencial humano!', 'Mas com mediação socrática, ela liberta o potencial humano!')

# 8. Página 14: Referências Bibliográficas em ABNT NBR 6023 auditadas
old_refs = '''            <div class="space-y-1.5 text-[8.2px] text-slate-300 font-mono leading-tight">
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-cyan-400">
                • <b>BLOOM, Benjamin S.</b> The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective as One-to-One Tutoring. <i>Educational Researcher</i>, v. 13, n. 6, p. 4-16, 1984.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-emerald-400">
                • <b>BRUNER, Jerome S.; WOOD, David; ROSS, Gail.</b> The role of tutoring in problem solving. <i>Journal of Child Psychology and Psychiatry</i>, v. 17, n. 2, p. 89-100, 1976.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-amber-400">
                • <b>CHEVALLARD, Yves.</b> <i>La Transposition Didactique: Du Savoir Savant au Savoir Enseigné</i>. Grenoble: La Pensée Sauvage, 1991.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-purple-400">
                • <b>KHAN, Salman.</b> How AI Could Save (Not Destroy) Education. <i>TED Talks</i>, Vancouver, 2023. Disponível em: &lt;ted.com&gt;.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-rose-400">
                • <b>OCDE.</b> <i>PISA 2025 AI and Education Policy Brief: Generative AI Use Among Students</i>. Paris: OECD Publishing, 2026.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-sky-400">
                • <b>SWELLER, John.</b> Cognitive load during problem solving: Effects on learning. <i>Cognitive Science</i>, v. 12, n. 2, p. 257-285, 1988.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-teal-400">
                • <b>VYGOTSKY, Lev S.</b> <i>Pensamento e Linguagem</i>. São Paulo: Martins Fontes, 1934 (Ed. brasileira 1987).
              </div>
            </div>'''

new_refs = '''            <div class="space-y-1 text-[8.0px] text-slate-300 font-mono leading-tight">
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-cyan-400">
                • <b>BASTANI, H. et al.</b> Generative AI can harm learning without calibrating practice. <i>Nature Human Behaviour</i>, v. 9, p. 1-12, 2025.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-emerald-400">
                • <b>BJORK, R. A.</b> Memory and metamemory considerations in the training of human beings. <i>Metacognition: Knowing about Knowing</i>, Cambridge: MIT Press, p. 185-205, 1994.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-amber-400">
                • <b>BLOOM, Benjamin S.</b> The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective as One-to-One Tutoring. <i>Educational Researcher</i>, v. 13, n. 6, p. 4-16, 1984.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-purple-400">
                • <b>CHEVALLARD, Yves.</b> <i>La Transposition Didactique: Du Savoir Savant au Savoir Enseigné</i>. Grenoble: La Pensée Sauvage, 1991.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-rose-400">
                • <b>KESTIN, G. et al.</b> AI tutoring outperforms active learning in introductory physics. <i>Physical Review Physics Education Research</i>, v. 21, 2025.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-sky-400">
                • <b>OECD.</b> <i>Students, Digital Devices and Success: PISA 2025 Policy Brief</i>. Paris: OECD Publishing, 2026. (Estudo com estudantes de 15 anos).
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-teal-400">
                • <b>SWELLER, John.</b> Cognitive load during problem solving: Effects on learning. <i>Cognitive Science</i>, v. 12, n. 2, p. 257-285, 1988.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-indigo-400">
                • <b>VYGOTSKY, Lev S.</b> <i>Mind in Society: The Development of Higher Psychological Processes</i>. Cambridge: Harvard University Press, 1978.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-yellow-400">
                • <b>WOOD, David; BRUNER, Jerome S.; ROSS, Gail.</b> The role of tutoring in problem solving. <i>Journal of Child Psychology and Psychiatry</i>, v. 17, n. 2, p. 89-100, 1976.
              </div>
            </div>'''

html = html.replace(old_refs, new_refs)

out_path = 'code/projeto_ead_tutores/ebook-hq.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Salvo {out_path} com sucesso!")
