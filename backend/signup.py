from flask import Blueprint, jsonify ,request
from database import db,User
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash
signup_bp=Blueprint('signup_bp',__name__)








@signup_bp.route('/post', methods=['POST'])
@cross_origin()
def handle_signup():
    data=request.get_json()
    print(data)
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 401

    required_fields = ['name', 'age', 'address', 'email', 'mobile', 'password']
    missing_fields = [field for field in required_fields if not data.get(field)]

    existing_user = User.query.filter(
        (User.email == data['email']) | (User.mobile == data['mobile'])
    ).first()

    if existing_user:
        return jsonify({'login': 'true', 'message': 'User already exists'}), 409 

    if missing_fields:
        return jsonify({'error': 'Missing required fields', 'missing': missing_fields}), 400
    new_user =User(
            name=data['name'],
            age=data['age'],
            address=data['address'],
            email=data['email'],
            mobile=data['mobile'],
            password=generate_password_hash(data['password'])  # Hash here

            #password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'signup':'true','message':'signup sucessfully'}) ,200    
  






