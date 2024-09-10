from langchain_openai import OpenAI, ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain_community.utilities import SQLDatabase

from dotenv import load_dotenv
import os
import uuid

from conversation import Conversation
from chat import interact_with_agent
from langchain.memory import ConversationBufferMemory
from chromadb_client import ChromaDBClient

# Load environment variables from .env file
load_dotenv()

# Access OPENAI_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

VERBOSE_LANGCHAIN = True

def create_agent(db_uri, memory, agent_type=AgentType.OPENAI_FUNCTIONS, verbose=VERBOSE_LANGCHAIN,
                 temperature=0, model="gpt-3.5-turbo", chat_history=None):
    db = SQLDatabase.from_uri(db_uri)
    toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=temperature, openai_api_key=OPENAI_API_KEY))

    return create_sql_agent(
        llm=ChatOpenAI(temperature=temperature, model=model),
        toolkit=toolkit,
        verbose=verbose,
        agent_type=agent_type,
    )

if __name__ == "__main__":
    # Create a unique session ID for the chat
    session_id = str(uuid.uuid4())
    print("Session ID:", session_id)

    # Initialize chat history
    chat_history = Conversation(session_id)
    client = ChromaDBClient()
    memory = ConversationBufferMemory()
    print("Starting chat...")
    print("Get all messages: ", client.get_all_messages(session_id = session_id))
    # Create SQL agent to interact with the ecommerce database
    agent = create_agent("sqlite:////Users/ghanshyam/Projects/fornax/llm/langchain/ecommerce.db", memory=memory, chat_history=chat_history)
    
    # Start the chat loop
    interact_with_agent(agent, chat_history)
