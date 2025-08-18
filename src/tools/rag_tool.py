from crewai.tools import tool
from agents.rag_agent import AgentRAG

agent_rag = AgentRAG(database_path="../database")

@tool("RAG Database Search")
def rag_search_tool(question: str) -> str:
    """
    Ferramenta para buscar informações no banco de dados vetorial personalizado.
    Use esta ferramenta para responder perguntas sobre salários, carreiras e
    tendências de mercado com base em dados internos.
    """
    return agent_rag.get_response(question=question)