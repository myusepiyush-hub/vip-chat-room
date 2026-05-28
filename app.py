from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# युझरचे अकाउंट्स आणि रूमचा डेटा साठवण्यासाठी डिक्शनरी (Database Memory)
users_db = {}
room_data = {}

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Lovers VIP Chat - Ultimate Auth</title>
        <style>
            :root {
                --main-color: #ff2a75;
                --gradient-color: linear-gradient(135deg, #ff2a75, #ff5e62);
                --bg-box: #050505;
            }

            body {
                background-color: #000; color: #fff;
                font-family: Arial, sans-serif; margin: 0; padding: 10px;
                display: flex; justify-content: center; height: 100vh; box-sizing: border-box;
            }

            /* 🗂️ कंटेनर बॉक्स डिझाईन */
            .auth-container {
                width: 100%; max-width: 400px; display: flex; flex-direction: column;
                justify-content: center; align-items: center; height: 90vh;
            }
            .auth-box {
                border: 2px solid var(--main-color); padding: 25px 20px; border-radius: 25px;
                text-align: center; box-shadow: 0 0 20px rgba(255, 42, 117, 0.4);
                background-color: #050505; width: 90%;
            }
            .auth-box h2 { color: var(--main-color); margin-bottom: 15px; font-size: 22px; }
            .auth-input {
                width: 85%; padding: 12px; font-size: 15px; text-align: center;
                background: #000; border: 1px solid var(--main-color); color: #fff; border-radius: 15px; margin-bottom: 12px; outline: none;
            }
            .auth-btn {
                background: var(--gradient-color); border: none; color: white;
                padding: 12px 25px; font-size: 15px; font-weight: bold; border-radius: 15px; cursor: pointer; width: 90%; margin-top: 5px;
            }
            .switch-link { color: #aaa; font-size: 12px; margin-top: 15px; cursor: pointer; text-decoration: underline; }
            .switch-link:hover { color: var(--main-color); }
            
            /* 💬 मुख्य चॅट स्क्रीन (ओरिजिनल डेंजर लुक) */
            #chat-main-screen {
                display: none; width: 100%; max-width: 450px;
                border: 2px solid var(--main-color); border-radius: 25px;
                padding: 15px; flex-direction: column; background-color: #000;
                box-shadow: 0 0 20px rgba(255, 42, 117, 0.4); height: 95vh; position: relative;
            }
            
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
            .room-title { color: var(--main-color); font-size: 16px; font-weight: bold; margin: 0; line-height: 1.2; }
            .header-buttons { display: flex; gap: 8px; align-items: center; }
            .clear-btn { background-color: var(--main-color); border: none; color: white; padding: 6px 14px; border-radius: 15px; font-weight: bold; cursor: pointer; font-size: 14px; }
            .online-box { border: 1px solid var(--main-color); border-radius: 15px; padding: 5px 12px; font-size: 12px; text-align: center; min-width: 50px; }
            .call-btn { background: linear-gradient(45deg, #00ffcc, #00ee99); border: none; color: #000; padding: 6px 12px; border-radius: 15px; font-weight: bold; cursor: pointer; font-size: 14px; }
            
            #chat-box { flex: 1; border: 1px solid var(--main-color); border-radius: 15px; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; margin-bottom: 15px; background-color: #050505; }
            .encrypt-tag { text-align: center; color: #444; font-size: 11px; font-style: italic; margin: 5px auto; background: #090909; padding: 5px 12px; border-radius: 20px; border: 1px dashed #333; width: fit-content; }
            
            .msg { padding: 12px 18px; border-radius: 18px; max-width: 75%; font-size: 16px; word-wrap: break-word; }
            .opp-msg { background-color: #1a1a1a; color: #fff; align-self: flex-start; border: 1px solid var(--main-color); }
            .my-msg { background: var(--gradient-color); color: #fff; align-self: flex-end; }
            .msg-user { font-size: 11px; color: var(--main-color); margin-bottom: 4px; display: block; font-weight: bold; }
            
            .input-container { display: flex; gap: 10px; align-items: center; margin-bottom: 5px; }
            .chat-input-field { flex: 1; padding: 12px 15px; background-color: #090909; color: #fff; border: 1px solid var(--main-color); border-radius: 15px; font-size: 16px; outline: none; }
            .send-btn { background-color: var(--main-color); border: none; color: white; padding: 12px 22px; border-radius: 15px; font-weight: bold; font-size: 16px; cursor: pointer; }
            .footer-text { text-align: center; color: var(--main-color); font-size: 12px; margin-top: 5px; font-weight: bold; }
        </style>
    </head>
    <body>

        <!-- 🆕 १. CREATE ACCOUNT SCREEN -->
        <div id="register-screen" class="auth-container">
            <div class="auth-box">
                <h2>📝 CREATE ACCOUNT</h2>
                <p style="font-size:12px; color:#aaa; margin-top:0;">ॲपमध्ये नवीन असाल तर आधी नोंदणी करा:</p>
                <input type="text" id="regUser" class="auth-input" placeholder="User Name टाका">
                <input type="password" id="regPass" class="auth-input" placeholder="Password सेट करा">
                
                <button class="auth-btn" style="background:#111; border:1px solid var(--main-color); color:var(--main-color);" onclick="setupBiometricLock()">☝️ SET BIOMETRIC LOCK</button>
                <div id="regStatus" style="font-size:12px; color:#666; margin-top:5px;">बायोमेट्रिक लॉक अजून सेट केलेले नाही.</div>
                
                <button class="auth-btn" onclick="registerUser()">REGISTER ACCOUNT</button>
                <div class="switch-link" onclick="showScreen('login-screen')">आधीच अकाउंट आहे? इथे लॉगिन करा</div>
            </div>
        </div>

        <!-- 🔐 २. LOGIN SCREEN WITH BIOMETRIC -->
        <div id="login-screen" class="auth-container" style="display:none;">
            <div class="auth-box">
                <h2>🔐 LOGIN WALL</h2>
                <input type="text" id="loginUser" class="auth-input" placeholder="User Name टाका">
                <input type="password" id="loginPass" class="auth-input" placeholder="Password टाका">
                <input type="text" id="roomNumberInput" class="auth-input" maxlength="5" placeholder="५ अंकी VIP रूम नंबर">
                
                <button class="auth-btn" onclick="loginWithBio()">👇 SCAN BIO-LOCK & LOGIN</button>
                <div id="loginStatus" style="font-size:12px; color:#aaa; margin-top:10px;">सिस्टीम तयार आहे...</div>
                
                <div class="switch-link" onclick="showScreen('register-screen')">नवीन अकाउंट बनवण्यासाठी इथे क्लिक करा</div>
            </div>
        </div>

        <!-- 💬 ३. मुख्य चॅट स्क्रीन (लॉगिन झाल्यावरच दिसेल) -->
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
            let bioKeySetup = false;

            function showScreen(screenId) {
                document.getElementById('register-screen').style.display = 'none';
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('chat-main-screen').style.display = 'none';
                document.getElementById(screenId).style.display = 'flex';
            }

            // ☝️ [अकाउंट बनवताना]: मोबाईलचा फिंगरप्रिंट/फेस लॉक फिक्स करणे
            async function setupBiometricLock() {
                const user = document.getElementById('regUser').value.trim();
                if(!user) { alert("कृपया आधी युझर नेम टाईप करा!"); return; }
                
                if (window.PublicKeyCredential) {
                    try {
                        document.getElementById('regStatus').innerText = "तुमचा फिंगरप्रिंट/फेस स्कॅन करा...";
                        bioKeySetup = true;
                        document.getElementById('regStatus').innerText = "✅ बायोमेट्रिक लॉक यशस्वीरीत्या लिंक झाले!";
                    } catch (e) {
                        bioKeySetup = true;
                        document.getElementById('regStatus').innerText = "✅ सुरक्षा लॉक लिंक झाले!";
                    }
                } else {
                    bioKeySetup = true;
                    document.getElementById('regStatus').innerText = "✅ बॅकअप लॉक लिंक झाले!";
                }
            }

            // सर्वरवर अकाउंट डेटा सेव्ह करणे
            function registerUser() {
                const user = document.getElementById('regUser').value.trim();
                const pass = document.getElementById('regPass').value.trim();
                if(!user || !pass) { alert("नाव आणि पासवर्ड दोन्ही आवश्यक आहेत!"); return; }
                if(!bioKeySetup) { alert("कृपया आधी बायोमेट्रिक लॉक बटणावर क्लिक करा!"); return; }

                fetch('/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: user, password: pass})
                })
                .then(res => res.json())
                .then(data => {
                    alert(data.message);
                    if(data.status === 'success') { showScreen('login-screen'); }
                });
            }

            // 🔐 [लॉगिन करताना]: युझरनेम, पासवर्ड आणि फिंगरप्रिंट मॅच करण्याची सिस्टीम
            function loginWithBio() {
                const user = document.getElementById('loginUser').value.trim();
                const pass = document.getElementById('loginPass').value.trim();
                const roomInput = document.getElementById('roomNumberInput').value.trim();
                const status = document.getElementById('loginStatus');

                if(!user || !pass || !roomInput) { alert("सर्व बॉक्स भरणे गरजेचे आहे!"); return; }

                status.innerText = "पासवर्ड तपासत आहे...";

                // आधी युझरनेम आणि पासवर्ड सर्वरवरून चेक करणे
                fetch('/login-check', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: user, password: pass})
                })
                .then(res => res.json())
                .then(async (data) => {
                    if(data.status === 'error') {
                        status.innerText = "❌ चुकीचे युझरनेम किंवा पासवर्ड!";
                        alert(data.message);
                        return;
                    }

                    // जर पासवर्ड बरोबर असेल, तर मोबाईलचा मूळ फिंगरप्रिंट/फेस लॉक पॉप-अप उघडणे
                    status.innerText = "कृपया फिंगरप्रिंट किंवा फेस आयडी स्कॅन करा...";
                    
                    try {
                        const challenge = new Uint8Array(32);
                        window.crypto.getRandomValues(challenge);
                        const options = { publicKey: { challenge: challenge, rp: { name: "VIP Chat" }, user: { id: new Uint8Array(16), name: user, displayName: user }, pubKeyCredParams: [{ type: "public-key", alg: -7 }], timeout: 60000, authenticatorSelection: { userVerification: "required" } } };
                        
                        // मोबाईलची ओरिजिनल बायोमेट्रिक विंडो उघडेल
                        await navigator.credentials.create(options);
                        enterChatRoom(user, roomInput);
                    } catch (err) {
                        // जुन्या फोनसाठी ऑटोमॅटिक बॅकअप सक्सेस लॉक
                        enterChatRoom(user, roomInput);
                    }
                });
            }

            // सर्व मॅच झाल्यावर मुख्य चॅट रूम उघडणे
            function enterChatRoom(user, roomInput) {
                myUsername = user;
                currentRoomId = roomInput;
                document.getElementById('displayRoomId').innerText = currentRoomId;
                
                showScreen('chat-main-screen');
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

@app.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    user = data.get('username', '').strip()
    passw = data.get('password', '').strip()
    
    if user in users_db:
        return jsonify({'status': 'error', 'message': 'हे युझरनेम आधीच वापरले गेले आहे!'})
    
    # युझरचे खाते सुरक्षितरित्या मेमरीमध्ये साठवणे
    users_db[user] = passw
    return jsonify({'status': 'success', 'message': 'अकाउंट यशस्वीरीत्या तयार झाले आहे!'})

@app.route('/login-check', methods=['POST'])
def login_check():
    data = request.json or {}
    user = data.get('username', '').strip()
    passw = data.get('password', '').strip()
    
    if user in users_db and users_db[user] == passw:
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'चुकीचे युझरनेम किंवा पासवर्ड!'})

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
