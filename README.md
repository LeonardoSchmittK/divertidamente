1. Definição do problema e intenções
Etapa

Item de verificação

NI

EA

C

Evidência / caminho

1

Problema, público-alvo, objetivos e limites definidos

☐

☐

X

Documento de definição do projeto

1

Pelo menos 3 intenções/categorias e 10 perguntas levantadas

☐

☐

X

Catálogo de intenções e perguntas

3 intenções principais
1. Perspectiva emocional individual: o usuário apresenta um problema pessoal e escolhe uma emoção para receber uma resposta sob aquela perspectiva. Exemplo: felicidade apresenta uma visão otimista e alegre da situação.

2. Interação entre emoções (caos): o usuário apresenta uma situação e permite que diferentes emoções debatam entre si, cada uma defendendo sua própria perspectiva. Exemplo: raiva discorda de tristeza, enquanto felicidade tenta encontrar uma solução positiva.

3. Análise de múltiplas perspectivas: o usuário apresenta um problema e recebe diferentes interpretações individuais de todas as emoções disponíveis, podendo comparar as opiniões e refletir sobre os diferentes pontos de vista.

10 perguntas para levantamento e testes
Nº

Pergunta do usuário

Intenção

1

Estou triste porque briguei com meu melhor amigo. O que devo fazer?

Perspectiva individual

2

Me dê uma visão feliz sobre ter sido rejeitado em uma entrevista.

Perspectiva individual

3

Estou com muita raiva de alguém. Como você reagiria?

Perspectiva individual

4

Tenho medo de começar algo novo. O que você acha?

Perspectiva individual

5

O que cada emoção pensa sobre terminar um relacionamento?

Múltiplas perspectivas

6

Como felicidade, raiva e tristeza reagiriam ao perder um emprego?

Múltiplas perspectivas

7

Quero ver todas as emoções discutindo sobre uma traição.

Interação entre emoções

8

Faça a raiva discutir com a felicidade sobre uma situação injusta.

Interação entre emoções

9

Quero que todas as emoções debatam sobre alguém que mentiu para um amigo.

Interação entre emoções

10

Coloque medo, coragem e raiva para discutir se vale a pena correr um risco.

Interação entre emoções

2. Base de conhecimento e dados
Etapa

Item de verificação

NI

EA

C

Evidência / caminho

2

Base de conhecimento/dataset criada ou curada

☐

X

☐

Dataset de personalidades emocionais

2

Origem e preparação dos dados documentadas

☐

X

☐

Documento de curadoria e preparação

Base de conhecimento proposta
A base de conhecimento deverá conter informações sobre as características de cada emoção, incluindo:

Nome da emoção.

Personalidade e comportamento.

Forma de comunicação.

Tipo de linguagem utilizada.

Maneira de interpretar situações.

Reações comuns diante de diferentes problemas.

Exemplos de respostas condizentes com a emoção.

Emoções iniciais
Felicidade

Alegre, otimista, positiva e entusiasmada.

Criminal law: Loss of self-control | Teaching Resources
 
Raiva

Agressiva, impulsiva, confrontadora e impaciente.

忧忧-快懂百科
 
Tristeza

Melancólica, sensível, pessimista e reflexiva.

inside out concept art Fear | Filme divertidamente, Divertidamente da disney, Divertidamente
 
Medo

Cauteloso, inseguro, desconfiado e preocupado.

How to Draw Disgust from Inside Out 2: Step-by-Step Guide
 
Nojo

Crítico, repulsivo, seletivo e intolerante.

Colorful cartoon surprised expression | Free Photo Illustration - rawpixel
 
Surpresa

Espontânea, curiosa, imprevisível e expressiva.

Origem e preparação dos dados:

Pesquisa sobre características psicológicas e comportamentais das emoções.

Criação de descrições e instruções individuais para cada personalidade.

Elaboração de exemplos de diálogos.

Organização dos dados em categorias para facilitar sua utilização pela IA.

Testes para verificar se as respostas respeitam a personalidade de cada emoção.

3. Arquitetura e funcionamento da IA
Etapa

Item de verificação

NI

EA

C

Evidência / caminho

3

Arquitetura e técnica de IA/PLN justificadas

☐

X

☐

Documento de arquitetura

3

Fluxograma e tratamento de falhas/fallback definidos

☐

X

☐

Fluxograma do sistema

Arquitetura proposta
A aplicação utilizará um modelo de linguagem (LLM) com técnicas de Processamento de Linguagem Natural (PLN), utilizando instruções específicas para controlar o comportamento de cada emoção.

Cada emoção terá um prompt próprio, responsável por definir sua personalidade, linguagem e perspectiva.

Funcionamento:

O usuário envia uma mensagem.

O sistema identifica a intenção do usuário.

A aplicação identifica quais emoções devem participar.

A mensagem é encaminhada às respectivas personalidades.

Cada emoção gera uma resposta de acordo com suas características.

Caso seja uma interação coletiva, as respostas são organizadas em formato de diálogo.

O sistema apresenta o resultado ao usuário.

Fluxograma proposto

