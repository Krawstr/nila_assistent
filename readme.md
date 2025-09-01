# Nila - Sua Assistente de Carreira com IA

Nila é uma assistente de carreira inteligente e interativa, projetada para responder às suas perguntas sobre desenvolvimento profissional. Utilizando um sofisticado sistema multi-agente construído com CrewAI, Nila pode fornecer informações sobre salários, planos de carreira e tendências de mercado. A aplicação possui uma interface de chat amigável para uma experiência de usuário fluida e envolvente.

## Índice

- [Funcionalidades](#funcionalidades)
- [Como Funciona](#como-funciona)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Começar](#como-começar)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalação](#instalação)
  - [Configuração](#configuração)
  - [Executando a Aplicação](#executando-a-aplicação)
- [Análise Técnica Detalhada](#análise-técnica-detalhada)
  - [Frontend](#frontend)
  - [Backend](#backend)
  - [A Equipe de IA (Crew)](#a-equipe-de-ia-crew)
- [Customização](#customização)

## Funcionalidades

* **Interface de Chat Interativa:** Uma interface de chat limpa e intuitiva para os usuários fazerem perguntas relacionadas à carreira.
* **Sistema de IA Multi-Agente:** Impulsionado pelo CrewAI, a aplicação utiliza uma equipe de agentes de IA especializados para lidar com as consultas dos usuários.
* **Capacidade de Pesquisa na Web:** Um dos agentes de IA é equipado com a ferramenta de busca DuckDuckGo para encontrar informações atualizadas na internet.
* **Geração Aumentada por Recuperação (RAG):** O sistema inclui um agente com uma ferramenta RAG para consultar um banco de dados vetorial especializado em busca de conhecimento interno ou de domínio específico.
* **Processamento de Tarefas Assíncrono:** As solicitações dos usuários são processadas em segundo plano, permitindo uma experiência de usuário sem bloqueios. O frontend consulta os resultados até que a equipe de IA conclua sua tarefa.
* **Arquitetura Escalável:** A separação entre frontend, backend e a lógica de IA permite o desenvolvimento e a escalabilidade independentes de cada componente.

## Como Funciona

1.  **Interação do Usuário:** O usuário digita uma pergunta relacionada à carreira na interface de chat e clica em "enviar".
2.  **Requisição à API:** O frontend envia a pergunta do usuário para o backend Flask através de uma requisição POST para o endpoint `/run_crew`.
3.  **Criação da Tarefa:** O backend cria um ID de tarefa único para a requisição e inicia uma nova thread para executar a equipe de agentes de IA. Isso garante que o servidor web permaneça responsivo.
4.  **Início da Equipe de IA:** A `AgentsCrew` é instanciada e o método `kickoff` é chamado com o tópico do usuário como entrada.
5.  **Colaboração dos Agentes:**
    * **Nila (A Guia de Carreira):** A agente principal que primeiro analisa a pergunta do usuário.
    * **Raga (O Recuperador de Dados):** Se necessário, Nila delega a tarefa de encontrar dados específicos para Raga. Raga usa sua `rag_search_tool` para consultar um banco de dados vetorial local. Nila também pode usar sua própria `DuckDuckGoSearchTool` para pesquisas mais amplas na web.
    * **Geração do Relatório Final:** Assim que todas as informações necessárias são coletadas, Nila compila um relatório final abrangente.
6.  **Polling de Resultados:** Enquanto a equipe de IA está trabalhando, o frontend envia periodicamente requisições GET para o endpoint `/get_result/<task_id>` para verificar o status da tarefa.
7.  **Exibição da Resposta:** Quando a tarefa é concluída, o backend retorna o resultado final, que é então exibido na interface de chat.

## Estrutura do Projeto

```
├── app.py                  
├── crew.py                 
├── rag_agent.py            
├── config/
│   ├── agents.yaml          
│   ├── tasks.yaml 
├── tools/
│   ├── init.py
│   ├── duck_search.py      
│   └── rag_tool.py         
├── agents/
│   ├── init.py
│   └── rag_agent.py        
├── templates/
│   └── index.html         
├── static/
│   ├── css/
│   │   └── style.css       
│   └── js/
│       └── script.js      
└── database/           
```

## Como Começar

### Pré-requisitos

* Python 3.8 ou superior
* pip
* Uma chave de API do Google AI

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-seu-repositorio>
    cd <nome-do-seu-repositorio>
    ```

2.  **Instale os pacotes Python necessários:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Nota: Um arquivo `requirements.txt` precisaria ser criado a partir das bibliotecas importadas.)*

### Configuração

1.  **Crie um arquivo `.env`** na raiz do diretório do projeto.
2.  **Adicione sua chave de API do Google AI** ao arquivo `.env`:
    ```
    GOOGLE_API_KEY="sua_chave_de_api_do_google"
    GEMINI_API_KEY="sua_chave_de_api_do_google" 
    ```

    OBS: No projeto utilizei a API do Gemini. Porém, caso você esteja utilizando a versão gratuita, recomendo optar por ferramentas e tecnologias como o Ollama (pretendo migrar o projeto para o Ollama no futuro).

### Executando a Aplicação

1.  **Inicie o servidor de desenvolvimento Flask:**
    ```bash
    python app.py
    ```

2.  **Abra seu navegador** e acesse `http://127.0.0.1:5000`.

## Análise Técnica Detalhada

### Frontend

O frontend é construído com HTML, CSS e JavaScript padrão.

* **`index.html`:** Fornece a estrutura básica da interface de chat, incluindo a área de exibição de mensagens e o formulário de entrada do usuário.
* **`style.css`:** Define a aparência visual da aplicação, com um design moderno e limpo.
* **`script.js`:** Gerencia toda a lógica do lado do cliente:
    * Captura a entrada do usuário.
    * Envia requisições para o backend.
    * Realiza o polling para obter os resultados.
    * Atualiza dinamicamente o chat com novas mensagens.

### Backend

O backend é uma aplicação web Flask.

* **`app.py`:**
    * **`/`:** Renderiza a página principal do chat (`index.html`).
    * **`/run_crew` (POST):** Recebe a pergunta do usuário, cria um ID de tarefa único e inicia uma thread em segundo plano para executar a equipe do CrewAI. Retorna imediatamente uma resposta `202 Accepted` com o `task_id`.
    * **`/get_result/<task_id>` (GET):** Permite que o frontend verifique o status de uma tarefa. Retornará "pending" até que a equipe de IA termine, momento em que retornará o resultado final.

### A Equipe de IA (Crew)

O núcleo da inteligência da aplicação reside no `crew.py`.

* **Classe `AgentsCrew`:** Esta classe, construída sobre a `CrewBase` do CrewAI, define os agentes e as tarefas.
* **Agentes:**
    * **`nila`:** A agente principal que interage com a consulta do usuário. Ela tem acesso à ferramenta de busca DuckDuckGo.
    * **`raga`:** Uma agente especializada em recuperar informações do banco de dados vetorial local usando a ferramenta RAG.
* **Tarefas:**
    * **`nila_career_guide`:** A tarefa inicial onde Nila analisa a solicitação do usuário.
    * **`raga_data_retrieval`:** Esta tarefa depende da saída de `nila_career_guide` e envolve Raga buscando dados específicos.
    * **`nila_final_report`:** A tarefa final onde Nila sintetiza todas as informações coletadas em uma resposta coerente.
* **Processo:** A equipe opera de maneira `Process.sequential`, garantindo um fluxo lógico de informações de uma tarefa para a outra.

## Customização

* **Alterar o Modelo de IA:** Você pode facilmente trocar o modelo `gemini-2.0-flash` no `crew.py` por qualquer outro modelo suportado pela configuração de LLM do CrewAI.
* **Adicionar Mais Agentes:** Você pode definir novos agentes com diferentes papéis, histórias e ferramentas no `crew.py` para expandir as capacidades do seu assistente.
* **Criar Novas Ferramentas:** Desenvolva ferramentas personalizadas no diretório `tools/` para dar aos seus agentes novas habilidades, como interagir com outras APIs ou bancos de dados.
* **Expandir a Base de Conhecimento:** Para melhorar as respostas do agente RAG, você pode adicionar mais documentos ao banco de dados vetorial Chroma localizado no diretório `database/`.
