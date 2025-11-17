from flask import Flask
from flask_cors import CORS
from database import db
from dotenv import load_dotenv
from sqlalchemy import text
import os

load_dotenv()

app = Flask(__name__)

frontend_dev = os.getenv("FRONTEND_DEV_URL")
frontend_prod = os.getenv("FRONTEND_PROD_URL")
print(frontend_dev, frontend_prod)
# CORS

CORS(app, resources={
    r"/*": {
        "origins": "*",    
        "supports_credentials": False,   # Must be False when origins="*"
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})



# MYSQL URL FIX
raw_url = os.getenv("MYSQL_PUBLIC_URL")

if raw_url.startswith("mysql://"):
    raw_url = raw_url.replace("mysql://", "mysql+pymysql://", 1)

print("DATABASE URL =>", raw_url)

app.config['SQLALCHEMY_DATABASE_URI'] = raw_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# DB INIT
db.init_app(app)

# TEST DB CONNECTION
with app.app_context():
    try:
        with db.engine.connect() as conn:
            r = conn.execute(text("SELECT DATABASE()"))
            print("Connected to DB:", r.fetchone()[0])
    except Exception as e:
        print("DB Connection Failed:", e)

# ROUTES
from signup import signup_bp
from login import login_bp
from dashboard import dashboard_bp

app.register_blueprint(signup_bp, url_prefix="/signup")
app.register_blueprint(login_bp, url_prefix="/login")
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

# RUN
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port ,debug="True")
