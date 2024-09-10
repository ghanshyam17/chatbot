import os
from langchain_openai import ChatOpenAI

# from langchain_openai import OpenAI

# Load environment variables from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client with your API key
# def get_response(prompt, openai_api_key):
#     openai_client = OpenAI(api_key=openai_api_key)
#     response = openai_client.generate_response(prompt)
#     return response['choices'][0]['text']


# Assuming you have initialized ChatOpenAI or similar
chat_model = ChatOpenAI(api_key=OPENAI_API_KEY)

def get_response(prompt):
    # Assume using an AI model such as OpenAI's GPT-3
    import openai
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

