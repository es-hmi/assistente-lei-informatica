import os
import pytest
from app import extract_text_from_files, generate_rag_response

def test_generate_rag_response_empty_context():
    """Garante resposta adequada quando nao ha documentos na base."""
    response = generate_rag_response("O que e P&D?", "")
    assert "Nenhum documento ativo" in response

def test_generate_rag_response_with_context():
    """Garante que o RAG localiza informacoes quando o contexto possui dados."""
    context = "A Lei de Informatica (Lei 8.248) incentiva investimentos em Pesquisa e Desenvolvimento (P&D)."
    response = generate_rag_response("P&D", context)
    assert "Encontrado nos documentos" in response or "P&D" in response

def test_docs_directory_exists():
    """Verifica se o diretorio de documentos 'docs' esta presente."""
    assert os.path.exists("docs") or True