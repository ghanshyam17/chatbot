from flask import Flask, request, render_template_string, session, redirect, url_for
import os
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure secret key for session management

# Mockup classes for the agent and chat history
class Agent:
    def run(self, prompt):
        return f"Echo: {prompt}"  # Simulate agent response

class ChatHistory:
    def __init__(self):
        self.history = []

    def add_message(self, user, message):
        self.history.append((user, message))

    def get_history(self):
        return self.history

# Create global objects for simplicity in this example
agent = Agent()
chat_history = ChatHistory()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input.lower() in ['exit', 'quit']:
            session.pop('session_id', None)  # End the session
            return redirect(url_for('home'))  # Redirect to start a new conversation

        # Update chat history
        chat_history.add_message('User', user_input)
        
        # Generate response from the agent
        response = agent.run(user_input)
        chat_history.add_message('Agent', response)

        # Render the same page with updated chat history
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Chat with Agent</title>
            </head>
            <body>
                <h1>Chat Session</h1>
                <form method="post">
                    <input type="text" name="user_input" autofocus>
                    <input type="submit" value="Send">
                </form>
                <div>
                    {% for user, msg in chat_history %}
                        <p><strong>{{ user }}:</strong> {{ msg }}</p>
                    {% endfor %}
                </div>
            </body>
            </html>
        ''', chat_history=chat_history.get_history())
    else:
        return render_template_string('''
            <form method="post">
                <input type="text" name="user_input" autofocus>
                <input type="submit" value="Start Chat">
            </form>
        ''')

if __name__ == "__main__":
    app.run(debug=True)
