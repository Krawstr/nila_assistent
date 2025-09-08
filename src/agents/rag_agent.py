import os
from dotenv import load_dotenv
from langchain_chroma.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()

class AgentRAG():
    PROMPT_TEMPLATE = """
    Use a informação de contexto abaixo para responder e ajudar a Nila com sua resposta.
    Seja descritivo, direto e amigável.

    Contexto:
    {context}

    Pergunta do usuário:
    {question}
    """

    def __init__(self, database_path: str):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("A variável de ambiente GOOGLE_API_KEY não foi encontrada.")

        print("Inicializando AgentRAG... (Isso só deve aparecer uma vez)")
        self.database_path = database_path
        self.embedding_function = self._load_embedding_function()
        self.db = self._load_database()
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=self.api_key)
        self.prompt = ChatPromptTemplate.from_template(self.PROMPT_TEMPLATE)

    def _load_embedding_function(self):
        return GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=self.api_key)

    def _load_database(self):
        return Chroma(persist_directory=self.database_path, embedding_function=self.embedding_function)
    
    def get_response(self, question: str) -> str:
        search_results = self.db.similarity_search_with_relevance_scores(question, k=10)
        relevance_threshold = 0.6
        relevant_docs = [doc for doc, score in search_results if score >= relevance_threshold]

        if not relevant_docs:
            return "Não consegui encontrar uma resposta relevante para essa pergunta no meu banco de dados."
        
        context = "\n\n---\n\n".join([doc.page_content for doc in relevant_docs])
        
        prompt_message = self.prompt.invoke({"question": question, "context": context})
        response = self.llm.invoke(prompt_message)
        return response.content
