from langchain_openai import OpenAI, ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain_community.utilities import SQLDatabase

from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# Load environment variables from .env file

#  Define a Chat History Storage

class ChatHistory:
    def __init__(self):
        self.history = []

    def add_message(self, message):
        self.history.append(message)

    def get_history(self):
        return self.history


# Now you can access OPENAI_API_KEY like this
OPENAI_API_KEY = "sk-KqQQCOuMMZVJMCwDG24e9A79YaIz2kIWGP3FYcS0HOT3BlbkFJE6hDryf7Gyu5hOusi0fxFspE1O2dQghkQaaVxlYJcA"

VERBOSE_LANGCHAIN = True
def create_agent(
    db_uri,
    memory,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    verbose=VERBOSE_LANGCHAIN,
    temperature=0,
    model="gpt-3.5-turbo",
    chat_history=None,  # Add chat_history as an optional parameter

):
    db = SQLDatabase.from_uri(db_uri)
    toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=temperature, openai_api_key=OPENAI_API_KEY))
    memory = ConversationBufferMemory()  # Initialize ConversationBufferMemory

    return create_sql_agent(
        llm=ChatOpenAI(temperature=temperature, model=model),
        toolkit=toolkit,
        memory=memory,  # Pass the memory object to the agent
        verbose=verbose,
        agent_type=agent_type,
    )

# # Initialize chat history
# chat_history = ChatHistory()

# # Create SQL agent to interact with ecommerce database
# agent_real_db = create_agent("sqlite:////Users/ghanshyam/Projects/fornax/llm/langchain/ecommerce.db", chat_history=chat_history)



# prompt = "What are the top 5 products in the database?"

# # Add prompt to chat history before running
# chat_history.add_message(prompt)
# result = agent_real_db.run(prompt)
# print(chat_history.get_history())
# print(result)


# def interact_with_agent(agent, chat_history):
#     while True:
#         prompt = input("You: ")
#         if prompt.lower() == "exit":
#             break
#         # Concatenate chat history with the new prompt
#         full_prompt = f"{chat_history.get_history()}\n{prompt}" if chat_history.get_history() else prompt
#         response = agent.run(full_prompt)  # Assuming the agent has a run method that takes the full prompt and returns a response
#         print(f"Agent: {response}")
#         # Update chat history
#         chat_history.add_message(f"You: {prompt}\nAgent: {response}")

def interact_with_agent(agent):
    while True:
        prompt = input("You: ")
        if prompt.lower() == "exit":
            break
        response = agent.run(prompt)  # The agent handles memory internally
        print(f"Agent: {response}")


# from langchain_community.chat_message_histories import FileChatMessageHistory

# agent = AutoGPT.from_llm_and_tools(
#     ai_name="Tom",
#     ai_role="Assistant",
#     tools=tools,
#     llm=ChatOpenAI(temperature=0),
#     memory=vectorstore.as_retriever(),
#     chat_history_memory=FileChatMessageHistory("chat_history.txt"),
# )


# Example usage
if __name__ == "__main__":
    # chat_history = ChatHistory()
    # agent = create_agent("sqlite:////Users/ghanshyam/Projects/fornax/llm/langchain/ecommerce.db", chat_history=chat_history)  # Adjust the db_uri as necessary
    
    memory = ConversationBufferMemory()
    # agent = create_agent("sqlite:///C:/Users/Gsutar/ghanshyam/excel_tool/ai_bot/chatbot/ecommerce1.db", memory=memory)
    agent = create_agent("sqlite:///C:/Users/Gsutar/ghanshyam/excel_tool/analysis.db", memory=memory)

    print("agent....")
    interact_with_agent(agent)