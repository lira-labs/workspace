import shutil
import os

src_antes = r'C:\Users\conta\.gemini\antigravity\brain\7cdd1353-603d-4398-85bf-4ec0c836a66e\.user_uploaded\media_1788914943440.png'
src_depois = r'C:\Users\conta\.gemini\antigravity\brain\7cdd1353-603d-4398-85bf-4ec0c836a66e\.user_uploaded\media_1788915092097.png'

dst_antes = r'D:\workspace\code\overleaf_mlp\figures\antes.png'
dst_depois = r'D:\workspace\code\overleaf_mlp\figures\depois.png'

shutil.copy(src_antes, dst_antes)
shutil.copy(src_depois, dst_depois)
print("Imagens LaTeX atualizadas com sucesso.")
