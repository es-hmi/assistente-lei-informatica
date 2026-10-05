import os
import streamlit as st
from pypdf import PdfReader

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Assistente Virtual - Lei de Informática",
    page_icon="🤖",
    layout="wide"
)

DOCS_DIR = "docs"
os.makedirs(DOCS_DIR, exist_ok=True)

def extract_text_from_files(directory=DOCS_DIR):
    """Extrai e consolida o texto de todos os arquivos PDF e TXT na pasta docs."""
    context = ""
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if filename.lower().endswith(".pdf"):
                try:
                    reader = PdfReader(file_path)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            context += text + "\n"
                except Exception as e:
                    st.error(f"Erro ao ler PDF {filename}: {e}")
            elif filename.lower().endswith(".txt"):
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        context += f.read() + "\n"
                except Exception as e:
                    st.error(f"Erro ao ler TXT {filename}: {e}")
    return context

def generate_rag_response(query, context):
    """Gera uma resposta baseada nos parágrafos mais relevantes do contexto."""
    if not context.strip():
        return "⚠️ Nenhum documento ativo na base de conhecimento. Faça o upload de um PDF ou TXT na barra lateral."
    
    # Lista de palavras de ligação irrelevantes para a busca (stopwords)
    stopwords = {
        "como", "onde", "qual", "quais", "quem", "sobre", "para", "com", 
        "uma", "esse", "essa", "esta", "tipos", "sao", "estao", "quaisque"
    }
    
    # Mantém palavras e siglas técnicas com 2 ou mais letras (ex: RDA, P&D, PPB)
    words = [w.lower().strip("?,.!") for w in query.split()]
    query_words = [w for w in words if w not in stopwords and len(w) >= 2]
    
    if not query_words:
        return "Por favor, digite uma pergunta com termos mais específicos para a busca."

    # Divide o documento em parágrafos reais (blocos de texto)
    paragraphs = [p.strip() for p in context.split("\n\n") if len(p.strip()) > 50]
    
    scored_paragraphs = []
    for p in paragraphs:
        # CORREÇÃO 1: Ignora linhas/blocos típicos de sumário com pontos corridos
        if "........" in p or "SUMÁRIO" in p.upper():
            continue
            
        p_lower = p.lower()
        # CORREÇÃO 2: Pontua o parágrafo pela quantidade de palavras-chave encontradas
        score = sum(1 for word in query_words if word in p_lower)
        if score > 0:
            scored_paragraphs.append((score, p))
    
    # Ordena os parágrafos do mais relevante para o menos relevante
    scored_paragraphs.sort(key=lambda x: x[0], reverse=True)
    
    if scored_paragraphs:
        # Seleciona os 3 parágrafos com maior pontuação
        best_matches = [p for score, p in scored_paragraphs[:3]]
        response_text = "\n\n---\n\n".join(best_matches)
        return f"📖 **Trechos mais relevantes encontrados no documento:**\n\n{response_text[:2000]}"
    else:
        return f"🔍 Busquei pelos termos `{query_words}`, mas não encontrei trechos correspondentes nos documentos ativos."

# --- INTERFACE STREAMLIT ---

# Barra Lateral (Sidebar)
with st.sidebar:
    st.header("📂 Base de Conhecimento")
    
    uploaded_file = st.file_uploader(
        "Adicionar Lei, Manual ou Projeto (PDF/TXT):",
        type=["pdf", "txt"]
    )
    
    if uploaded_file is not None:
        file_path = os.path.join(DOCS_DIR, uploaded_file.name)
        if not os.path.exists(file_path):
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Documento '{uploaded_file.name}' adicionado com sucesso!")
    
    st.subheader("📋 Documentos Ativos na Memória")
    # Lista e gerenciamento de exclusão de arquivos ativos
    active_files = [f for f in os.listdir(DOCS_DIR) if not f.startswith(".")]
    
    if active_files:
        for file in active_files:
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write(f"📄 {file}")
            with col2:
                # Botão de apagar para cada arquivo individual
                if st.button("🗑️", key=f"del_{file}", help=f"Excluir {file}"):
                    file_path = os.path.join(DOCS_DIR, file)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        st.toast(f"Arquivo '{file}' removido com sucesso!")
                        st.rerun()
    else:
        st.info("Nenhum documento cadastrado na pasta `docs/`.")

# Área Principal - Chatbot
st.title("🤖 Assistente Virtual - Lei de Informática")
st.caption("Respostas baseadas estritamente na base de documentos carregada (RAG).")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Como posso ajudar você com a Lei de Informática hoje?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Digite sua dúvida..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.spinner("Analisando documentos..."):
        context = extract_text_from_files()
        response = generate_rag_response(prompt, context)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)