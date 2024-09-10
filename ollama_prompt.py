from langchain_community.llms import Ollama

# Create Langchain MRKL Agents

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
llm = Ollama(model="llama2")

VERBOSE_LANGCHAIN = True
def create_agent(
    db_uri,
    # agent_type=AgentType.OPENAI_FUNCTIONS,  # Commented out to use Ollama
    agent_type=AgentType.Ollama,  # Adjusted to MRKL_FUNCTIONS for Ollama

    verbose=VERBOSE_LANGCHAIN,
    temperature=0,
    model="llama2",  # Updated model to llama2
):
    db = SQLDatabase.from_uri(db_uri)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)  # Use the Ollama instance

    return create_sql_agent(
        llm=llm,  # Use the Ollama instance directly
        toolkit=toolkit,
        verbose=verbose,
        agent_type=agent_type,
    )

# Create SQL agent to interact with ecommerce database
agent_real_db = create_agent("sqlite:////Users/ghanshyam/Projects/fornax/llm/langchain/ecommerce.db")

prompt = "What are the top 5 products in the database?"
result = agent_real_db.run(prompt)
