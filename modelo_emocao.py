"""
Classe principal do modelo de emoção.

Cada emoção (raiva, medo, alegria, tristeza, nojinho) é uma instância
de ModeloEmocao que encapsula:
- Construção de rede neural com Keras/TensorFlow
- Treinamento com dados específicos da emoção
- Predição de intenção e geração de resposta
- Integração com a base de conhecimento compartilhada
"""

import os
import sys
import json
import random
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from preprocessamento import (
    preparar_dados,
    texto_para_bow,
    salvar_preprocessamento,
    carregar_preprocessamento,
)

# Garante que prints com caracteres especiais funcionem no Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


class ModeloEmocao:
    """Modelo de classificação de intenção para uma emoção específica."""

    def __init__(self, nome_emocao):
        """
        Args:
            nome_emocao: nome da emoção (ex: 'raiva', 'medo', 'alegria').
        """
        self.nome = nome_emocao
        self.pasta = os.path.join('emocoes', nome_emocao)
        self.modelo = None
        self.vocabulario = None
        self.tags = None
        self.dados_treino = None
        self.base_conhecimento = None

    # ------------------------------------------------------------------ #
    #  Carregamento de dados                                              #
    # ------------------------------------------------------------------ #

    def carregar_dados_treino(self):
        """Carrega o dataset JSON da emoção."""
        caminho = os.path.join(self.pasta, 'dados_treino.json')
        with open(caminho, 'r', encoding='utf-8') as f:
            self.dados_treino = json.load(f)
        return self.dados_treino

    def carregar_base_conhecimento(self):
        """Carrega a base de conhecimento compartilhada."""
        with open('base_conhecimento.json', 'r', encoding='utf-8') as f:
            self.base_conhecimento = json.load(f)
        return self.base_conhecimento

    # ------------------------------------------------------------------ #
    #  Construção e treinamento do modelo                                 #
    # ------------------------------------------------------------------ #

    def construir_modelo(self, tam_entrada, tam_saida):
        """
        Constrói a rede neural sequencial com Keras.

        Arquitetura:
            Input(tam_entrada) -> Dense(128, relu) -> Dropout(0.5)
                               -> Dense(64, relu)  -> Dropout(0.5)
                               -> Dense(tam_saida, softmax)
        """
        self.modelo = keras.Sequential([
            layers.Input(shape=(tam_entrada,)),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(tam_saida, activation='softmax'),
        ])

        self.modelo.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy'],
        )

        return self.modelo

    def treinar(self, epochs=200, batch_size=8):
        """
        Pipeline completo de treinamento:
        1. Carrega dados de treino
        2. Prepara bag-of-words e labels
        3. Constrói e treina o modelo

        Args:
            epochs: número de épocas de treinamento.
            batch_size: tamanho do batch.

        Returns:
            Objeto History do Keras com métricas de treino.
        """
        self.carregar_dados_treino()

        X, y, self.vocabulario, self.tags = preparar_dados(self.dados_treino)

        self.construir_modelo(X.shape[1], y.shape[1])

        print(f"\n{'='*50}")
        print(f"🎭  Treinando emoção: {self.nome.upper()}")
        print(f"📊  Vocabulário: {len(self.vocabulario)} palavras")
        print(f"🏷️   Intenções: {len(self.tags)} tags")
        print(f"📝  Exemplos de treino: {len(X)}")
        print(f"{'='*50}\n")

        historico = self.modelo.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            verbose=1,
        )

        return historico

    # ------------------------------------------------------------------ #
    #  Persistência                                                       #
    # ------------------------------------------------------------------ #

    def salvar(self):
        """Salva o modelo .keras e o pickle de preprocessamento."""
        caminho_modelo = os.path.join(self.pasta, f'modelo_{self.nome}.keras')
        caminho_prep = os.path.join(self.pasta, f'preprocessamento_{self.nome}.pkl')

        self.modelo.save(caminho_modelo)
        salvar_preprocessamento(self.vocabulario, self.tags, caminho_prep)

        print(f"\n✅ Modelo salvo em: {caminho_modelo}")
        print(f"✅ Preprocessamento salvo em: {caminho_prep}")

    def carregar(self):
        """Carrega modelo treinado, preprocessamento e dados."""
        caminho_modelo = os.path.join(self.pasta, f'modelo_{self.nome}.keras')
        caminho_prep = os.path.join(self.pasta, f'preprocessamento_{self.nome}.pkl')

        if not os.path.exists(caminho_modelo):
            raise FileNotFoundError(
                f"Modelo não encontrado: {caminho_modelo}\n"
                f"Treine primeiro com: python treinar.py {self.nome}"
            )

        self.modelo = keras.models.load_model(caminho_modelo)
        self.vocabulario, self.tags = carregar_preprocessamento(caminho_prep)
        self.carregar_dados_treino()
        self.carregar_base_conhecimento()

    # ------------------------------------------------------------------ #
    #  Predição e resposta                                                #
    # ------------------------------------------------------------------ #

    def prever(self, texto):
        """
        Classifica a intenção do texto e retorna uma resposta no tom da emoção.

        Args:
            texto: pensamento digitado pelo usuário.

        Returns:
            Tupla (resposta, tag, confianca).
        """
        bow = texto_para_bow(texto, self.vocabulario)
        resultado = self.modelo.predict(np.array([bow]), verbose=0)[0]

        idx = np.argmax(resultado)
        confianca = float(resultado[idx])
        tag = self.tags[idx]

        # Se a confiança for muito baixa, usa resposta padrão
        if confianca < 0.25:
            return self._resposta_padrao(), tag, confianca

        # Busca resposta na intenção correspondente
        for intencao in self.dados_treino['intencoes']:
            if intencao['tag'] == tag:
                resposta = random.choice(intencao['respostas'])
                resposta = self._inserir_conhecimento(resposta)
                return resposta, tag, confianca

        return self._resposta_padrao(), tag, confianca

    def _resposta_padrao(self):
        """Retorna resposta genérica quando a confiança é baixa."""
        for intencao in self.dados_treino['intencoes']:
            if intencao['tag'] in ('nao_entendi', 'desconhecido', 'padrao'):
                return random.choice(intencao['respostas'])
        return "..."

    def _inserir_conhecimento(self, resposta):
        """
        Substitui placeholders {chave} na resposta por valores da base de
        conhecimento. Exemplo: '{nome}' -> 'Lucas'.
        """
        if self.base_conhecimento is None:
            self.carregar_base_conhecimento()

        pessoa = self.base_conhecimento.get('pessoa', {})

        for chave, valor in pessoa.items():
            placeholder = '{' + chave + '}'
            if placeholder in resposta:
                if isinstance(valor, list):
                    resposta = resposta.replace(
                        placeholder, ', '.join(str(v) for v in valor)
                    )
                elif isinstance(valor, dict):
                    resposta = resposta.replace(
                        placeholder, str(valor.get('nome', valor))
                    )
                else:
                    resposta = resposta.replace(placeholder, str(valor))

        return resposta
