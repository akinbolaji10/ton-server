from flask import Flask, request, jsonify
import psycopg2_binary  # Corrected import
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return psycopg2_binary.connect(  # Corrected usage
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

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if user already exists
        cur.execute("SELECT * FROM users WHERE telegram_id = %s", (telegram_id,))
        user = cur.fetchone()

        expiry_date = (datetime.utcnow() + timedelta(days=30)).date()

        if user:
            # Update subscription for existing user
            cur.execute("""
                UPDATE users
                SET subscription_active = TRUE,
                    subscription_expiry = %s
                WHERE telegram_id = %s
            """, (expiry_date, telegram_id))
        else:
            # Insert new user with default values for all required columns
            cur.execute("""
                INSERT INTO users (
                    telegram_id, username, subscription_active, subscription_expiry,
                    interactions_today, comments_today, likes_today, retweets_today
                )
                VALUES (%s, %s, TRUE, %s, 0, 0, 0, 0)
            """, (telegram_id, 'new_user', expiry_date))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "message": f"✅ Subscription activated for {telegram_id} until {expiry_date}",
            "status": "ok"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
