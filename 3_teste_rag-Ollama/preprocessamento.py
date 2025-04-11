# preprocessors.py
import re
from typing import List

def extrair_blocos_relevantes(texto: str) -> List[str]:
    blocos = texto.split("\n\n")
    blocos_relevantes = []

    for bloco in blocos:
        bloco = bloco.strip()
        if len(bloco) < 50:
            continue

        # Excluir rodapés/cabeçalhos genéricos
        if "aws cli command reference" in bloco.lower():
            continue

        # Incluir blocos com comandos da AWS
        if re.search(r'\baws\s+\w+', bloco):
            blocos_relevantes.append(bloco)
        # Ou blocos que contêm exemplos com $
        elif "$ aws " in bloco:
            blocos_relevantes.append(bloco)

    return blocos_relevantes
