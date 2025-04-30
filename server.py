from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is working!"

@app.route('/test')
def test():
    return "Test route is working!"

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    
    # Expecting: { "telegram_id": "123456789" }
    telegram_id = data.get("telegram_id")

    if not telegram_id:
        return jsonify({"error": "telegram_id is required"}), 400

    # TODO: Log or process the subscription trigger here
    print(f"Subscription request received for Telegram user: {telegram_id}")

    # For now, just simulate success
    return jsonify({"status": "ok", "message": f"Subscription request received for {telegram_id}"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
