from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from database import db, User
import os

dashboard_bp = Blueprint("dashboard_bp", __name__)
# Get user details using email
@dashboard_bp.route("/user", methods=["GET"])
def get_user():
    email = request.args.get("email")
    user = User.query.filter(User.email==email).first()
    print(user)

    if not email:
        return jsonify({"message": "Email required"}), 400

    
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "phone": user.mobile,
        "address": user.address
        
    }), 200



@dashboard_bp.route("/update", methods=["PUT"])
def update_user():
    # Get email from query parameters
    data=request.get_json()
    email =data.get("email")
    
    print(data,email)
    if not email:
        return jsonify({"message": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Get JSON data from request body
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    # Update fields if present in request
    name = data.get("name")
    mobile = data.get("mobile")
    address = data.get("address")

    if name:
        user.name = name
    if mobile:
        user.mobile = mobile
    if address:
        user.address = address

    db.session.commit()

    return jsonify({
        "message": "User details updated successfully",
        "user": {
            "email": user.email,
            "name": user.name,
            "mobile": user.mobile,
            "address": user.address
        }
    }), 200



@dashboard_bp.route("/upload", methods=["POST"])
def upload_file():
    data=request.get_json
    email = request.form.get("email")
    file = request.files.get("file")
    UPLOAD_FOLDER = email
    ALLOWED_EXTENSIONS = {"pdf", "png", "jpeg"}

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    def allowed_file(filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    if not email or not file:
        return jsonify({"message": "email and file required"}), 400

    if not allowed_file(file.filename):
        return jsonify({"message": "Invalid file type"}), 400

    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Update user record
    user.uploaded_file = filename
    db.session.commit()

    return jsonify({"message": "File uploaded successfully!"}), 200
 


@dashboard_bp.route("/filedownload", methods=["GET"])
def file_download_route():
    email = request.args.get("email")   # <-- FIXED
    print("email:",email)
    if not email:
        return jsonify({"error": "Email required"}), 400

    user_folder = os.path.join(email)

    if not os.path.exists(user_folder):
        return jsonify([]), 200

    files = os.listdir(user_folder)
    return jsonify(files), 200
