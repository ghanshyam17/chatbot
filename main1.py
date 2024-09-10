# Create Langchain MRKL Agents

from langchain_openai import OpenAI, ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now you can access OPENAI_API_KEY like this
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


VERBOSE_LANGCHAIN = True
def create_agent(
    db_uri,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    verbose=VERBOSE_LANGCHAIN,
    temperature=0,
    model="gpt-3.5-turbo",
):
    db = SQLDatabase.from_uri(db_uri)
    toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=temperature, openai_api_key=OPENAI_API_KEY))

    return create_sql_agent(
        llm=ChatOpenAI(temperature=temperature, model=model),
        toolkit=toolkit,
        verbose=verbose,
        agent_type=agent_type,
    )


# Create SQL agent to interact with ecommerce database
agent_real_db = create_agent("sqlite:////Users/ghanshyam/Projects/fornax/llm/langchain/ecommerce.db")

prompt = "What are the top 5 products in the database?"
result = agent_real_db.run(prompt)
print(result)
