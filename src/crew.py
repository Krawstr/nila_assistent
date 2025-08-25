import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from typing import List
from crewai.agents.agent_builder.base_agent import BaseAgent
from tools import rag_search_tool, SearchTools 

load_dotenv()

search_tool = SearchTools().DuckDuckGoSearchTool

@CrewBase
class AgentsCrew():
    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.gemini_llm = LLM(
            model="gemini/gemini-2.0-flash", 
            api_key=self.google_api_key,
        )

    @agent
    def nila(self) -> Agent:
        return Agent(
            config=self.agents_config['nila'],
            llm=self.gemini_llm,
            tools=[search_tool],
            allow_delegation=False,
            embedder={
                "provider": "google",
                "config": {
                    "api_key": self.google_api_key,
                    "model": "models/text-embedding-004" }
                    },
            memory=True,
            verbose=True,
            max_iter=7 
        )

    @agent
    def raga(self) -> Agent:
        return Agent(
            config=self.agents_config['raga'],
            llm=self.gemini_llm,
            tools=[rag_search_tool],
            allow_delegation=False, 
            verbose=True,
            max_iter=5 
        )

    @task
    def nila_career_guide(self) -> Task:
        return Task(config=self.tasks_config['nila_career_guide'], 
                    agent=self.nila())

    @task
    def raga_data_retrieval(self) -> Task:
        return Task(config=self.tasks_config['raga_data_retrieval'], agent=self.raga(), 
                    context=[self.nila_career_guide()])
    
    @task
    def nila_final_report(self) -> Task:
        return Task(config=self.tasks_config['nila_final_report'], agent=self.nila(),
                     context=[self.raga_data_retrieval()])

    @crew
    def career_crew(self) -> Crew:
        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            process=Process.sequential,
            memory=True,
            embedder={
                "provider": "google",
                "config": {
                    "api_key": self.google_api_key,
                    "model": "models/text-embedding-004" }
                    },
            verbose=True,
            max_rpm=14
          
        )
    
    def kickoff(self, inputs: dict):
        result = self.career_crew().kickoff(inputs=inputs)
        return result.raw


# if __name__ == "__main__":
#     print("Iniciando o Crew de Carreira...")
#     my_crew = AgentsCrew()
#     inputs = {'topic': 'quero saber quanto ganha um analista de sistemas.'}
#     result = my_crew.kickoff(inputs=inputs) 

#     print("\n\n########################")
#     print("## Execução do Crew Finalizada!")
#     print("########################\n")
#     print("Resultado:")
#     print(result)