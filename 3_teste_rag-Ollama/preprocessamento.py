# preprocessors.py
import re
from typing import List

# Palavras-chave dos serviços que queremos priorizar
SERVICOS_FOCADOS = ['ec2', 'security-group', 'key pair', 'SSH', 'configure', 'help', 'vpc']

def extrair_blocos_relevantes(texto: str) -> List[str]:
    blocos = texto.split("\n\n")
    blocos_relevantes = []

    for bloco in blocos:
        bloco = bloco.strip()
        if len(bloco) < 50:
            continue
        
        bloco_lower = bloco.lower()

        if any(excluir in bloco_lower for excluir in [
            "aws cli command reference",
            "table of contents",
            "feedback",
            "copyright",
            "document history"
        ]):
            continue

        # Detectar comandos AWS diretamente
        if re.search(r'\baws\s+(' + "|".join(SERVICOS_FOCADOS) + r')\b', bloco_lower):
            blocos_relevantes.append(bloco)

        # Ou blocos com exemplos do terminal que envolvem esses serviços
        elif re.search(r'\$\s+aws\s+(' + "|".join(SERVICOS_FOCADOS) + r')\b', bloco_lower):
            blocos_relevantes.append(bloco)

        # Blocos com "usage" ou sintaxe de comandos, desde que relevante
        elif "usage:" in bloco_lower and any(s in bloco_lower for s in SERVICOS_FOCADOS):
            blocos_relevantes.append(bloco)

    return blocos_relevantes
