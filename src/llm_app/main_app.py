import streamlit as st
from langchain_openai import OpenAI, ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain_community.utilities import SQLDatabase
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

# Load environment variables (e.g., OpenAI API key)
load_dotenv()

# Get the OpenAI API key from environment
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set verbose flag for Langchain
VERBOSE_LANGCHAIN = True

# Function to create a Langchain SQL agent
def create_agent(
    db_uri,
    memory,
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
        memory=memory,
        verbose=verbose,
        agent_type=agent_type,
    )

# Streamlit App Title
st.title("SQL Database Chatbot with Langchain Agent")

# Initialize memory in session state
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

# Initialize the Langchain agent using the SQLite database and memory
agent = create_agent("sqlite:///C:/Users/Gsutar/ghanshyam/excel_tool/analysis.db", memory=st.session_state.memory)

# Input field for the user to ask questions
prompt = st.text_input("Ask a question about the database", value="What is the Plan Qty for the item: ")

# Button to submit the question to the agent
if st.button("Ask Agent"):
    if prompt:
        # Interact with the agent and get the result
        result = agent.run(prompt)

        # Display the result and update conversation in memory
        st.write(f"**You**: {prompt}")
        st.write(f"**Agent**: {result}")

        # Display the conversation history managed by ConversationBufferMemory
        st.text_area("Conversation History", value=st.session_state.memory.buffer, height=300)
    else:
        st.write("Please enter a question.")
