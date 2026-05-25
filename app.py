from flask import Flask, request, jsonify
import os

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome Piyush Website ❤️</title>
    <style>
        body { background: linear-gradient(45deg, #2b0000, #000000); color: white; font-family: sans-serif; margin: 0; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        #login-screen { text-align: center; padding: 20px; border: 1px solid #ff4d4d; border-radius: 20px; }
        button { padding: 10px 20px; background: #ff4d4d; color: white; border: none; border-radius: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <div id="login-screen">
        <h1>Welcome Piyush Website 💕</h1>
        <p>सिक्रेट लव्ह चॅट</p>
    </div>
</body>
</html>
"""

rooms_data = {}

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/send', methods=['POST'])
def send_msg():
    data = request.json
    room = data.get('room')
    if room not in rooms_data:
        rooms_data[room] = {'messages': [], 'call': None}
    rooms_data[room]['messages'].append({"sender": data.get('sender'), "message": data.get('message')})
    return jsonify({"status": "success"})

@app.route('/get/<room>')
def get_msg(room):
    if room not in rooms_data:
        return jsonify({"messages": [], "call": None})
    return jsonify({"messages": rooms_data[room]['messages'], "call": rooms_data[room]['call']})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
