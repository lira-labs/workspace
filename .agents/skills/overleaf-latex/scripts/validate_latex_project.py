"""Quality Gate estático para projetos LaTeX/Overleaf.

Verifica integridade de \\cite vs .bib, \\ref vs \\label, \\input existentes,
balanceamento de ambientes, ausência de tokens secretos e padrões de AI slop.
"""

from __future__ import annotations

import pathlib
import re
import sys

AI_SLOP_PATTERNS = [
    r"\brevolutionizing\b",
    r"\bgroundbreaking\b",
    r"\bgame[- ]changing\b",
    r"\bunprecedented\b",
    r"\binnovative solution\b",
    r"\brevolutiona(?:ndo|ria)\b",
    r"\bsem precedentes\b",
]


def validate_project(project_dir: pathlib.Path) -> int:
    """Executa auditoria completa em um diretório LaTeX."""
    main_tex = project_dir / "main.tex"
    if not main_tex.is_file():
        print(f"[ERRO] main.tex nao encontrado em {project_dir}")
        return 1

    tex_files = [main_tex]
    sections_dir = project_dir / "sections"
    if sections_dir.is_dir():
        tex_files.extend(sorted(sections_dir.rglob("*.tex")))

    bib_files = sorted(project_dir.glob("*.bib"))
    bib_keys: set[str] = set()
    bib_text = ""
    for bf in bib_files:
        content = bf.read_text(encoding="utf-8", errors="replace")
        bib_text += "\n" + content
        bib_keys.update(re.findall(r"@\w+\{([^,\s]+)", content))

    cites: set[str] = set()
    labels: set[str] = set()
    refs: set[str] = set()
    inputs: list[str] = []
    errors: list[str] = []
    warnings: list[str] = []

    for tf in tex_files:
        rel = tf.relative_to(project_dir)
        txt = tf.read_text(encoding="utf-8", errors="replace")

        if "olp_" in txt:
            errors.append(f"Token secreto detectado em {rel}")
        if "??" in txt:
            warnings.append(f"Marcador '??' encontrado em {rel}")

        for pat in AI_SLOP_PATTERNS:
            if re.search(pat, txt, flags=re.IGNORECASE):
                warnings.append(f"Possivel AI slop ({pat}) em {rel}")

        for match in re.findall(r"\\cite[tp]?\{([^}]+)\}", txt):
            for key in match.split(","):
                cites.add(key.strip())

        for match in re.findall(r"\\label\{([^}]+)\}", txt):
            labels.add(match.strip())

        for match in re.findall(r"\\(?:auto|page|eq)?ref\{([^}]+)\}", txt):
            refs.add(match.strip())

        for match in re.findall(r"\\input\{([^}]+)\}", txt):
            inputs.append(match.strip())

        begins = re.findall(r"\\begin\{([^}]+)\}", txt)
        ends = re.findall(r"\\end\{([^}]+)\}", txt)
        if sorted(begins) != sorted(ends):
            errors.append(f"Ambientes LaTeX desbalanceados em {rel}")

    if "olp_" in bib_text:
        errors.append("Token secreto detectado em arquivo .bib")

    missing_cites = sorted(cites - bib_keys)
    unused_bib = sorted(bib_keys - cites)
    missing_refs = sorted(refs - labels)
    missing_inputs = [
        inp for inp in inputs if not (project_dir / (inp if inp.endswith(".tex") else f"{inp}.tex")).is_file()
    ]

    if missing_cites:
        errors.append(f"Citacoes ausentes no .bib: {missing_cites}")
    if missing_refs:
        errors.append(f"Referencias cruzadas sem \\label: {missing_refs}")
    if missing_inputs:
        errors.append(f"Arquivos \\input ausentes: {missing_inputs}")
    if unused_bib:
        warnings.append(f"Entradas no .bib nao citadas: {unused_bib}")

    print(f"Projeto: {project_dir}")
    print(f"Arquivos .tex: {len(tex_files)} | Chaves .bib: {len(bib_keys)} | Citadas: {len(cites)}")
    print(f"Labels: {len(labels)} | Refs: {len(refs)}")
    for w in warnings:
        print(f"[AVISO] {w}")
    for e in errors:
        print(f"[ERRO] {e}")

    if errors:
        print("STATUS: REPROVADO")
        return 1
    print("STATUS: APROVADO")
    return 0


if __name__ == "__main__":
    target = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(".")
    raise SystemExit(validate_project(target.resolve()))