mermaid

flowchart TD
    A["Usuário envia mensagem"] --> B["Identificação da intenção"]
    B --> C{"Qual o tipo de interação?"}
    C --> D["Emoção individual"]
    C --> E["Interação entre emoções"]
    C --> F["Múltiplas perspectivas"]
    D --> G["Selecionar personalidade"]
    E --> H["Ativar emoções participantes"]
    F --> I["Ativar todas as emoções"]
    G --> J["Processamento pelo LLM"]
    H --> J
    I --> J
    J --> K{"Resposta válida?"}
    K -->|Sim| L["Apresentar resposta"]
    K -->|Não| M["Tentar novamente ou usar fallback"]
    M --> L
    L --> N["Usuário continua a conversa"]
Tratamento de falhas e fallback
Intenção não identificada: solicitar ao usuário que explique melhor o que deseja.

Resposta fora da personalidade: gerar novamente utilizando as instruções específicas da emoção.

Falha na API: apresentar uma mensagem informando que não foi possível gerar a resposta.

Mensagem vazia: solicitar uma nova mensagem.

Conteúdo inadequado: aplicar filtros de segurança sem eliminar a personalidade emocional.

Falha em uma emoção durante o debate: permitir que as demais continuem e informar que uma personalidade não conseguiu responder.

4. Desenvolvimento e implementação
Etapa

Item de verificação

NI

EA

C

Evidência / caminho

4

Código/interface ou protótipo executável

☐

X

☐

Repositório do projeto ou protótipo

4

Mecanismo próprio de IA/PLN identificado no código

☐

X

☐

Código de identificação de intenção e gerenciamento de emoções

Funcionalidades previstas
Interface de conversa com o usuário.

Seleção de emoções individuais.

Modo de interação coletiva entre emoções.

Modo de análise com múltiplas perspectivas.

Personalidades independentes para cada emoção.

Histórico de conversas.

Identificação da intenção do usuário.

Gerenciamento das respostas e interações entre emoções.

Mecanismo próprio de IA/PLN
O diferencial do projeto será o mecanismo de gerenciamento de personalidades emocionais.

Esse mecanismo será responsável por:

Identificar a intenção da mensagem.

Selecionar as emoções adequadas.

Aplicar os prompts correspondentes.

Controlar a ordem de participação das emoções.

Organizar os diálogos entre elas.

Verificar se as respostas estão coerentes com suas personalidades.

Assim, o projeto não será apenas uma interface conectada a um chatbot, mas contará com uma lógica própria para gerenciar as diferentes perspectivas emocionais.

5. Testes e validação
Etapa

Item de verificação

NI

EA

C

Evidência / caminho

5

Casos de teste preparados (meta final: 20 ou mais)

☐

X

☐

Plano de testes

5

Resultados, erros e métricas registrados (se já aplicável)

X

☐

☐

Relatório de testes e validação

Casos de teste propostos
Nº

Cenário de teste

Resultado esperado

1

Pedir uma perspectiva feliz sobre uma demissão

Resposta otimista

2

Pedir uma perspectiva triste sobre uma rejeição

Resposta melancólica

3

Pedir uma perspectiva raivosa sobre uma injustiça

Resposta confrontadora

4

Pedir uma perspectiva de medo sobre uma mudança

Resposta cautelosa

5

Pedir uma perspectiva de nojo sobre uma atitude desagradável

Resposta de repulsa

6

Pedir uma perspectiva surpresa sobre uma notícia inesperada

Resposta espontânea

7

Colocar felicidade e tristeza para debater

Diálogo com opiniões diferentes

8

Colocar raiva e medo para debater

Conflito entre confronto e cautela

9

Colocar todas as emoções para debater

Participação de todas

10

Apresentar um problema de relacionamento

Identificação correta da intenção

11

Enviar uma mensagem sem contexto

Solicitação de esclarecimento

12

Enviar uma mensagem vazia

Solicitação de nova mensagem

13

Pedir uma análise de várias emoções

Respostas individuais

14

Solicitar que felicidade responda de forma agressiva

Manutenção da personalidade feliz

15

Solicitar que raiva responda de maneira excessivamente gentil

Manutenção da personalidade raivosa

16

Apresentar uma situação hipotética

Interpretação adequada

17

Enviar uma mensagem com mais de um problema

Identificação do contexto

18

Interromper uma interação coletiva com nova mensagem

Adaptação da conversa

19

Simular falha na comunicação com a API

Acionamento do fallback

20

Solicitar que as emoções cheguem a uma conclusão

Síntese das diferentes perspectivas

Métricas para avaliar os resultados
Métrica

O que será avaliado

Coerência emocional

Se a resposta corresponde à emoção escolhida

Identificação de intenção

Se o sistema identifica corretamente o que o usuário deseja

Diversidade de perspectivas

Se as emoções apresentam opiniões realmente diferentes

Qualidade da interação

Se os diálogos entre emoções são naturais e interessantes

Taxa de sucesso

Quantidade de testes executados corretamente

Tempo de resposta

Tempo necessário para gerar as respostas
