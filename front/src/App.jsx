import React, { useState } from 'react';
import './App.css';

// 5 Emoções distribuídas geometricamente em volta do centro
// Raio circular / elíptico: alegria (topo), tristeza (topo-esq), raiva (baixo-esq), medo (baixo-dir), nojinho (topo-dir)
const EMOCOES = [
  {
    id: 'alegria',
    nome: 'Alegria',
    cor: '#e5a500',
    icone: '/emocoes/alegria.png',
    posicao: 'top',
    flutuarAnim: 'flutuar-1',
    delayMin: 600,
    delayMax: 1000
  },
  {
    id: 'nojinho',
    nome: 'Nojinho',
    cor: '#1fad42',
    icone: '/emocoes/nojinho.png',
    posicao: 'top-right',
    flutuarAnim: 'flutuar-2',
    delayMin: 900,
    delayMax: 1400
  },
  {
    id: 'medo',
    nome: 'Medo',
    cor: '#8a3fd9',
    icone: '/emocoes/medo.png',
    posicao: 'bottom-right',
    flutuarAnim: 'flutuar-3',
    delayMin: 1200,
    delayMax: 1800
  },
  {
    id: 'raiva',
    nome: 'Raiva',
    cor: '#d92521',
    icone: '/emocoes/raiva.png',
    posicao: 'bottom-left',
    flutuarAnim: 'flutuar-4',
    delayMin: 200,
    delayMax: 450
  },
  {
    id: 'tristeza',
    nome: 'Tristeza',
    cor: '#1f6fc9',
    icone: '/emocoes/tristeza.png',
    posicao: 'top-left',
    flutuarAnim: 'flutuar-5',
    delayMin: 1400,
    delayMax: 2200
  }
];

// Memórias da base de conhecimento representadas pelas esferas coloridas
const ESFERAS_MEMORIA = [
  { id: 1, fato: "Nome: Lucas", cor: "#ffd000", brilho: "rgba(255, 208, 0, 0.4)", top: "12%", left: "28%", size: 26 },
  { id: 2, fato: "Nasceu em 15 de dezembro", cor: "#ffd000", brilho: "rgba(255, 208, 0, 0.35)", top: "34%", left: "10%", size: 22 },
  { id: 3, fato: "Mora em Florianópolis/SC", cor: "#2a75d3", brilho: "rgba(42, 117, 211, 0.4)", top: "75%", left: "14%", size: 28 },
  { id: 4, fato: "Ciência da Computação na Unisul", cor: "#2a75d3", brilho: "rgba(42, 117, 211, 0.35)", top: "84%", left: "32%", size: 30 },
  { id: 5, fato: "Medo terrível de aranha", cor: "#9b51e0", brilho: "rgba(155, 81, 224, 0.4)", top: "68%", left: "76%", size: 24 },
  { id: 6, fato: "Tem medo de altura e escuro", cor: "#9b51e0", brilho: "rgba(155, 81, 224, 0.35)", top: "85%", left: "62%", size: 22 },
  { id: 7, fato: "Comida favorita: Lasanha", cor: "#e52521", brilho: "rgba(229, 37, 33, 0.4)", top: "62%", left: "36%", size: 24 },
  { id: 8, fato: "Odeia comer jiló", cor: "#2bb64a", brilho: "rgba(43, 182, 74, 0.4)", top: "25%", left: "70%", size: 26 },
  { id: 9, fato: "Matéria favorita: Geografia", cor: "#ffd000", brilho: "rgba(255, 208, 0, 0.35)", top: "14%", left: "68%", size: 24 },
  { id: 10, fato: "Cachorro: Thor (Golden)", cor: "#ffd000", brilho: "rgba(255, 208, 0, 0.4)", top: "30%", left: "84%", size: 28 },
  { id: 11, fato: "Quase se afogou quando criança", cor: "#2a75d3", brilho: "rgba(42, 117, 211, 0.4)", top: "45%", left: "16%", size: 24 },
  { id: 12, fato: "Sonho de viajar o mundo", cor: "#ffd000", brilho: "rgba(255, 208, 0, 0.35)", top: "46%", left: "82%", size: 26 }
];

