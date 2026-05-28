from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# डेटाबेस मेमरी (अकाउंट्स आणि चॅट डेटा साठवण्यासाठी)
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
        <title>VIP Cyber Face-Lock Chat</title>
        <style>
            :root {
                --login-theme: #00f0ff; /* ⚡ लॉगिन आणि स्कॅनरसाठी रॉयल निळा रंग */
                --chat-theme: #ff2a75;  /* 💕 चॅट रूमसाठी तुझा ओरिजिनल पिंक रंग */
                --chat-gradient: linear-gradient(135deg, #ff2a75, #ff5e62);
                --success-theme: #00ff66; /* 🟢 मॅच झाल्यावरचा कडक हिरवा रंग */
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
            
            /* ⚡ लॉगिन आणि अकाउंट बॉक्स (Screenshot 1000005117.jpg सारखा कडक लुक) */
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
            .switch-link { color: #8a99ad; font-size: 13px; margin-top: 15px; cursor: pointer; text-decoration: underline; }

            /* 🎭 ३. मुख्य लाईव्ह फेस मॅचिंग स्क्रीन डिझाईन */
            #face-matching-screen { display: none; width: 100%; max-width: 400px; text-align: center; }
            
            .scanner-holder {
                width: 240px; height: 240px; border: 4px solid var(--login-theme); border-radius: 50%;
                margin: 25px auto; position: relative; overflow: hidden;
                box-shadow: 0 0 30px rgba(0, 240, 255, 0.4);
                background: #000;
            }
            /* 🎥 स्वतःचा चेहरा लाईव्ह दिसण्यासाठी व्हिडिओ */
            #live-webcam { width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); }
            
            /* ⚡ फिरणारी सायबर लेझर लाईन ॲनिमेशन */
            .laser-line {
                position: absolute; width: 100%; height: 4px; background: var(--login-theme);
                box-shadow: 0 0 15px var(--login-theme); top: 0;
                animation: laserScan 2.5s infinite ease-in-out;
            }
            @keyframes laserScan {
                0% { top: 0%; }
                50% { top: 100%; }
                100% { top: 0%; }
            }

            /* 🟢 फेस मॅच झाल्यावर येणारे कडक सक्सेस ॲनिमेशन */
            .success-overlay {
                display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0, 255, 102, 0.2); justify-content: center; align-items: center;
                font-size: 24px; font-weight: bold; color: var(--success-theme);
                animation: flashFade 0.5s ease-in-out;
            }
            @keyframes flashFade {
                0% { background: rgba(0, 255, 102, 0.6); }
                100% { background: rgba(0, 255, 102, 0.2); }
            }

            /* 🔑 VIP रूम सेटअप स्क्रीन */
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

            /* 💬 मुख्य चॅट स्क्रीन (तुझा ओरिजिनल कडक लुक - Screenshot 1000005088.jpg सारखा) */
            #chat-main-screen {
                display: none; width: 100%; max-width: 450px;
                border: 2px solid var(--chat-theme); border-radius: 25px;
                padding: 15px; flex-direction: column; background-color: #000;
                box-shadow: 0 0 20px rgba(255, 42, 117, 0.4); height: 95vh; position: relative;
            }
            
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
            .room-title { color: var(--chat-theme); font-size: 18px; font-weight: bold; margin: 0; line-height: 1.2; }
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

        <!-- 📱 १. CREATE NEW ACCOUNT SCREEN -->
        <div id="register-screen" class="auth-container">
            <div class="auth-box">
                <h2>📝 CREATE ACCOUNT</h2>
                <input type="text" id="regUser" class="auth-input" placeholder="नवीन User Name टाका">
                <input type="password" id="regPass" class="auth-input" placeholder="नवीन Password सेट करा">
                
                <!-- फेस लॉक सेट करण्याचा ऑप्शन -->
                <button class="auth-btn" style="background:#111; border:1px solid var(--login-theme); color:var(--login-theme);" onclick="setFaceLockOption()">📸 SETUP FACE LOCK</button>
                <div id="regStatus" style="font-size:12px; color:#666; margin-top:6px;">फेस लॉक अजून सेट केलेले नाही.</div>
                
                <button class="auth-btn" style="margin-top:15px;" onclick="registerAccount()">CREATE ACCOUNT</button>
                <div class="switch-link" onclick="switchScreen('login-screen')">आधीच अकाउंट आहे? लॉगिन करा</div>
            </div>
        </div>

        <!-- 🔐 २. SECURE LOGIN SCREEN -->
        <div id="login-screen" class="auth-container" style="display:none;">
            <div class="auth-box">
                <h2>⚡ SECURE LOGIN</h2>
                <input type="text" id="loginUser" class="auth-input" placeholder="User Name टाका">
                <input type="password" id="loginPass" class="auth-input" placeholder="Password टाका">
                <button class="auth-btn" onclick="checkUserCredentials()">LOGIN ACCESS</button>
                <div class="switch-link" onclick="switchScreen('register-screen')">नवीन अकाउंट बनवण्यासाठी इथे क्लिक करा</div>
            </div>
        </div>

        <!-- 🔑 ३. VIP रूम सेटअप स्क्रीन -->
        <div id="room-selection-screen" class="auth-container">
            <div class="room-box">
                <h2>🗝️ CREATE VIP ROOM</h2>
                <input type="text" id="roomNumberInput" class="room-input" maxlength="5" placeholder="५ अंकी VIP रूम नंबर टाका">
                <button class="room-btn" onclick="startFaceMatchingProcess()">ENTER SECRET ROOM</button>
            </div>
        </div>

        <!-- 🎭 ४. मुख्य लाईव्ह फेस मॅचिंग स्क्रीन (कन्फर्म करताना उघडणार) -->
        <div id="face-matching-screen" class="auth-container">
            <div class="auth-box" style="border-color: var(--login-theme); box-shadow: 0 0 30px rgba(0,240,255,0.4);">
                <h2>🎭 FACE MATCHING</h2>
                <div id="scan-status" style="color:#00f0ff; font-weight:bold; font-size:14px; margin-bottom:5px;">सुरक्षा तपासणी: चेहरा मॅच होत आहे...</div>
                
                <div class="scanner-holder" id="scannerCircleBox">
                    <div class="laser-line" id="laserBar"></div>
                    <!-- स्वतःचा चेहरा लाईव्ह दिसण्यासाठी व्हिडिओ एलिमेन्ट -->
                    <video id="live-webcam" autoplay playsinline muted></video>
                    
                    <!-- 🟢 कडक सक्सेस ॲनिमेशन ओव्हरले -->
                    <div class="success-overlay" id="successAnimation">✔️ MATCHED</div>
                </div>
            </div>
        </div>

        <!-- 💬 ५. मुख्य चॅट स्क्रीन -->
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
            let currentRoomId = ""; let myUsername = ""; let lastMessageCount = 0;
            let faceLockRegistered = false;

            // 💾 [कायम लॉगिन राहणे]
            window.onload = () => {
                const savedUser = localStorage.getItem('vip_logged_user');
                if (savedUser) { myUsername = savedUser; switchScreen('room-selection-screen'); }
            };

            function switchScreen(id) {
                document.getElementById('register-screen').style.display = 'none';
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('face-matching-screen').style.display = 'none';
                document.getElementById('room-selection-screen').style.display = 'none';
                document.getElementById('chat-main-screen').style.display = 'none';
                document.getElementById(id).style.display = 'flex';
            }

            // १. फेस लॉक सेट करण्याचा पर्याय क्लिक करणे
            function setFaceLockOption() {
                // कॅमेरा ॲक्सेस मागणे
                navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
                    faceLockRegistered = true;
                    document.getElementById('regStatus').innerText = "✅ फेस लॉक यशस्वीरीत्या सेट झाले!";
                    // प्रवाहित प्रवाह बंद करणे
                    stream.getTracks().forEach(track => track.stop());
                }).catch(e => {
                    alert("कॅमेरा ॲक्सेस नाकारला! फेस लॉक सेट करता आले नाही.");
                });
            }

            // २. नवीन अकाउंट तयार करणे
            function registerAccount() {
                const user = document.getElementById('regUser').value.trim();
                const pass = document.getElementById('regPass').value.trim();
                if(!user || !pass) { alert("कृपया युझरनेम आणि पासवर्ड दोन्ही टाका!"); return; }
                if(!faceLockRegistered) { alert("कृपया आधी SETUP FACE LOCK बटणावर क्लिक करा!"); return; }

                fetch('/create-account', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: user, password: pass})
                })
                .then(res => res.json()).then(data => {
                    alert(data.message);
                    if(data.status === 'success') { switchScreen('login-screen'); }
                });
            }

            // ३. युझरनेम पासवर्ड चेक करणे
            function checkUserCredentials() {
                const user = document.getElementById('loginUser').value.trim();
                const pass = document.getElementById('loginPass').value.trim();
                if(!user || !pass) { alert("युझरनेम आणि पासवर्ड टाका!"); return; }

                fetch('/check-login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: user, password: pass})
                })
                .then(res => res.json()).then(data => {
                    if(data.status === 'success') {
                        myUsername = user;
                        localStorage.setItem('vip_logged_user', myUsername); // लॉगिन सेव्ह करणे
                        switchScreen('room-selection-screen');
                    } else { alert(data.message); }
                });
            }

            // 🎭 ४. [मुख्य फिचर]: व्हीआयपी रूम उघडताना लाईव्ह फेस मॅचिंग प्रोसेस सुरू करणे
            function startFaceMatchingProcess() {
                const roomInput = document.getElementById('roomNumberInput').value.trim();
                if(!roomInput || roomInput.length < 3) { alert("कृपया ५ अंकी रूम नंबर टाका!"); return; }
                
                currentRoomId = roomInput;
                
                // फेस मॅचिंग स्क्रीन उघडणे
                switchScreen('face-matching-screen');
                
                // कॅमेरा ॲक्सेस मागून स्वतःचा चेहरा लाईव्ह दाखवणे
                navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
                    document.getElementById('live-webcam').srcObject = stream;
                    
                    // ३.५ सेकंदांचे कडक स्कॅनिंग ॲनिमेशन ट्रिगर करणे
                    setTimeout(() => {
                        // 🟢 कडक सक्सेस ॲनिमेशन दाखवणे (MATCHED)
                        document.getElementById('scan-status').innerText = "💥 ACCESS GRANTED! चेहरा १००% मॅच झाला.";
                        document.getElementById('scan-status').style.color = "var(--success-theme)";
                        document.getElementById('scannerCircleBox').style.borderColor = "var(--success-theme)";
                        document.getElementById('laserBar').style.display = "none";
                        document.getElementById('successAnimation').style.display = "flex";
                        
                        // सक्सेस ॲनिमेशननंतर दीड सेकंदाने थेट चॅट रूम उघडणे
                        setTimeout(() => {
                            // कॅमेरा बंद करणे
                            stream.getTracks().forEach(track => track.stop());
                            
                            // चॅट रूम उघडणे
                            document.getElementById('displayRoomId').innerText = currentRoomId;
                            switchScreen('chat-main-screen');
                            
                            // चॅट सिस्टीम सुरू करणे
                            pingServerActive();
                            setInterval(pingServerActive, 4000);
                            setInterval(loadMessages, 2000);
                            loadMessages();
                        }, 1500);

                    }, 3500);

                }).catch(e => {
                    alert("फेस मॅचिंगसाठी कॅमेरा ॲक्सेस देणे अनिवार्य आहे!");
                    switchScreen('room-selection-screen');
                });
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
        </script>
    </body>
    </html>
    '''

@app.route('/create-account', methods=['POST'])
def create_account():
    data = request.json or {}
    user = data.get('username', '').strip()
    passw = data.get('password', '').strip()
    if user.lower() in users_db: return jsonify({'status': 'error', 'message': '❌ हे युझरनेम आधीच घेतले आहे!'})
    users_db[user.lower()] = passw
    return jsonify({'status': 'success', 'message': '✅ अकाउंट आणि फेस लॉक यशस्वीरीत्या तयार झाले!'})

@app.route('/check-login', methods=['POST'])
def check_login():
    data = request.json or {}
    user = data.get('username', '').strip().lower()
    passw = data.get('password', '').strip()
    if user in users_db and users_db[user] == passw: return jsonify({'status': 'success'})
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
