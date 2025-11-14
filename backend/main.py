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

frontend_dev = os.getenv("FRONTEND_DEV_URL")
frontend_prod = os.getenv("FRONTEND_PROD_URL")
raw_url = os.getenv("MYSQL_PUBLIC_URL") 
if raw_url.startswith("mysql://"):
    raw_url = raw_url.replace("mysql://", "mysql+pymysql://", 1)

print(raw_url)

   
# CORS configuration
CORS(app, resources={
    r"/signup/*": {"origins": [frontend_dev, frontend_prod]},
    r"/login/*": {"origins": [frontend_dev, frontend_prod]},
    r"/dashboard/*": {"origins": [frontend_dev, frontend_prod]},
})

app.config['SQLALCHEMY_DATABASE_URI'] = raw_url

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
    db.session.close()
    db.engine.dispose()
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    
