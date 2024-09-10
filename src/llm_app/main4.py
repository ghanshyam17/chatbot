from flask import Flask, render_template, request, session
from langchain_openai import OpenAI, ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain_community.utilities import SQLDatabase
from llm_app.conversation import Conversation  # Ensure this is correctly implemented

from dotenv import load_dotenv
import os
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for session management

# Load environment variables from .env file
load_dotenv()

# Access OPENAI_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Global dictionary to store Conversation objects
conversations = {}

def create_agent(db_uri, verbose=True, temperature=0, model="gpt-3.5-turbo"):
    db = SQLDatabase.from_uri(db_uri)
    toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=temperature, openai_api_key=OPENAI_API_KEY))
    return create_sql_agent(
        llm=ChatOpenAI(temperature=temperature, model=model),
        toolkit=toolkit,
        verbose=verbose,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )

@app.route("/", methods=["GET", "POST"])
def home():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())  # Initialize session ID if it doesn't exist

    session_id = session['session_id']
    if session_id not in conversations:
        conversations[session_id] = Conversation(session_id)  # Initialize conversation if not present

    conversation = conversations[session_id]

    if request.method == "POST":
        user_input = request.form['user_input']
        agent = create_agent("sqlite:////Users/ghanshyam/Projects/fornax/llm/langchain/ecommerce.db")
        
        response = agent.run(user_input)
        conversation.add_message('User', user_input)
        conversation.add_message('Agent', response)

        chat_history = conversation.get_history()
        return render_template('chat.html', history=chat_history)
    else:
        return render_template('chat.html')
if __name__ == "__main__":
    app.run(debug=True)