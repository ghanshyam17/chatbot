# Create Langchain MRKL Agents

from langchain_openai import OpenAI, ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain_community.utilities import SQLDatabase

# import os

# # Load environment variables from .env file

# # Now you can access OPENAI_API_KEY like this
# OPENAI_API_KEY = "sk-KqQQCOuMMZVJMCwDG24e9A79YaIz2kIWGP3FYcS0HOT3BlbkFJE6hDryf7Gyu5hOusi0fxFspE1O2dQghkQaaVxlYJcA"
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

VERBOSE_LANGCHAIN = True
def create_agent(
    db_uri,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    verbose=VERBOSE_LANGCHAIN, 
    temperature=0,
    model="gpt-3.5-turbo",
):
    db = SQLDatabase.from_uri(db_uri)
    toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=temperature, openai_api_key=openai_api_key))

    return create_sql_agent(
        llm=ChatOpenAI(temperature=temperature, model=model),
        toolkit=toolkit,
        verbose=verbose,
        agent_type=agent_type,
    )


# Create SQL agent to interact with ecommerce database
# agent = create_agent("sqlite:///C:/Users/Gsutar/ghanshyam/excel_tool/ai_bot/chatbot/ecommerce1.db")
agent = create_agent("sqlite:///C:/Users/Gsutar/ghanshyam/excel_tool/analysis.db")

prompt = "What are the top 5 products in the database with high Plan Qty availability?"
result = agent.run(prompt)
print(result)
