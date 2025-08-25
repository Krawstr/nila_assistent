from ddgs import DDGS
from crewai.tools import tool

class SearchTools:
    @tool("Ferramenta de Busca DuckDuckGo")
    def DuckDuckGoSearchTool(query: str) -> str:
        """Uma ferramenta para realizar buscas na internet usando DuckDuckGo.
        A entrada para esta ferramenta deve ser a pergunta ou termo de busca
        em formato de texto simples.""" 

        if isinstance(query, dict) and 'query' in query:
            query = query['query']
        
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=5)]
            return "\n".join(str(r) for r in results) if results else "Nenhum resultado encontrado."

