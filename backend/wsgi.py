from dotenv import load_dotenv
import os

# Load environment variables before anything else
load_dotenv()

from main import app  # Import AFTER .env is loaded

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
