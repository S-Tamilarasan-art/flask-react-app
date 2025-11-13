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
db_url = os.getenv("DATABASE_URL") or os.getenv("MYSQL_URL")

if not db_url:
    # Manually build connection if Railway splits it
    host = os.getenv("MYSQLHOST")
    user = os.getenv("MYSQLUSER")
    password = os.getenv("MYSQLPASSWORD")
    dbname = os.getenv("MYSQLDATABASE")
    port = os.getenv("MYSQLPORT", 3306)
    if host and user and password and dbname:
        db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
# CORS configuration
CORS(app, resources={
    r"/signup/*": {"origins": [frontend_dev, frontend_prod]},
    r"/login/*": {"origins": [frontend_dev, frontend_prod]},
    r"/dashboard/*": {"origins": [frontend_dev, frontend_prod]},
})

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print("DATABASE_URL:", os.getenv("DATABASE_URL"))
print("MYSQL_URL:", os.getenv("MYSQL_URL"))
print("MYSQLHOST:", os.getenv("MYSQLHOST"))
print("MYSQLUSER:", os.getenv("MYSQLUSER"))
print("MYSQLPASSWORD:", os.getenv("MYSQLPASSWORD"))
print("MYSQLDATABASE:", os.getenv("MYSQLDATABASE"))
print("MYSQLPORT:", os.getenv("MYSQLPORT"))

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    
