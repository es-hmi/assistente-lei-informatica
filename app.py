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
    """Gera uma resposta baseada no contexto extraído dos documentos."""
    if not context.strip():
        return "⚠️ Nenhum documento ativo na base de conhecimento. Faça o upload de um PDF ou TXT na barra lateral."
    
    query_words = [w.lower() for w in query.split() if len(w) > 3]
    matches = []
    
    paragraphs = context.split("\n\n")
    for p in paragraphs:
        if any(word in p.lower() for word in query_words):
            matches.append(p.strip())
            if len(matches) >= 3:
                break
    
    if matches:
        response_text = "\n\n".join(matches)
        return f"📖 **Análise baseada nos documentos ativos:**\n\n{response_text[:1500]}"
    else:
        return f"🔍 Não encontrei informações diretamente relacionadas a '{query}' nos documentos ativos da base."

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
    active_files = os.listdir(DOCS_DIR)
    if active_files:
        for file in active_files:
            st.write(f"- 📄 {file}")
    else:
        st.info("Nenhum arquivo na pasta 'docs'.")

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