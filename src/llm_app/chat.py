from llm_app.conversation import Conversation
from llm_app.langchain_client import get_response

def interact_with_agent(agent, session_id):
    # Create a Conversation object for this session
    chat_history = Conversation(session_id)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        # Use the refactored handle_input function to process the input
        response = handle_input(chat_history, user_input)
        print(f"Agent: {response}")


def handle_input(conversation, user_input):
    # Add user's input to conversation history
    conversation.add_message('User', user_input)

    # Retrieve updated conversation history
    chat_history = conversation.get_history()

    # Prepare the prompt for the language model by concatenating all previous exchanges
    # prompt = '\n'.join([f"{msg['user']}: {msg['message']}" for msg in history])
    prompt = '\n'.join([f"{speaker}: {message}" for speaker, message in chat_history])

    # Get response from the language model
    response = get_response(prompt)  # Ensure get_response is properly defined or imported

    # Add model's response to conversation history
    conversation.add_message('AI', response)
    return response




# from conversation import Conversation
# from langchain_client import get_response

# def handle_input(conversation, user_input):
#     conversation.add_message('User', user_input)
#     prompt = '\n'.join([f"{msg['user']}: {msg['message']}" for msg in conversation.get_history()])
#     response = get_response(prompt)
#     conversation.add_message('AI', response)
#     return response

# def interact_with_agent(agent, chat_history):
#     while True:
#         current_chat_history = chat_history.get_history()
#         prompt = input("You: ")

#         if prompt.lower() in ['exit', 'quit']:
#             break
#         # Concatenate chat history with the new prompt
#         # full_prompt = '\n'.join([f"{msg['user']}: {msg['message']}" for msg in chat_history.get_history()]) + f"\nUser: {prompt}"
#         response = agent.run(prompt)
#         print(f"Agent: {response}")
        
#         # Update chat history
#         chat_history.add_message('User', prompt)
#         chat_history.add_message('Agent', response)
