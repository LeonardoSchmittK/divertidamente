"""
Módulo de pré-processamento de texto.

Responsável por:
- Limpeza e tokenização de texto em português
- Criação de vocabulário
- Conversão de texto para Bag of Words (BoW)
- Preparação dos dados para treinamento (X e y)
- Serialização do vocabulário e tags
"""

import re
import pickle
import numpy as np


def limpar_texto(texto):
    """Remove pontuação e converte para minúsculo, preservando acentos."""
    texto = texto.lower().strip()
    # Remove tudo que não seja letra (incluindo acentuadas), número ou espaço
    texto = re.sub(r'[^\w\sáàâãéèêíïóôõúüç]', '', texto)
    # Colapsa espaços múltiplos
    texto = re.sub(r'\s+', ' ', texto)
    return texto


def tokenizar(texto):
    """Divide o texto limpo em uma lista de tokens (palavras)."""
    return limpar_texto(texto).split()


def criar_vocabulario(dados_treino):
    """
    Cria um vocabulário ordenado a partir de todos os padrões de treino.

    Args:
        dados_treino: dict com chave 'intencoes', cada uma contendo 'padroes'.

    Returns:
        Lista ordenada de palavras únicas.
    """
    vocabulario = set()
    for intencao in dados_treino['intencoes']:
        for padrao in intencao['padroes']:
            tokens = tokenizar(padrao)
            vocabulario.update(tokens)
    return sorted(list(vocabulario))


def texto_para_bow(texto, vocabulario):
    """
    Converte um texto em um vetor Bag of Words binário.

    Args:
        texto: string de entrada.
        vocabulario: lista ordenada de palavras conhecidas.

    Returns:
        np.array de 0s e 1s com tamanho len(vocabulario).
    """
    tokens = tokenizar(texto)
    bow = np.zeros(len(vocabulario), dtype=np.float32)
    for token in tokens:
        if token in vocabulario:
            idx = vocabulario.index(token)
            bow[idx] = 1.0
    return bow


def preparar_dados(dados_treino):
    """
    Prepara os arrays X (Bag of Words) e y (one-hot das tags) para treino.

    Args:
        dados_treino: dict com chave 'intencoes'.

    Returns:
        Tupla (X, y, vocabulario, tags):
        - X: np.array shape (n_exemplos, tam_vocabulario)
        - y: np.array shape (n_exemplos, n_tags)
        - vocabulario: lista de palavras
        - tags: lista de tags de intenção
    """
    vocabulario = criar_vocabulario(dados_treino)
    tags = [intencao['tag'] for intencao in dados_treino['intencoes']]

    X = []
    y = []

    for intencao in dados_treino['intencoes']:
        tag_idx = tags.index(intencao['tag'])
        for padrao in intencao['padroes']:
            bow = texto_para_bow(padrao, vocabulario)
            X.append(bow)

            label = np.zeros(len(tags), dtype=np.float32)
            label[tag_idx] = 1.0
            y.append(label)

    return np.array(X), np.array(y), vocabulario, tags


def salvar_preprocessamento(vocabulario, tags, caminho):
    """Serializa vocabulário e tags em um arquivo pickle."""
    dados = {'vocabulario': vocabulario, 'tags': tags}
    with open(caminho, 'wb') as f:
        pickle.dump(dados, f)


def carregar_preprocessamento(caminho):
    """Carrega vocabulário e tags de um arquivo pickle."""
    with open(caminho, 'rb') as f:
        dados = pickle.load(f)
    return dados['vocabulario'], dados['tags']
