"""
Script de treinamento individual de uma emoção.

Uso:
    python treinar.py <emoção> [epochs]

Exemplos:
    python treinar.py raiva          # Treina raiva com 200 epochs (padrão)
    python treinar.py alegria 500    # Treina alegria com 500 epochs
"""

import sys
import os

# Garante que prints com caracteres especiais funcionem no Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Suprime avisos verbosos do TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from modelo_emocao import ModeloEmocao

EMOCOES_VALIDAS = ['raiva', 'medo', 'alegria', 'tristeza', 'nojinho']


def main():
    if len(sys.argv) < 2:
        print("❌ Uso: python treinar.py <emoção> [epochs]")
        print(f"   Emoções disponíveis: {', '.join(EMOCOES_VALIDAS)}")
        sys.exit(1)

    emocao = sys.argv[1].lower()

    if emocao == 'todas':
        # Atalho para treinar todas de uma vez
        for e in EMOCOES_VALIDAS:
            _treinar_emocao(e, _parse_epochs())
        return

    if emocao not in EMOCOES_VALIDAS:
        print(f"❌ Emoção '{emocao}' não reconhecida.")
        print(f"   Emoções disponíveis: {', '.join(EMOCOES_VALIDAS)}")
        sys.exit(1)

    _treinar_emocao(emocao, _parse_epochs())


def _parse_epochs():
    """Lê o número de epochs da linha de comando (padrão 200)."""
    if len(sys.argv) >= 3:
        try:
            return int(sys.argv[2])
        except ValueError:
            print("⚠️  Epochs inválido, usando 200")
    return 200


def _treinar_emocao(emocao, epochs):
    """Treina e salva o modelo de uma emoção."""
    modelo = ModeloEmocao(emocao)
    modelo.treinar(epochs=epochs)
    modelo.salvar()

    print(f"\n🎉 Treinamento da emoção '{emocao.upper()}' concluído!")
    print(f"   Teste com: python chatbot.py --emocao {emocao}\n")


if __name__ == '__main__':
    main()
