from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
import os
# Load environment variables from .env file
load_dotenv()

# Access OPENAI_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI
app = FastAPI()

# Setup for document embedding and Chroma database
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
chroma_db = Chroma(persist_directory="data", embedding_function=embeddings, collection_name="lc_chroma_demo")

async def initialize_chroma_collection():
    # Load or create the Chroma collection
    collection = await chroma_db.get()
    
    # Check if the collection is empty and needs initialization
    if not collection['ids']:
        # Placeholder: Assume 'docs' is predefined or fetched from somewhere
        docs = ["Document 1 content", "Document 2 content"]
        
        # Create and populate the Chroma database from documents
        chroma_db = Chroma.from_documents(
            documents=docs, 
            embedding=embeddings, 
            persist_directory="data",
            collection_name="lc_chroma_demo"
        )
        # Save the Chroma database to disk
        chroma_db.persist()

# Define a message model for inserting data via API
class Message(BaseModel):
    text: str

@app.on_event("startup")
async def startup_event():
    # Initialize or load Chroma collection on server startup
    await initialize_chroma_collection()

@app.post("/insert_document/")
async def insert_document(message: Message):
    # Insert a new document into the Chroma collection
    try:
        # Embed the document text
        embedding = await embeddings.embed(message.text)
        # Add to Chroma collection
        await chroma_db.add(documents=[message.text], embeddings=[embedding])
        return {"status": "Document inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_documents/")
async def get_documents():
    try:
        # Fetch all documents and their embeddings
        documents = await chroma_db.get()
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def start_chroma_server():
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    start_chroma_server()
