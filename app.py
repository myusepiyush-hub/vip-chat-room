from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# सर्व डेटा थेट रेंडर सर्व्हरच्या स्वतःच्या मेमरीमध्ये सुरक्षित राहील
rooms_data = {}

HTML_CODE = '''
<!DOCTYPE html>
<html lang="mr">
<head>
    <meta charset="UTF-8">
    <title>Lovers VIP Secret Chat</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { 
            box-sizing: border-box; 
            margin: 0; padding: 0; 
            -webkit-user-select: none;
            user-select: none;
        }
        body {
            background: #000000; /* संपूर्ण कडक काळा बॅकग्राउंड */
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 15px;
        }
        .chat-container {
            width: 100%;
            max-width: 480px;
            background: #000000; 
            border: 2px solid #ff2a5f;
            border-radius: 20px;
            box-shadow: 0 0 35px rgba(255, 42, 95, 0.4);
            display: flex;
            flex-direction: column;
            height: 85vh;
            position: relative;
        }
        .chat-header {
            background: #0a0507;
            padding: 15px;
            border-bottom: 1px solid #ff2a5f;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top-left-radius: 18px;
            border-top-right-radius: 18px;
        }
        .chat-title {
            font-size: 1.1rem;
            font-weight: bold;
            color: #ff2a5f;
            text-shadow: 0 0 10px rgba(255, 42, 95, 0.5);
        }
        .header-actions {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .online-status {
            background: rgba(255, 42, 95, 0.15);
            color: #ff2a5f;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85rem;
            font-weight: bold;
            border: 1px solid #ff2a5f;
        }
        .messages-box {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
            background: #000000;
        }
        .msg {
            max-width: 75%;
            padding: 11px 15px;
            border-radius: 15px;
            font-size: 1rem;
            line-height: 1.4;
            word-wrap: break-word;
        }
        /* तुमचा स्वतःचा मेसेज (गुलाबी निऑन पट्टी + पांढरा मजकूर) */
        .msg.sent {
            background: linear-gradient(135deg, #ff2a5f 0%, #ff5e3a 100%);
            color: #ffffff !important;
            align-self: flex-end;
            border-bottom-right-radius: 2px;
            box-shadow: 0 2px 8px rgba(255, 42, 95, 0.3);
        }
        /* पार्टनरचा मेसेज (डार्क ग्रे पट्टी + पांढरा मजकूर) */
        .msg.received {
            background: #1a1a1a;
            color: #ffffff !important;
            align-self: flex-start;
            border-bottom-left-radius: 2px;
            border: 1px solid #ff2a5f;
        }
        .input-area {
            padding: 15px;
            background: #0a0507;
            border-top: 1px solid #ff2a5f;
            display: flex;
            gap: 10px;
            border-bottom-left-radius: 18px;
            border-bottom-right-radius: 18px;
        }
        input[type="text"], input[type="number"] {
            flex: 1;
            padding: 12px;
            background: #000000;
            border: 1px solid #ff2a5f;
            color: #ffffff;
            border-radius: 10px;
            outline: none;
            font-size: 1rem;
        }
        .send-btn {
            background: #ff2a5f;
            color: #ffffff;
            border: none;
            padding: 0 22px;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
        }
        .login-box {
            width: 100%;
            max-width: 400px;
            background: #000000;
            border: 2px solid #ff2a5f;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 0 35px rgba(255, 42, 95, 0.35);
        }
        .login-box h1 {
            color: #ff2a5f;
            margin-bottom: 10px;
        }
        .update-badge {
            display: inline-block;
            background: rgba(34, 197, 94, 0.15);
            color: #22c55e;
            border: 1px solid #22c55e;
            padding: 5px 12px;
            font-size: 0.8rem;
            font-weight: bold;
            border-radius: 20px;
            margin-bottom: 20px;
        }
        .credit-text {
            color: #ff2a5f;
            font-size: 0.9rem;
            font-weight: bold;
            margin-top: 20px;
        }
    </style>
</head>
<body>

<!-- LOGIN SCREEN -->
<div class="login-box" id="loginScreen">
    <div class="update-badge">🟢 INSTANT DISPLAY SYSTEM (VER 4.0)</div>
    <h1>❤️ LOVERS VIP CHAT ❤️</h1>
    <p style="color: #a1979b; margin-bottom: 25px;">गुप्त व्हीआयपी रूमसाठी खाली कोणताही ५ अंकी कोड टाका. पार्टनरलाही तोच कोड टाकायला सांगा!</p>
    <input type="number" id="secretCode" placeholder="५ अंकी कोड टाका" style="width:100%; padding:12px; margin-bottom:15px; background:#000000; border:1px solid #ff2a5f; color:#ff2a5f; border-radius:10px; text-align:center; font-weight:bold; font-size:1.2rem;">
    <button class="send-btn" style="width:100%; padding:12px;" onclick="joinChat()">रूममध्ये प्रवेश करा ➔</button>
    <div class="credit-text">Website Created by Piyush Patil</div>
</div>

<!-- MAIN CHAT SCREEN -->
<div class="chat-container" id="chatScreen" style="display: none;">
    <div class="chat-header">
        <div class="chat-title" id="roomTitle">❤️ ROOM</div>
        <div class="header-actions">
            <button class="send-btn" style="padding:4px 10px; font-size:0.8rem;" onclick="clearChat()">Clear</button>
            <div class="online-status" id="onlineCount">Online: 1</div>
        </div>
    </div>
    <div class="messages-box" id="msgBox"></div>
    <div class="input-area">
        <input type="text" id="msgInput" placeholder="मेसेज टाईप करा..." onkeypress="if(event.key==='Enter') sendMsg()">
        <button class="send-btn" onclick="sendMsg()">Send</button>
    </div>
    <div class="credit-text" style="text-align: center; margin: 5px 0; font-size: 0.75rem;">Website Created by Piyush Patil</div>
</div>

<script>
    let mySecretCode, randomUserID;
    let localMessages = []; // स्वतःचे मेसेज ट्रॅक करण्यासाठी लोकल एरे

    function joinChat() {
        mySecretCode = document.getElementById('secretCode').value.trim();
        if(mySecretCode.length !== 5) { alert("कृपया बरोबर ५ अंकी कोड टाका भावा!"); return; }
        
        randomUserID = "User-" + Math.floor(1000 + Math.random() * 9000);
        document.getElementById('loginScreen').style.display = 'none';
        document.getElementById('chatScreen').style.display = 'flex';
        document.getElementById('roomTitle').innerText = "❤️ VIP ROOM: " + mySecretCode;

        // दर १ सेकंदाला बॅकग्राउंडला मेसेज आणि ऑनलाईन लोक अपडेट करणे
        setInterval(fetchMessages, 1000);
        setInterval(pingPresence, 1000);
    }

    function sendMsg() {
        const input = document.getElementById('msgInput');
        const text = input.value.trim();
        if(!text) return;

        // 💥 झटका सिस्टीम: सर्व्हरवर जाण्याआधी मेसेज आधी स्वतःच्या स्क्रीनवर दाखवणे 💥
        const msgBox = document.getElementById('msgBox');
        const msgDiv = document.createElement('div');
        msgDiv.className = 'msg sent';
        msgDiv.innerText = text;
        msgBox.appendChild(msgDiv);
        msgBox.scrollTop = msgBox.scrollHeight;

        // लोकल रेकॉर्डमध्ये सेव्ह करणे जेणेकरून रिफ्रेश होताना डबल दिसणार नाही
        localMessages.push({sender: randomUserID, text: text});

        // सर्व्हरवर मेसेज पाठवणे
        fetch('/send', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ room: mySecretCode, sender: randomUserID, text: text })
        });
        
        input.value = "";
    }

    function fetchMessages() {
        fetch('/get?room=' + mySecretCode)
        .then(res => res.json())
        .then(data => {
            const msgBox = document.getElementById('msgBox');
            
            // जर सर्व्हर रिकामी असेल (Clear दाबल्यावर) तर लोकल मेसेज साफ करणे
            if (data.messages.length === 0) {
                msgBox.innerHTML = "";
                localMessages = [];
                return;
            }

            // फक्त नवीन किंवा पार्टनरचे मेसेजेस बॉक्समध्ये जोडणे
            // स्क्रीन सारखी साफ न करता फक्त नवीन मेसेज अपेंड करणे
            data.messages.forEach((msg, index) => {
                // जर हा मेसेज आधीच स्क्रीनवर नसेल तरच दाखवणे
                if (index >= msgBox.children.length) {
                    const msgDiv = document.createElement('div');
                    msgDiv.className = (msg.sender === randomUserID) ? 'msg sent' : 'msg received';
                    msgDiv.innerText = msg.text;
                    msgBox.appendChild(msgDiv);
                    msgBox.scrollTop = msgBox.scrollHeight;
                }
            });
        });
    }

    function pingPresence() {
        fetch('/ping', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ room: mySecretCode, user: randomUserID })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('onlineCount').innerText = "Online: " + data.online;
        });
    }

    function clearChat() {
        fetch('/clear', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ room: mySecretCode })
        });
    }
</script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    room = data.get('room')
    if room not in rooms_data:
        rooms_data[room] = {'messages': [], 'users': {}}
    rooms_data[room]['messages'].append({'sender': data.get('sender'), 'text': data.get('text')})
    return jsonify({'status': 'ok'})

@app.route('/get', methods=['GET'])
def get_messages():
    room = request.args.get('room')
    messages = rooms_data.get(room, {}).get('messages', [])
    return jsonify({'messages': messages})

@app.route('/ping', methods=['POST'])
def ping():
    import time
    data = request.json
    room = data.get('room')
    user = data.get('user')
    now = time.time()
    
    if room not in rooms_data:
        rooms_data[room] = {'messages': [], 'users': {}}
        
    rooms_data[room]['users'][user] = now
    active_users = [u for u, t in rooms_data[room]['users'].items() if now - t < 3]
    rooms_data[room]['users'] = {u: t for u, t in rooms_data[room]['users'].items() if now - t < 3}
    
    return jsonify({'online': len(active_users)})

@app.route('/clear', methods=['POST'])
def clear_room():
    data = request.json
    room = data.get('room')
    if room in rooms_data:
        rooms_data[room]['messages'] = []
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
