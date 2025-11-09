from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from signup import signup_bp
from login import login_bp
from dashboard import dashboard_bp
from database import db
from dotenv import load_dotenv
import os



load_dotenv() 

app = Flask(__name__)
db_url = os.getenv("DATABASE_URL")
frontend_dev = os.getenv("FRONTEND_DEV_URL")
frontend_prod = os.getenv("FRONTEND_PROD_URL")

# CORS configuration
CORS(app, resources={
    r"/signup/*": {"origins": [frontend_dev, frontend_prod]},
    r"/login/*": {"origins": [frontend_dev, frontend_prod]},
    r"/dashboard/*": {"origins": [frontend_dev, frontend_prod]},
})

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # or specify your domain
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


db.init_app(app)


app.register_blueprint(signup_bp, url_prefix='/signup')
app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(dashboard_bp,url_prefix='/dashboard')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
