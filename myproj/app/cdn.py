import random
import requests

# Define the list of backend servers
backend_servers = ['http://127.0.0.1:4000', 'http://192.168.137.7:4000']

# Define the function that returns a randomly selected backend server
def get_backend_server():
    return random.choice(backend_servers)

# # Define the function that handles incoming requests
# def handle_request(request):
#     # Get a backend server
#     backend_server = get_backend_server()
    
#     # Forward the request to the backend server
#     response = requests.get(backend_server + request.path, headers=request.headers)
    
#     # Return the response from the backend server
#     return response.content, response.status_code, response.headers.items()

def handle_request(request):
    # Get a backend server
    backend_server = get_backend_server()
    
    # Forward the request to the backend server
    if request.method == 'GET':
        response = requests.get(backend_server + request.path, headers=request.headers)
    elif request.method == 'POST':
        response = requests.post(backend_server + request.path, headers=request.headers, data=request.get_data())
    else:
        return 'Method not allowed', 405
    
    # Return the response from the backend server
    return response.content, response.status_code, response.headers.items()



# Define the Flask app
from flask import Flask, request

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    content, status_code, headers = handle_request(request)
    return content, status_code, headers
