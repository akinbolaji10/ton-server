from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from your deployed server!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # <- use Render's port if available
    app.run(host="0.0.0.0", port=port)         # <- listen publicly, not just localhost
