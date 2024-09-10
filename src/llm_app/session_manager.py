from llm_app.chat_history import ChatHistory

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def get_session_history(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = ChatHistory()
        return self.sessions[session_id]