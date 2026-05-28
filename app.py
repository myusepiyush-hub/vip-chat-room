from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# युझरचे फिक्स अकाउंट्स आणि चॅट डेटा मेमरी (Database Memory)
# तुम्ही आणि तुमची पार्टनर लॉगिन करण्यासाठी हे दोन आयडी वापरू शकता:
users_db = {
    "piyush": "12345",   # तुमचे युझरनेम आणि पासवर्ड
    "vipuser": "54321"   # पार्टनरचे युझरनेम आणि पासवर्ड
}
room_data = {}

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VIP Chat Hub</title>
        <style>
            :root {
                --login-theme: #00f0ff; /* ⚡ लॉगिन पेजसाठी रॉयल निळा/सायन रंग */
                --chat-theme: #ff2a75;  /* 💕 चॅट रूमसाठी तुझा ओरिजिनल पिंक रंग */
                --chat-gradient: linear-gradient(135deg, #ff2a75, #ff5e62);
            }

            body {
                background-color: #030308; color: #fff;
                font-family: Arial, sans-serif; margin: 0; padding: 10px;
                display: flex; justify-content: center; height: 100vh; box-sizing: border-box;
            }

            .auth-container {
                width: 100%; max-width: 400px; display: flex; flex-direction: column;
                justify-content: center; align-items: center; height: 90vh;
            }
            
            /* ⚡ १. नवीन डार्क रॉयल निळा लॉगिन बॉक्स (Screenshot 1000005114.jpg सारखा) */
            .auth-box {
                border: 2px solid var(--login-theme); padding: 35px 20px; border-radius: 30px;
                text-align: center; box-shadow: 0 0 25px rgba(0, 240, 255, 0.3);
                background-color: #060814; width: 90%;
            }
            .auth-box h2 { color: var(--login-theme); margin: 0 0 20px 0; font-size: 24px; font-weight: bold; letter-spacing: 1px; }
            
            .auth-input {
                width: 85%; padding: 12px; font-size: 16px; text-align: center;
                background: #000; border: 1px solid var(--login-theme); color: #fff; border-radius: 15px; margin-bottom: 15px; outline: none;
            }
            .auth-btn {
                background: linear-gradient(135deg, #0072ff, #00f0ff); border: none; color: black;
                padding: 12px 25px; font-size: 16px; font-weight: bold; border-radius: 15px; cursor: pointer; width: 90%; margin-top: 5px;
            }

            /* 🔑 २. VIP रूम बनवण्याची दुसरी कडक स्क्रीन */
            #room-selection-screen {
                display: none; width: 100%; max-width: 400px; 
                flex-direction: column; justify-content: center; align-items: center; height: 90vh;
            }
            .room-box {
                border: 2px solid var(--chat-theme); padding: 35px 20px; border-radius: 25px; text-align: center;
                box-shadow: 0 0 25px rgba(255, 42, 117, 0.4); background-color: #050505; width: 90%;
            }
            .room-box h2 { color: var(--chat-theme); margin-bottom: 20px; font-size: 22px; }
            .room-input {
                width: 85%; padding: 12px; font-size: 16px; text-align: center;
                background: #000; border: 1px solid var(--chat-theme); color: #fff; border-radius: 15px; margin-bottom: 20px; outline: none;
            }
            .room-btn {
                background: var(--chat-gradient); border: none; color: white;
                padding: 12px 30px; font-size: 16px; font-weight: bold; border-radius: 15px; cursor: pointer; width: 90%;
            }

            /* 💬 ३. मुख्य चॅट स्क्रीन (तुझा ओरिजिनल कडक लुक) */
            #chat-main-screen {
                display: none; width: 100%; max-width: 450px;
                border: 2px solid var(--chat-theme); border-radius: 25px;
                padding: 15px; flex-direction: column; background-color: #000;
                box-shadow: 0 0 20px rgba(255, 42, 117, 0.4); height: 95vh; position: relative;
            }
            
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
            .room-title { color: var(--chat-theme); font-size: 16px; font-weight: bold; margin: 0; line-height: 1.2; }
            .header-buttons { display: flex; gap: 8px; align-items: center; }
            .clear-btn { background-color: var(--chat-theme); border: none; color: white; padding: 6px 14px; border-radius: 15px; font-weight: bold; cursor: pointer; font-size: 14px; }
            .online-box { border: 1px solid var(--chat-theme); border-radius: 15px; padding: 5px 12px; font-size: 12px; text-align: center; min-width: 50px; }
            .call-btn { background: linear-gradient(45deg, #00ffcc, #00ee99); border: none; color: #000; padding: 6px 12px; border-radius: 15px; font-weight: bold; cursor: pointer; font-size: 14px; }
            
            #chat-box { flex: 1; border: 1px solid var(--chat-theme); border-radius: 15px; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; margin-bottom: 15px; background-color: #050505; }
            .encrypt-tag { text-align: center; color: #444; font-size: 11px; font-style: italic; margin: 5px auto; background: #090909; padding: 5px 12px; border-radius: 20px; border: 1px dashed #333; width: fit-content; }
            
            .msg { padding: 12px 18px; border-radius: 18px; max-width: 75%; font-size: 16px; word-wrap: break-word; }
            .opp-msg { background-color: #1a1a1a; color: #fff; align-self: flex-start; border: 1px solid var(--chat-theme); }
            .my-msg { background: var(--chat-gradient); color: #fff; align-self: flex-end; }
            .msg-user { font-size: 11px; color: var(--chat-theme); margin-bottom: 4px; display: block; font-weight: bold; }
            
            .input-container { display: flex; gap: 10px; align-items: center; margin-bottom: 5px; }
            .chat-input-field { flex: 1; padding: 12px 15px; background-color: #090909; color: #fff; border: 1px solid var(--chat-theme); border-radius: 15px; font-size: 16px; outline: none; }
            .send-btn { background-color: var(--chat-theme); border: none; color: white; padding: 12px 22px; border-radius: 15px; font-weight: bold; font-size: 16px; cursor: pointer; }
            .footer-text { text-align: center; color: var(--chat-theme); font-size: 12px; margin-top: 5px; font-weight: bold; }
        </style>
    </head>
    <body>

        <!-- ⚡ १. मुख्य लॉगिन स्क्रीन (नवीन कडक डार्क रॉयल निळा लुक) -->
        <div id="login-screen" class="auth-container">
            <div class="auth-box">
                <h2>⚡ SECURE LOGIN</h2>
                <input type="text" id="loginUser" class="auth-input" placeholder="User Name टाका">
                <input type="password" id="loginPass" class="auth-input" placeholder="Password टाका">
                <button class="auth-btn" onclick="checkAppLogin()">LOGIN ACCESS</button>
            </div>
        </div>

        <!-- 🔑 २. व्हीआयपी रूम सेटअप स्क्रीन (लॉगिन झाल्यावरच उघडणार) -->
        <div id="room-selection-screen" class="auth-container">
            <div class="room-box">
                <h2>🗝️ CREATE VIP ROOM</h2>
                <input type="text" id="roomNumberInput" class="room-input" maxlength="5" placeholder="५ अंकी VIP रूम नंबर टाका">
                <button class="room-btn" onclick="joinRoom()">ENTER SECRET ROOM</button>
            </div>
        </div>

        <!-- 💬 ३. मुख्य चॅट स्क्रीन -->
        <div id="chat-main-screen">
            <div class="header">
                <div class="room-title">❤️ VIP ROOM:<br><span id="displayRoomId">XXXXX</span></div>
                <div class="header-buttons">
                    <button class="call-btn" onclick="startVideoCall()">📹 Call</button>
                    <button class="clear-btn" onclick="clearChat()">Clear</button>
                    <div class="online-box">Online:<br><span id="onlineCount">1</span></div>
                </div>
            </div>

            <div id="chat-box">
                <div class="encrypt-tag">🔐 End-to-End Encrypted VIP Chat</div>
            </div>

            <div class="input-container">
                <input type="text" id="msgInput" class="chat-input-field" placeholder="मेसेज टाईप करा...">
                <button class="send-btn" onclick="send()">Send</button>
            </div>

            <div class="footer-text">Website Created by Piyush Patil</div>
        </div>

        <script>
            let currentRoomId = "";
            let myUsername = "";
            let lastMessageCount = 0;

            // १. लॉगिन पासवर्ड चेक करणे
            function checkAppLogin() {
                const user = document.getElementById('loginUser').value.trim();
                const pass = document.getElementById('loginPass').value.trim();

                if(!user || !pass) { alert("कृपया नाव आणि पासवर्ड दोन्ही टाका!"); return; }

                fetch('/app-login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: user, password: pass})
                })
                .then(res => res.json())
                .then(data => {
                    if(data.status === 'success') {
                        myUsername = user;
                        // लॉगिन स्क्रीन लपवून रूम सेटअप स्क्रीन उघडणे
                        document.getElementById('login-screen').style.display = 'none';
                        document.getElementById('room-selection-screen').style.display = 'flex';
                    } else {
                        alert(data.message);
                    }
                });
            }

            // २. ५ अंकी गुप्त रूम नंबर टाकून चॅट उघडणे
            function joinRoom() {
                const roomInput = document.getElementById('roomNumberInput').value.trim();
                if(!roomInput || roomInput.length < 3) { alert("कृपया अचूक रूम नंबर टाका!"); return; }
                
                currentRoomId = roomInput;
                document.getElementById('displayRoomId').innerText = currentRoomId;
                
                document.getElementById('room-selection-screen').style.display = 'none';
                document.getElementById('chat-main-screen').style.display = 'flex';
                
                pingServerActive();
                setInterval(pingServerActive, 4000);
                setInterval(loadMessages, 2000);
                loadMessages();
            }

            function pingServerActive() {
                fetch('/ping', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({room: currentRoomId, user: myUsername}) })
                .then(res => res.json()).then(data => { document.getElementById('onlineCount').innerText = data.online_count; });
            }

            function loadMessages() {
                fetch('/get-messages?room=' + currentRoomId).then(res => res.json()).then(data => {
                    const chatBox = document.getElementById('chat-box');
                    chatBox.innerHTML = data.map(m => {
                        const isMe = m.user.toLowerCase() === myUsername.toLowerCase();
                        const msgClass = isMe ? 'my-msg' : 'opp-msg';
                        const nameLabel = isMe ? '' : `<span class="msg-user">${m.user}</span>`;
                        return `<div class="msg ${msgClass}">${nameLabel}${m.text}</div>`;
                    }).join('');
                    if(data.length > lastMessageCount) { chatBox.scrollTop = chatBox.scrollHeight; lastMessageCount = data.length; }
                });
            }

            function send() {
                const input = document.getElementById('msgInput'); const text = input.value.trim(); if(!text) return;
                fetch('/send-message', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({text: text, user: myUsername, room: currentRoomId}) }).then(() => { input.value = ''; loadMessages(); });
            }

            function clearChat() { if(confirm("या रूमचे सर्व चॅट डिलीट करायचे आहे का?")) { fetch('/clear-messages', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({room: currentRoomId}) }).then(() => { lastMessageCount = 0; loadMessages(); }); } }
            function startVideoCall() { window.open("https://meet.jit.si/PiyushVipSecretRoom_" + currentRoomId, '_blank'); }
            document.getElementById("msgInput").addEventListener("keyup", function(event) { if (event.key === "Enter") { send(); } });
        </script>
    </body>
    </html>
    '''

@app.route('/app-login', methods=['POST'])
def app_login():
    data = request.json or {}
    user = data.get('username', '').strip().lower()
    passw = data.get('password', '').strip()
    
    if user in users_db and users_db[user] == passw:
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': '❌ चुकीचे युझरनेम किंवा पासवर्ड!'})

@app.route('/ping', methods=['POST'])
def ping_user():
    data = request.json or {}
    room = data.get('room', 'default')
    user = data.get('user', 'Unknown')
    if room not in room_data: room_data[room] = {'messages': [], 'users': {}}
    room_data[room]['users'][user] = True
    return jsonify({'status': 'success', 'online_count': len(room_data[room]['users'])})

@app.route('/get-messages', methods=['GET'])
def get_messages():
    room = request.args.get('room', 'default')
    return jsonify(room_data[room]['messages'] if room in room_data else [])

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json or {}
    if data.get('text'):
        room = data.get('room', 'default')
        if room not in room_data: room_data[room] = {'messages': [], 'users': {}}
        room_data[room]['messages'].append({'user': data.get('user'), 'text': data.get('text')})
    return jsonify({'status': 'success'})

@app.route('/clear-messages', methods=['POST'])
def clear_messages():
    data = request.json or {}
    room = data.get('room', 'default')
    if room in room_data: room_data[room]['messages'] = []
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
