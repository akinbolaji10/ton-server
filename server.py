from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv
import traceback

load_dotenv()

app = Flask(__name__)

# Database connection setup
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

@app.route('/')
def home():
    return 'TON Payment Server is running!'

@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        data = request.get_json()
        telegram_id = data.get('telegram_id')

        print("Received telegram_id:", telegram_id)

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO subscriptions (telegram_id, status, subscribed_at)
            VALUES (%s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (telegram_id)
            DO UPDATE SET status = EXCLUDED.status, subscribed_at = CURRENT_TIMESTAMP
        """, (telegram_id, 'active'))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": f"Subscription successful for ID {telegram_id}"}), 200

    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
