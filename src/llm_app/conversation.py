from llm_app.chromadb_client import ChromaDBClient
from collections import deque
from langchain_community.memory import ConversationBufferMemory

# class Conversation:
#     def __init__(self, session_id):
#         self.session_id = session_id
#         self.db_client = ChromaDBClient()
#         self.local_cache = deque(maxlen=100)  # Keep last 100 messages in memory for quick access

#     def add_message(self, user, message):
#         # Add message to local cache
#         self.local_cache.append((user, message))
#         # Insert message to ChromaDB for persistence
#         self.db_client.insert_message(self.session_id, user, message)

#     def get_history(self):
#         # First check if there's sufficient history in local cache
#         if len(self.local_cache) < 100:
#             # If not, load more history from ChromaDB
#             more_history = self.db_client.get_all_messages(self.session_id)
#             # Prepend older messages to the local cache
#             for message in reversed(more_history):
#                 self.local_cache.appendleft(message)
#                 if len(self.local_cache) >= 100:
#                     break
#         return list(self.local_cache)

#     def sync_with_db(self):
#         """Method to synchronize local cache with database if needed."""
#         # This method can be called periodically or after a conversation ends
#         for user, message in self.local_cache:
#             self.db_client.insert_message(self.session_id, user, message)


# from chromadb_client import ChromaDBClient

# class Conversation:
#     def __init__(self, session_id):
#         self.db_client = ChromaDBClient()
#         self.session_id = session_id

#     def add_message(self, user, message):
#         self.db_client.insert_message(self.session_id, user, message)

#     def get_history(self):
#         return self.db_client.get_all_messages(self.session_id)



# from llm_app.chromadb_client import ChromaDBClient
# from langchain_community.memory import ConversationBufferMemory
# class Conversation:
#     def __init__(self, session_id):
#         self.db_client = ChromaDBClient()
#         self.session_id = session_id
#         self.memory = ConversationBufferMemory()

#     def add_message(self, user, message):
#         # Add to memory and DB
#         self.memory.add_message(user, message)
#         self.db_client.insert_message(self.session_id, user, message)

#     def get_history(self):
#         # Get history from memory
#         return self.memory.get_history()

class Conversation:
    def __init__(self, session_id):
        self.db_client = ChromaDBClient()
        self.session_id = session_id
        self.memory = ConversationBufferMemory()

    def add_message(self, user, message):
        try:
            self.db_client.save_message(self.session_id, (user, message))
            if self.history_cache is not None:
                self.history_cache.append((user, message))
        except Exception as e:
            print(f"Failed to add message: {e}")

    def get_history(self):
        if self.history_cache is None:
            try:
                self.history_cache = self.db_client.load_history(self.session_id)
            except Exception as e:
                print(f"Failed to load history: {e}")
                self.history_cache = []
        return self.history_cache

    def end_conversation(self):
        try:
            self.db_client.reset_history(self.session_id)
            self.history_cache = []
        except Exception as e:
            print(f"Failed to end conversation: {e}")

    def refresh_history(self):
        try:
            self.history_cache = self.db_client.load_history(self.session_id)
        except Exception as e:
            print(f"Failed to refresh history: {e}")
            self.history_cache = []
