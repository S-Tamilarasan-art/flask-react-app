from flask import Blueprint, jsonify,request
from sqlalchemy import and_,or_
from database import User
from flask_cors import CORS
from werkzeug.security import check_password_hash

login_bp =Blueprint('login_bp',__name__)



@login_bp.route('/search',methods=['GET'])
def handle_login():
    
    email=request.args.get("email")
    password=request.args.get("password")
    
    if not email or not password:
        return jsonify({"success": False, "message": "Email and password required"}), 400
    
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    
    is_password_correct = check_password_hash(user.password, password)

    if is_password_correct:
        return jsonify({
            "success": True,
            "message": "Login successful",
            "email": user.email,
            "name": user.name
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Invalid password"
        }), 401
   
