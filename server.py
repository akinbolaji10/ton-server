from flask import Flask, request, jsonify
import psycopg2
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

@app.route("/")
def home():
    return "TON Payment Server is running!"

@app.route("/subscribe", methods=["POST"])
def subscribe_user():
    data = request.get_json()
    telegram_id = data.get("telegram_id")

    if not telegram_id:
        return jsonify({"error": "Missing telegram_id"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    now = datetime.utcnow()
    expiry = now + timedelta(days=30)

    cur.execute(
        "INSERT INTO subscriptions (telegram_id, start_date, expiry_date) VALUES (%s, %s, %s) ON CONFLICT (telegram_id) DO UPDATE SET start_date = %s, expiry_date = %s",
        (telegram_id, now, expiry, now, expiry)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Subscription activated successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
