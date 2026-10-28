"""
Interface principal do chatbot Divertida Mente.

Carrega as emoções treinadas e executa um loop interativo onde o usuário
digita pensamentos e cada emoção reage no seu estilo.

Uso:
    python chatbot.py                   # Todas as emoções
    python chatbot.py --emocao raiva    # Apenas a raiva
    python chatbot.py --debug           # Mostra tags e confiança
"""

import sys
import os
import json
import argparse

# Garante que prints com caracteres especiais funcionem no Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Suprime avisos verbosos do TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from modelo_emocao import ModeloEmocao

# Configuração visual de cada emoção
EMOCOES = {
    'raiva':    {'emoji': '😡', 'cor': '\033[91m', 'nome': 'RAIVA'},
    'medo':     {'emoji': '😨', 'cor': '\033[95m', 'nome': 'MEDO'},
    'alegria':  {'emoji': '😄', 'cor': '\033[93m', 'nome': 'ALEGRIA'},
    'tristeza': {'emoji': '😢', 'cor': '\033[94m', 'nome': 'TRISTEZA'},
    'nojinho':  {'emoji': '🤢', 'cor': '\033[92m', 'nome': 'NOJINHO'},
}
RESET = '\033[0m'


def exibir_banner():
    """Exibe o banner do chatbot."""
    print("""
╔══════════════════════════════════════════════════════╗
║           🧠  DIVERTIDA MENTE — CHATBOT  🧠          ║
║                                                      ║
║   Digite um pensamento e veja como cada emoção       ║
║   reage!  Digite 'sair' para encerrar.               ║
╚══════════════════════════════════════════════════════════╝
    """)


def exibir_base_conhecimento():
    """Mostra um resumo da pessoa na base de conhecimento."""
    try:
        with open('base_conhecimento.json', 'r', encoding='utf-8') as f:
            base = json.load(f)
    except FileNotFoundError:
        print("⚠️  base_conhecimento.json não encontrado!")
        return

    p = base['pessoa']
    print(f"📋  Pessoa: {p['nome']}, {p['idade']} anos ({p['aniversario']})")
    print(f"    📍 {p['cidade']}/{p['estado']}")
    print(f"    🎓 {p['curso']} — {p['faculdade']} ({p['semestre']}º semestre)")
    print(f"    🐾 Pet: {p['pet']['nome']} ({p['pet']['raca']})")
    print(f"    🎮 Hobbies: {', '.join(p['hobbies'])}")
    print(f"    😰 Medos: {', '.join(p['medos'])}")
    print()


def carregar_emocoes(filtro=None):
    """
    Carrega os modelos treinados.

    Args:
        filtro: lista de nomes de emoção para carregar, ou None para todas.

    Returns:
        Dict {nome: ModeloEmocao} dos modelos carregados com sucesso.
    """
    modelos = {}
    lista = filtro if filtro else list(EMOCOES.keys())

    for emocao in lista:
        if emocao not in EMOCOES:
            print(f"  ⚠️  '{emocao}' não é uma emoção válida. Pulando...")
            continue
        try:
            modelo = ModeloEmocao(emocao)
            modelo.carregar()
            modelos[emocao] = modelo
            info = EMOCOES[emocao]
            print(f"  ✅ {info['emoji']} {info['nome']} carregada!")
        except FileNotFoundError:
            print(
                f"  ⚠️  {emocao.capitalize()} ainda não treinada "
                f"(treine com: python treinar.py {emocao})"
            )

    return modelos


def chat_loop(modelos, debug=False):
    """Loop principal de interação com o usuário."""
    while True:
        try:
            pensamento = input("\n💭 Pensamento: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Até mais!")
            break

        if not pensamento:
            continue
        if pensamento.lower() in ('sair', 'exit', 'quit'):
            print("\n👋 Até mais!")
            break

        print(f"\n{'─' * 55}")

        for emocao, modelo in modelos.items():
            info = EMOCOES[emocao]
            resposta, tag, confianca = modelo.prever(pensamento)

            linha = f"  {info['cor']}{info['emoji']} {info['nome']}: {resposta}{RESET}"
            print(linha)

            if debug:
                print(f"       [tag: {tag} | confiança: {confianca:.2%}]")

        print(f"{'─' * 55}")


def main():
    parser = argparse.ArgumentParser(description='🧠 Divertida Mente — Chatbot')
    parser.add_argument(
        '--emocao', '-e', type=str, default=None,
        help='Testar apenas uma emoção específica (ex: raiva)',
    )
    parser.add_argument(
        '--debug', '-d', action='store_true',
        help='Exibir tag e confiança de cada predição',
    )
    args = parser.parse_args()

    exibir_banner()

    print("🔄 Carregando emoções...\n")

    filtro = [args.emocao.lower()] if args.emocao else None
    modelos = carregar_emocoes(filtro)

    if not modelos:
        print("\n❌ Nenhuma emoção treinada encontrada!")
        print("   Treine pelo menos uma: python treinar.py <emocao>")
        print(f"   Opções: {', '.join(EMOCOES.keys())}")
        sys.exit(1)

    exibir_base_conhecimento()
    chat_loop(modelos, debug=args.debug)


if __name__ == '__main__':
    main()
