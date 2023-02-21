from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

users = []

# Signup API
@app.route('/signup', methods=['POST'])
def signup():
    # Parse the request data
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    # Generate a hash of the user's password
    hashed_password = generate_password_hash(password, method='sha256')

    # Add the new user to the list of users
    users.append({
        'name': name,
        'email': email,
        'password': hashed_password
    })

    # Return a success message
    return jsonify({'message': 'User created successfully!'}), 201

# Login API
@app.route('/login', methods=['POST'])
def login():
    # Parse the request data
    data = request.get_json()
    email = data['email']
    password = data['password']

    # Find the user with the given email address
    user = next((user for user in users if user['email'] == email), None)

    if not user:
        # Return an error if the user is not found
        return jsonify({'message': 'User not found!'}), 401

    if not check_password_hash(user['password'], password):
        # Return an error if the password is incorrect
        return jsonify({'message': 'Invalid credentials!'}), 401

    # Return a success message
    return jsonify({'message': 'Login successful!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
