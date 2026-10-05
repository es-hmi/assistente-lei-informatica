# 🤖 Assistente Virtual & Gerenciador da Lei de Informática (RAG)

> **MVP de Inteligência Artificial Generativa e Engenharia de Software**  
> Aplicação conversacional desenvolvida com **Streamlit** e **Arquitetura RAG (Retrieval-Augmented Generation)** local para consulta, análise e gestão de documentos da **Lei de Informática (Lei nº 8.248/1991 e Lei nº 13.969/2019)** e do **Manual de Análise do RDA**.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Tests](https://img.shields.io/badge/pytest-passing-brightgreen.svg)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 1. Visão Geral do Projeto

O **Assistente Virtual da Lei de Informática** é um protótipo funcional (MVP) projetado para auxiliar empresas, auditores independentes e analistas na interpretação dos requisitos de **Pesquisa, Desenvolvimento e Inovação (PD&I)** e no enquadramento do **Relatório Demonstrativo Anual (RDA)**.

A aplicação combina uma **interface interativa em Streamlit** com uma arquitetura **RAG local**, permitindo:
- **Consultas em Linguagem Natural**: Perguntas sobre conceitos, enquadramentos e regras da Lei de Informática.
- **RAG Grounded (Zero Alucinação)**: Respostas baseadas estritamente nos documentos ativos carregados na memória.
- **Gestão Completa da Base de Conhecimento**: Upload dinâmico de novos arquivos (`.pdf` e `.txt`) e exclusão individual de documentos via interface.
- **Diagnóstico Transparente da Memória**: Contador visual em tempo real do total de caracteres carregados e status da base ativa.

---

## 📖 2. Entendendo o RAG Grounded e a Prevenção de Alucinações

Para garantir total clareza técnica e transparência a auditores, avaliadores e usuários da aplicação:

* **RAG Grounded (RAG Ancorado)**:  
  A arquitetura RAG (*Retrieval-Augmented Generation*) realiza a busca de informações em uma base documental para responder a dúvidas. O termo **Grounded (Ancorado)** significa que o sistema responde **estritamente com base nos dados recuperados** das fontes oficiais carregadas (`docs/`). Se a informação não constar na base ativa, o sistema informa que não encontrou o dado, evitando respostas inventadas ou baseadas em conhecimento externo.

* **Zero Alucinação (Recuperação Literal e Auditável)**:  
  Em projetos de IA, "alucinação" é quando o modelo gera respostas plausíveis, porém falsas. Neste MVP, a busca local extrai e apresenta **diretamente os parágrafos literais e originais** dos manuais oficiais da Lei de Informática e do RDA. Por adotar uma recuperação determinística do texto oficial (sem reescrita probabilística por API externa nesta fase do MVP), **garante-se 100% de fidelidade ao texto legal, zero custo financeiro e total auditabilidade das respostas**.

---

## 🏗️ 3. Arquitetura e Estrutura do Repositório

### Tecnologias Utilizadas
- **Linguagem**: Python 3.10+
- **Interface Web**: Streamlit
- **Leitura de Documentos**: PyPDF (`pypdf`)
- **Testes Automatizados**: Pytest
- **Controle de Versão**: Git & GitHub (Conventional Commits)

### Estrutura do Projeto
```text
assistente-lei-informatica/
├── app.py               # Aplicação principal (Streamlit + Lógica RAG + UI + Exclusão)
├── test_app.py          # Testes unitários automatizados (Pytest)
├── requirements.txt     # Gestão de dependências do projeto
├── .gitignore           # Regras de omissão de arquivos temporários e virtuais
├── .env.example         # Modelo de configuração de variáveis de ambiente
├── Makefile             # Atalhos de automação (install, run, test)
├── LICENSE              # Licença aberta MIT
└── docs/                # Diretório local da base de conhecimento (PDFs e TXTs)
🚀 4. Instruções de Instalação e Execução
Pré-requisitos
Python 3.10 ou superior instalado.
Git instalado.
Passo a Passo
Clonar o Repositório:
git clone https://github.com/es-hmi/assistente-lei-informatica.git
cd assistente-lei-informatica
Criar e Ativar o Ambiente Virtual:
Windows (PowerShell):
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Linux/macOS:
python3 -m venv .venv
source .venv/bin/activate
Instalar as Dependências:
pip install -r requirements.txt
Executar a Aplicação Streamlit:
streamlit run app.py
Acesse a aplicação no seu navegador em http://localhost:8501.
Executar os Testes Automatizados:
pytest
🧠 5. Storytelling da IA: O Papel da IA Generativa no Desenvolvimento
Ganhos de Produtividade
A Inteligência Artificial Generativa atuou como um co-piloto de engenharia de software ao longo de todo o ciclo de desenvolvimento do MVP:
Aceleração de Código Boilerplate: Geração rápida dos componentes de interface no Streamlit (st.sidebar, st.file_uploader, colunas e botões de exclusão).
Automação de Testes Unitários: Criação da suíte de testes com pytest para validação da leitura de arquivos e geração do contexto RAG.
Documentação e Padronização: Estruturação das mensagens de commit no padrão Conventional Commits e redação de documentação técnica.
Desafios Encontrados e Soluções Engenheiradas
Tratamento Inteligente de Siglas Críticas (RDA, P&D, PPB):
Desafio: O algoritmo inicial do RAG descartava palavras curtas (com menos de 4 letras). Isso fazia com que buscas por siglas essenciais como RDA, P&D, TIC e PPB retornassem vazias.
Solução: Refinamento da lógica no app.py, adicionando remoção inteligente de stopwords e aceitação de siglas técnicas com 2 ou mais caracteres.
Filtragem de Ruídos do Documento (Sumários e Capas):
Desafio: A busca por correspondência de linhas capturava índices/sumários repletos de pontos (........), que pontuavam alto por conterem palavras-chave, mas não explicavam os conceitos.
Solução: Implementação de filtro determinístico que ignora blocos contendo pontuação repetida de sumário e divisão do documento em parágrafos completos (\n\n).
Gerenciamento e Exclusão Dinâmica de Documentos:
Desafio: O usuário precisava remover arquivos antigos da pasta docs/ sem ter que abrir o gerenciador de arquivos do sistema operacional.
Solução: Criação de botões de exclusão individual (🗑️) na barra lateral usando os.remove e st.rerun(), atualizando instantaneamente o contador de memória ativa.
O Papel Fundamental do Supervisor Humano (Human-in-the-Loop - HITL)
A supervisão humana foi a pedra angular para garantir que a aceleração por IA mantivesse o rigor técnico:
Prevenção de Alucinações: Testes práticos confrontaram as respostas do assistente contra os manuais oficiais da SETAD/MCTI, garantindo que o RAG recusasse responder sobre dados ausentes na base.
Validação de Respostas: O supervisor humano identificou a necessidade de apresentar os parágrafos literais completos para auditoria e idealizou a barra lateral de diagnóstico para total controle da base ativa.
📋 6. Suíte de Testes Automatizados
O arquivo test_app.py valida as funcionalidades essenciais da aplicação:
test_generate_rag_response_empty_context: Garante aviso apropriado quando a base está sem documentos.
test_generate_rag_response_with_context: Confirma que buscas por siglas e termos específicos retornam dados contextualizados.
test_docs_directory_exists: Valida a presença do diretório local de documentos do RAG.
📄 7. Licença e Autoria
Este projeto foi desenvolvido sob a licença MIT — consulte o arquivo LICENSE para mais detalhes.
Desenvolvido por: es-hmi
Repositório Oficial: github.com/es-hmi/assistente-lei-informatica