import httpx
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
import hashlib
import json
import os
from chromadb.api.async_fastapi import AsyncFastAPI
import requests

import chromadb
import hashlib
import json

# class ChromaDBClient:
#     def __init__(self):
#         self.client = chromadb.HttpClient(host='localhost', port=8000)
#         self.collection = self.client.get_or_create_collection(name="chat_history")

#     def generate_unique_id(self, session_id, user, message):
#         hash_input = f"{session_id}:{user}:{message}"
#         return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()

#     def insert_message(self, session_id, user, message):
#         unique_id = self.generate_unique_id(session_id, user, message)
#         self.collection.upsert(documents=[json.dumps({"user": user, "message": message})], ids=[unique_id])

#     def get_all_messages(self, session_id):
#         query_texts = [f"session_id:{session_id}"]
#         results = self.collection.query(query_texts=query_texts, n_results=100)
#         chat_history = [json.loads(doc) for doc in results]
#         return chat_history


class ChromaDBClient:
    def __init__(self):
        # Initialize the embeddings and Chroma persistence with a specific directory
        # self.embeddings = OpenAIEmbeddings(api_key="your_openai_api_key")
        # self.chroma_db = Chroma(persist_directory="data/chat_history", 
        #                         embedding_function=self.embeddings,
        #                         collection_name="lc_chat_history")
        # self.collection = self.chroma_db.get()
        # Initialize the AsyncFastAPI implementation
        self.api_client = requests.Session()  # Persistent session for connection pooling
        
        # Initialize Chroma with the AsyncFastAPI instance
        self.chroma_db = httpx.Client()


    def generate_unique_id(self, session_id, user, message):
        # Generate a unique ID using SHA-256 hash of the combined string
        hash_input = f"{session_id}:{user}:{message}"
        return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()

    async def insert_message(self, session_id, user, message):
        # Insert a new document with embedding into the Chroma database
        unique_id = self.generate_unique_id(session_id, user, message)
        embedding = await self.embeddings.embed(message)
        await self.chroma_db.add(documents=[message], embeddings=[embedding], ids=[unique_id])
        self.chroma_db.persist()

    async def get_all_messages(self, session_id=None):
        # Fetch all documents; filtering by session_id if specified
        all_docs = await self.chroma_db.get()
        if session_id:
            # Filter documents by session_id
            filtered_docs = {k: v for k, v in all_docs.items() if v['session_id'] == session_id}
            return filtered_docs
        return all_docs

# Example usage
if __name__ == "__main__":
    import asyncio

    client = ChromaDBClient()
    
    async def manage_data():
        await client.insert_message("session1", "user1", "Hello from ChromaDB!")
        messages = await client.get_all_messages()
        print("All messages:", messages)

    asyncio.run(manage_data())
