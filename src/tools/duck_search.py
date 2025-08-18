from ddgs import DDGS
from crewai.tools import BaseTool
# A correção está aqui! Usando o Pydantic padrão (V2).
from pydantic import BaseModel, Field

class SearchToolInput(BaseModel):
    query: str = Field(description="A query de busca a ser executada")

class SearchTools:
    class DuckDuckGoSearchTool(BaseTool):
        name: str = "Ferramenta de Busca DuckDuckGo"
        description: str = "Use esta ferramenta para buscar informações na internet."
        args_schema: type[BaseModel] = SearchToolInput

        def _run(self, query: str) -> str:
            try:
                with DDGS() as ddgs:
                    results = [r for r in ddgs.text(keywords=query, max_results=5)]
                    return str(results) if results else "Nenhum resultado encontrado."
            except Exception as e:
                return f"Erro ao executar a busca: {e}"

# E no seu arquivo principal (crew.py), você importaria assim:
# from tools import SearchTools
# search_tool = SearchTools.DuckDuckGoSearchTool()