
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from datetime import date
from dotenv import load_dotenv
import os
from src.tool.sql_consult import run_query_tool, list_tables, describe_tables_tool

load_dotenv()


class OpenAIAgent:
    def __init__(self, model: str = "gpt-4o", temperature: float = 0):
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        self.chat = ChatOpenAI(temperature=temperature, model=model)
        self.tools = [run_query_tool, describe_tables_tool]
        
        tables = list_tables()
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessage(content=(
                    "Você é uma IA que tem acesso a um banco de dados SQLite.\n"
                    f"Se precisar fazer algum filtro de data, hoje é dia {date.today()} \n"
                   f"banco de dados possui tabelas de: : {tables}\n"
                    "Não faça suposições sobre quais tabelas existem, ou quais colunas existem.\n"
                    "Em vez disso, use a função 'describe_tables'"
                )),
                HumanMessagePromptTemplate.from_template("{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )
        
        agent = OpenAIFunctionsAgent(
            llm=self.chat,
            prompt=prompt,
            tools=self.tools
        )
        
        self.agent_executor = AgentExecutor(
            agent=agent,
            verbose=True,
            tools=self.tools,
        )
    
    def execute(self, query: str):
        return self.agent_executor.invoke({"input": query})