export default function App() {
  const [pensamento, setPensamento] = useState('');
  const [ultimoPensamento, setUltimoPensamento] = useState('');
  const [respostas, setRespostas] = useState({});
  const [enviando, setEnviando] = useState(false);
  const [modoChat, setModoChat] = useState(false);
  const [historicoChat, setHistoricoChat] = useState([]);

  const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  const enviarPensamento = async (e) => {
    e.preventDefault();
    if (!pensamento.trim()) return;

    const texto = pensamento.trim();
    const idMsg = Date.now();
    const hora = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    setUltimoPensamento(texto);
    setPensamento('');
    setEnviando(true);

    // Registra a mensagem do usuário no histórico do modo chat
    setHistoricoChat((prev) => [
      ...prev,
      { id: idMsg, autor: 'voce', texto, hora }
    ]);

    // Inicializa todos com status "digitando"
    const estadoInicial = {};
    EMOCOES.forEach((emo) => {
      estadoInicial[emo.id] = { status: 'digitando' };
    });
    setRespostas(estadoInicial);

    // Cada emoção responde de forma autônoma e em tempos diferentes
    const promises = EMOCOES.map(async (emo) => {
      const tempo = emo.delayMin + Math.random() * (emo.delayMax - emo.delayMin);
      await delay(tempo);

      let textoResposta = '';

      try {
        const res = await fetch(`/api/pensamento/emocao/${emo.id}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ pensamento: texto })
        });

        if (res.ok) {
          const dados = await res.json();
          textoResposta = dados.texto;
        } else {
          throw new Error('API offline');
        }
      } catch {
        // Fallback para demonstração sem backend ativo
        const fallback = {
          raiva: texto.toLowerCase().includes('pular') || texto.toLowerCase().includes('desistir')
            ? 'Pular?! Desistir?! TÁ MALUCO?! Levanta essa cabeça e enfrenta! Tu já passou no vestibular de primeira, esqueceu?!'
            : 'Para de moleza e resolve isso logo!',
          alegria: 'Não desanima! Vamos ver o lado positivo e encontrar uma saída legal!',
          tristeza: 'Eu entendo você... às vezes tudo parece pesado e sem sentido.',
          nojinho: 'Sério mesmo? Mas que pensamento mais sem graça e de mau gosto.',
          medo: 'AI NÃO! E se der tudo errado?! Cuidado, pensa bem antes de fazer isso!'
        };
        textoResposta = fallback[emo.id] || '...';
      }

      // Atualiza o estado circular
      setRespostas((prev) => ({
        ...prev,
        [emo.id]: {
          status: 'pronto',
          texto: textoResposta
        }
      }));

      // Adiciona a fala individual do bot na timeline sequencial do modo chat
      setHistoricoChat((prev) => [
        ...prev,
        {
          id: `${idMsg}-${emo.id}`,
          autor: emo.id,
          nome: emo.nome,
          cor: emo.cor,
          icone: emo.icone,
          texto: textoResposta,
          hora: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    });

    await Promise.all(promises);
    setEnviando(false);
  };

  return (
    <div className={`canvas ${modoChat ? 'modo-chat-ativo' : ''}`}>
      {/* TOGGLE NO CANTO DA TELA (MINIMALISTA) */}
      <div className="toggle-container">
        <button
          type="button"
          className="toggle-btn"
          onClick={() => setModoChat(!modoChat)}
          title="Alternar entre Sala Orbital e Chat Linear"
        >
          <span className="toggle-icone">{modoChat ? '◯' : '≡'}</span>
          <span className="toggle-texto">{modoChat ? 'Visão Orbital' : 'Modo Chat'}</span>
        </button>
      </div>

      {/* ESFERAS DE MEMÓRIA (BASE DE CONHECIMENTO) */}
      {!modoChat && (
        <div className="memoria-layer">
          {ESFERAS_MEMORIA.map((esfera) => (
            <div
              key={esfera.id}
              className="esfera-orb"
              style={{
                top: esfera.top,
                left: esfera.left,
                width: `${esfera.size}px`,
                height: `${esfera.size}px`,
                '--orb-cor': esfera.cor,
                '--orb-glow': esfera.brilho
              }}
            >
              <div className="esfera-brilho-interno"></div>
              {/* Tooltip com o fato da base de conhecimento no hover */}
              <div className="esfera-tooltip">
                <span className="tooltip-tag">MEMÓRIA</span>
                <span className="tooltip-fato">{esfera.fato}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {modoChat ? (
        /* LAYOUT 2: CONVERSA DE CHAT SEQUENCIAL (UM EMBAIXO DO OUTRO) */
        <div className="chat-layout">
          <div className="chat-mensagens">
            {historicoChat.length === 0 ? (
              <div className="chat-vazio">
                <p>Nenhuma mensagem ainda.</p>
                <span>Digite um pensamento abaixo para iniciar a conversa.</span>
              </div>
            ) : (
              historicoChat.map((msg) => {
                const isVoce = msg.autor === 'voce';
                return (
                  <div
                    key={msg.id}
                    className={`chat-item ${isVoce ? 'item-voce' : 'item-bot'}`}
                  >
                    {!isVoce && (
                      <img src={msg.icone} alt={msg.nome} className="chat-avatar" />
                    )}
                    <div className="chat-balao-wrap">
                      {!isVoce && (
                        <span className="chat-autor" style={{ color: msg.cor }}>
                          {msg.nome}
                        </span>
                      )}
                      <div
                        className="chat-balao"
                        style={{
                          borderColor: isVoce ? '#e0e0e0' : msg.cor
                        }}
                      >
                        <p>{msg.texto}</p>
                      </div>
                      <span className="chat-hora">{msg.hora}</span>
                    </div>
                  </div>
                );
              })
            )}
          </div>

          <form onSubmit={enviarPensamento} className="chat-form">
            <input
              type="text"
              className="chat-input"
              placeholder="Digite seu pensamento..."
              value={pensamento}
              onChange={(e) => setPensamento(e.target.value)}
              autoFocus
            />
          </form>
        </div>
      ) : (
        /* LAYOUT 1: ÓRBITA CIRCULAR COM BOTS FLUTUANDO */
        <>
          {EMOCOES.map((emo) => {
            const resp = respostas[emo.id];
            const temResposta = resp && resp.status === 'pronto';
            const isDigitando = resp && resp.status === 'digitando';

            return (
              <div key={emo.id} className={`node-bot node-${emo.posicao} ${emo.flutuarAnim}`}>
                {/* Balão de fala minimalista */}
                {(temResposta || isDigitando) && (
                  <div
                    className="fala-balao"
                    style={{
                      '--cor-emocao': emo.cor
                    }}
                  >
                    {isDigitando ? (
                      <div className="digitando">
                        <span style={{ backgroundColor: emo.cor }}></span>
                        <span style={{ backgroundColor: emo.cor }}></span>
                        <span style={{ backgroundColor: emo.cor }}></span>
                      </div>
                    ) : (
                      <p className="texto-fala">{resp.texto}</p>
                    )}
                  </div>
                )}

                {/* Imagem do Bot sem camadas */}
                <div className="bot-avatar-wrap">
                  <img
                    src={emo.icone}
                    alt={emo.nome}
                    className={`bot-avatar ${temResposta ? 'falando' : ''}`}
                  />
                  <span className="bot-label" style={{ color: emo.cor }}>
                    {emo.nome}
                  </span>
                </div>
              </div>
            );
          })}

          {/* CENTRO: INPUT MINIMALISTA */}
          <div className="centro-container">
            {ultimoPensamento && (
              <p className="ultimo-pensamento">"{ultimoPensamento}"</p>
            )}

            <form onSubmit={enviarPensamento} className="form-pensamento">
              <input
                type="text"
                className="input-pensamento"
                placeholder="O que está pensando agora?"
                value={pensamento}
                onChange={(e) => setPensamento(e.target.value)}
                autoFocus
              />
            </form>

            <span className="instrucao-tecla">Pressione Enter para pensar</span>
          </div>
        </>
      )}
    </div>
  );
}
