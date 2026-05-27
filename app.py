from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# मेसेज साठवण्यासाठी तात्पुरती लिस्ट
messages = []

@app.route('/')
def home():
    # हा तुझा पहिला ओरिजिनल चॅट स्क्रीनचा कोड आहे
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VIP Chat Room</title>
        <style>
            body { background: #000; color: #fff; font-family: Arial; text-align: center; padding: 20px; }
            #chat { border: 1px solid #ff2a75; height: 300px; overflow-y: auto; padding: 10px; margin-bottom: 10px; border-radius: 10px; }
            input { padding: 10px; width: 60%; background: #111; color: #fff; border: 1px solid #ff2a75; border-radius: 5px; }
            button { padding: 10px 20px; background: #ff2a75; border: none; color: #fff; border-radius: 5px; cursor: pointer; }
        </style>
    </head>
    <body>
        <h2>❤️ VIP ROOM: 50501</h2>
        <div id="chat"></div>
        <input type="text" id="msg" placeholder="मेसेज टाईप करा...">
        <button onclick="send()">Send</button>

        <script>
            function loadMessages() {
                fetch('/get-messages')
                .then(res => res.json())
                .then(data => {
                    const chat = document.getElementById('chat');
                    chat.innerHTML = data.map(m => `<div><b>${m.user}:</b> ${m.text}</div>`).join('');
                });
            }
            function send() {
                const msg = document.getElementById('msg').value;
                if(!msg) return;
                fetch('/send-message', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: msg, user: 'User'})
                }).then(() => {
                    document.getElementById('msg').value = '';
                    loadMessages();
                });
            }
            setInterval(loadMessages, 2000); // दर २ सेकंदाला मेसेज रिफ्रेश होणार
        </script>
    </body>
    </html>
    '''

@app.route('/get-messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    messages.append({'user': data.get('user', 'Guest'), 'text': data.get('text', '')})
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
