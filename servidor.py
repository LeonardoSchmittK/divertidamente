"""
API Flask para integrar o frontend React (Vite) com os modelos Keras/TensorFlow.

Execução:
    python servidor.py
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from modelo_emocao import ModeloEmocao

app = Flask(__name__)
CORS(app)

EMOCOES_LIST = ['raiva', 'alegria', 'tristeza', 'nojinho', 'medo']
modelos = {}

# Tenta carregar todos os modelos já disponíveis
for nome in EMOCOES_LIST:
    try:
        m = ModeloEmocao(nome)
        m.carregar()
        modelos[nome] = m
        print(f"✅ Modelo '{nome}' carregado com sucesso!")
    except Exception as e:
        print(f"⏳ Modelo '{nome}' ainda não disponível: {e}")

@app.route('/api/pensamento/emocao/<nome>', methods=['POST'])
def processar_emocao_individual(nome):
    """
    Recebe um pensamento e devolve a resposta de UMA emoção específica.
    Permite ao front consultar as emoções de forma assíncrona/independente,
    fazendo com que cada bot reaja no seu próprio tempo!
    """
    nome = nome.lower()
    if nome not in EMOCOES_LIST:
        return jsonify({'error': f"Emoção '{nome}' inválida"}), 400

    data = request.get_json() or {}
    pensamento = data.get('pensamento', '').strip()

    if not pensamento:
        return jsonify({'error': 'Pensamento vazio'}), 400

    if nome in modelos:
        resposta, tag, confianca = modelos[nome].prever(pensamento)
        return jsonify({
            'emocao': nome,
            'texto': resposta,
            'tag': tag,
            'confianca': float(confianca),
            'treinado': True
        })
    else:
        # Placeholder enquanto o colega responsável não treina
        placeholders = {
            'alegria': 'Ei, não desanima! Vamos focar nas coisas boas e encontrar uma saída alegre pra isso! ✨',
            'tristeza': 'Eu entendo como você se sente... o peito fica apertado e parece que nada faz sentido... 💧',
            'nojinho': 'Ai, por favor né? Essa atitude não combina nada com o Lucas. Melhore! 💅',
            'medo': 'AI MEU DEUS! Respira fundo! E se isso for perigoso demais?! Tem certeza?! ⚡'
        }
        return jsonify({
            'emocao': nome,
            'texto': f"[{nome.upper()} - Aguardando treino do colega]: {placeholders.get(nome, '...')}",
            'tag': 'em_desenvolvimento',
            'confianca': 0.0,
            'treinado': False
        })

def listar_emocoes():
    """Retorna o status dos modelos treinados."""
    return jsonify({
        nome: (nome in modelos)
        for nome in EMOCOES_LIST
    })

@app.route('/api/pensamento', methods=['POST'])
def processar_pensamento():
    """Recebe um pensamento e devolve as respostas de cada emoção."""
    data = request.get_json() or {}
    pensamento = data.get('pensamento', '').strip()

    if not pensamento:
        return jsonify({'error': 'Pensamento vazio'}), 400

    respostas = {}

    for nome in EMOCOES_LIST:
        if nome in modelos:
            resposta, tag, confianca = modelos[nome].prever(pensamento)
            respostas[nome] = {
                'texto': resposta,
                'tag': tag,
                'confianca': float(confianca)
            }
        else:
            # Resposta temporária enquanto o colega não finaliza o treino
            placeholders = {
                'alegria': 'Não desanime! Vai dar tudo certo se a gente mantiver o otimismo!',
                'tristeza': 'Eu sinto muito por isso... é realmente difícil aguentar às vezes.',
                'nojinho': 'Sério? Mas que ideia mais sem noção...',
                'medo': 'Ai caramba, tem certeza disso? E se der tudo errado?!'
            }
            respostas[nome] = {
                'texto': f"[{nome.upper()} - Aguardando treino do integrante]: {placeholders.get(nome, '...')}",
                'tag': 'pendente',
                'confianca': 0.0
            }

    return jsonify({
        'pensamento': pensamento,
        'timestamp': datetime.now().strftime('%H:%M'),
        'respostas': respostas
    })

if __name__ == '__main__':
    print("\n🚀 Servidor Divertida Mente rodando em http://127.0.0.1:5000\n")
    app.run(port=5000, debug=False)
