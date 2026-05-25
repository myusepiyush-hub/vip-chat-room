from flask import Flask, request, jsonify
import os

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Piyush Love Chat</title>
    <style>
        body { background: #000; color: white; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; padding: 20px; }
        #chat-box { width: 100%; max-width: 400px; height: 300px; border: 1px solid #ff4d4d; overflow-y: scroll; margin-bottom: 10px; padding: 10px; }
        input { width: 70%; padding: 10px; }
        button { padding: 10px; background: #ff4d4d; color: white; border: none; }
    </style>
</head>
<body>
    <h1>Piyush Love Chat 💕</h1>
    <div id="chat-box"></div>
    <div>
        <input type="text" id="msg" placeholder="मॅसेज लिहा...">
        <button onclick="send()">पाठवा</button>
    </div>
    <script>
        function send() {
            let msg = document.getElementById('msg').value;
            fetch('/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({sender: 'Piyush', message: msg, room: 'love'})
            }).then(() => location.reload());
        }
        setInterval(() => {
            fetch('/get/love').then(res => res.json()).then(data => {
                let box = document.getElementById('chat-box');
                box.innerHTML = data.messages.map(m => `<p><b>${m.sender}:</b> ${m.message}</p>`).join('');
            });
        }, 1000);
    </script>
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
    if room not in rooms_data: rooms_data[room] = {'messages': []}
    rooms_data[room]['messages'].append({"sender": data.get('sender'), "message": data.get('message')})
    return jsonify({"status": "success"})

@app.route('/get/<room>')
def get_msg(room):
    return jsonify({"messages": rooms_data.get(room, {}).get('messages', [])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
