from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm_app.chromadb_client import ChromaDBClient

app = FastAPI()

# Assuming ChromaDBClient is initialized without any arguments; adjust as necessary.
client = ChromaDBClient()

class Message(BaseModel):
    session_id: str
    message: str

@app.post("/messages/")
async def create_message(message: Message):
    try:
        # Assuming 'insert_message' is a method you define to insert a message into ChromaDB.
        client.insert_message(session_id=message.session_id, message=message.message)
        return {"message": "Message inserted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/messages/{session_id}")
async def get_messages(session_id: str):
    try:
        # Assuming 'get_all_messages' retrieves messages for a session from ChromaDB.
        messages = client.get_all_messages(session_id=session_id)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))