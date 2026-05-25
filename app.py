from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>VIP Chat Room</title>
    <style>
        body { background: #1a1a1a; color: #ffd700; font-family: Arial; text-align: center; padding: 20px; }
        #chat-box { width: 100%; max-width: 400px; height: 300px; border: 2px solid #ffd700; margin: auto; overflow-y: scroll; padding: 10px; background: #000; }
        button { padding: 10px; margin: 5px; background: #ffd700; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>VIP Chat Room 👑</h1>
    <div id="chat-box"></div>
    <input type="text" id="msg" placeholder="मॅसेज...">
    <button onclick="send()">पाठवा</button>
    <br>
    <button onclick="call()">📞 कॉल करा</button>
    <script>
        function send() {
            let msg = document.getElementById('msg').value;
            fetch('/send', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({sender: 'Piyush', message: msg})}).then(() => location.reload());
        }
        function call() { alert("कॉल लावला जात आहे... (येथे व्हिडिओ कॉल लिंक जोडा)"); }
        setInterval(() => {
            fetch('/get').then(res => res.json()).then(data => {
                document.getElementById('chat-box').innerHTML = data.messages.map(m => `<p>${m.sender}: ${m.message}</p>`).join('');
            });
        }, 1000);
    </script>
</body>
</html>
"""

messages = []

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/send', methods=['POST'])
def send():
    messages.append(request.json)
    return jsonify({"status": "success"})

@app.route('/get')
def get():
    return jsonify({"messages": messages})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
