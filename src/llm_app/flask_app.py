# from flask import Flask
# app = Flask(__name__)
# @app.route('/')  # Define a route for the root URL
# def home():
#     return 'Hello, Chroma!'

# def start_chroma_server(config):
#     host = config.get('host', 'localhost')
#     port = config.get('port', 8000)
#     try:
#         app.run(host=host, port=port)
#     except Exception as e:
#         print(f"Failed to start the server: {e}")

# # Example server configuration
# server_config = {
#     'host': 'localhost',
#     'port': 8000
# }

# start_chroma_server(server_config)