from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb+srv://test:test@venkatesh.nvutauw.mongodb.net/?retryWrites=true&w=majority")
db = client['user_db']
users = db['users']
projects = db['projects']

# ✅ Health check route
@app.route('/')
def home():
    return "Backend is running!"

# ✅ Register
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if users.find_one({"email": data['email']}):
        return jsonify({"message": "Email already exists!"}), 400

    hashed_password = generate_password_hash(data['password'])

    user = {
        "name": data['name'],
        "email": data['email'],
        "password": hashed_password,
        "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    users.insert_one(user)
    return jsonify({"message": "Registered successfully!"})

# ✅ Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = users.find_one({"email": data['email']})
    if user and check_password_hash(user["password"], data["password"]):
        return jsonify({
            "message": "Login successful!",
            "user": {
                "name": user["name"],
                "email": user["email"],
                "createdAt": user["createdAt"]
            }
        })
    return jsonify({"message": "Invalid email or password!"}), 401


# ✅ Projects CRUD API
# 🔹 Get all projects
@app.route('/api/projects', methods=['GET'])
def get_projects():
    project_list = []
    for proj in projects.find():
        proj['_id'] = str(proj['_id'])
        project_list.append(proj)
    return jsonify(project_list)


# 🔹 Create a new project
@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.json
    project = {
        "name": data.get('name'),
        "url": data.get('url'),
        "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    result = projects.insert_one(project)
    return jsonify({"message": "Project added!", "id": str(result.inserted_id)})


# 🔹 Update a project
@app.route('/api/projects/<id>', methods=['PUT'])
def update_project(id):
    data = request.json
    projects.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "name": data.get('name'),
            "url": data.get('url')
        }}
    )
    return jsonify({"message": "Project updated!"})


# 🔹 Delete a project
@app.route('/api/projects/<id>', methods=['DELETE'])
def delete_project(id):
    projects.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Project deleted!"})


# ✅ Run the app
if __name__ == '__main__':
    app.run(debug=True)
