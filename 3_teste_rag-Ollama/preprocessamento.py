import re
from typing import List

def extrair_blocos_relevantes(texto: str) -> List[str]:
    # quebra em blocos de parágrafo
    blocos = texto.split("\n\n")

    for idx, bloco in enumerate(blocos):
        # detecta o cabeçalho de Examples (case‑insensitive, com ou sem "¶")
        if re.search(r'(?mi)^\s*Examples\s*¶?' or r'(?mi)^\s*examples\s*?', bloco):
            # retorna tudo a partir desse bloco
            return blocos[idx:]
    # se não encontrar, retorna lista vazia
    return []
