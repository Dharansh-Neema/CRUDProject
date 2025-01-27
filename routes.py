from flask import request,current_app,Blueprint,jsonify
from bson import ObjectId
from datetime import datetime
from bson.json_util import dumps
user_bp = Blueprint('/user',__name__)

@user_bp.route('/')
def index():
    users = current_app.db.users.find()
    return jsonify({"users":dumps(users)}),201

@user_bp.route('/details',methods=["POST"])
def get_user():
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({"error":"user_id not provided"}),400
    user_id = data['user_id']
    try:
        user = current_app.db.users.find_one({'_id': ObjectId(user_id)})
        if user:
            return jsonify({"user":dumps(user)}), 200
        else:
            return jsonify({"error":"No user found"})
    except Exception as e:
        return f"Unexpected exception happend {e}",404

@user_bp.route("/create",methods=["POST"])
def create_user():
    data = request.json
    if not data:
        return jsonify({"error":"No Data provided"}),400
    new_user = {
        'username' : data.get("username"),
        'email' : data.get("email"),
        "name" : data.get("name"),
        "age":data.get("age"),
        "created_at":datetime.utcnow(),
        "updated_at":datetime.utcnow()
    }
    res = current_app.db.users.insert_one(new_user)
    new_user['_id'] = str(res.inserted_id)
    return jsonify({"message": "User created successfully", "user": dumps(new_user)}), 201

@user_bp.route("/edit/<string:user_id>",methods=["POST"])
def edit_user(user_id):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    user = current_app.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    updated_user = {
        'username': data.get('username', user['username']),
        'email': data.get('email', user['email']),
        'full_name': data.get('full_name', user['full_name']),
        'age': data.get('age', user['age']),
        'updated_at': datetime.utcnow()
    }
    current_app.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': updated_user})
    updated_user['_id'] = user_id
    return jsonify({"message": "User updated successfully", "user": dumps(updated_user)}), 200

@user_bp.route('/delete/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = current_app.db.users.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count:
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404