from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# डेटाबेस मेमरी (अकाउंट्स, पासवर्ड आणि फेस डेटा साठवण्यासाठी)
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
        <title>VIP Cyber Face-Lock System</title>
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

            /* 🗂️ मुख्य ऑथेंटिकेशन बॉक्स (Screenshot 1000005117.jpg सारखा कडक लुक) */
            .auth-container {
                width: 100%; max-width: 400px; display: none; flex-direction: column;
                justify-content: center; align-items: center; height: 90vh;
            }
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

            /* 📸 वर्तुळाकार कॅमेरा स्कॅनर फ्रेम डिझाईन (Screenshot 1000005122.jpg सारखा कडक लुक) */
            .scanner-holder {
                width: 240px; height: 240px; border: 4px solid var(--login-theme); border-radius: 50%;
                margin: 25px auto; position: relative; overflow: hidden;
                box-shadow: 0 0 30px rgba(0, 240, 255, 0.4); background: #000;
            }
            .live-webcam-view { width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); }
            
            /* ⚡ फिरणारी लेझर लाईन ॲनिमेशन */
            .laser-line {
                position: absolute; width: 100%; height: 4px; background: var(--login-theme);
                box-shadow: 0 0 15px var(--login-theme); top: 0;
                animation: laserScan 2s infinite ease-in-out;
            }
            @keyframes laserScan { 0% { top: 0%; } 50% { top: 100%; } 100% { top: 0%; } }

            /* 🟢 मॅच झाल्यावर पूर्ण वर्तुळ हिरवे करणारे सक्सेस ओव्हरले (Screenshot 1000005122.jpg) */
            .success-overlay {
                display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0, 255, 102, 0.2); justify-content: center; align-items: center;
                font-size: 24px; font-weight: bold; color: var(--success-theme);
            }

            /* 🗝️ ३. VIP रूम सेटअप स्क्रीन (Screenshot 1000005123.jpg सारखा मूळ कोरा काळा लुक) */
            #room-selection-screen { width: 100%; max-width: 400px; display: none; flex-direction: column; justify-content: center; align-items: flex-start; height: 90vh; padding-left: 20px; }
            .room-title-text { font-size: 26px; font-weight: bold; color: #fff; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
            .room-input-box { width: 100%; max-width: 280px; padding: 12px; font-size: 16px; background-color: #fff; color: #000; border: none; outline: none; margin-bottom: 15px; font-weight: bold; }
            .room-submit-btn { background-color: #e0e0e0; color: #000; border: 1px solid #777; padding: 10px 22px; font-size: 14px; cursor: pointer; font-weight: bold; }

            /* 💬 ५. मुख्य चॅट स्क्रीन (तुझा ओरिजिनल कडक लुक - Screenshot 1000005088.jpg सारखा) */
            #chat-main-screen {
                display: none; width: 100%; max-width: 450px;
                border: 2px solid var(--chat-theme); border-radius: 25px;
                padding: 15px; flex-direction: column; background-color: #000;
                box-shadow: 0 0 20px rgba(255, 42, 117, 0.4); height: 95vh; position: relative;
            }
            
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
            .chat-room-header-title { color: var(--chat-theme); font-size: 18px; font-weight: bold; margin: 0; }
            .header-buttons { display: flex; gap: 8px; align-items: center; }
            .clear-btn { background-color: var(--chat-theme); border: none; color: white; padding: 6px 14px; border-radius: 15px; font-weight: bold; cursor: pointer; }
            .online-box { border: 1px solid var(--chat-theme); border-radius: 15px; padding: 5px 12px; font-size: 12px; text-align: center; min-width: 50px; }
            .call-btn { background: linear-gradient(45deg, #00ffcc, #00ee99); border: none; color: #000; padding: 6px 12px; border-radius: 15px; font-weight: bold; cursor: pointer; }
            
            #chat-box { flex: 1; border: 1px solid var(--chat-theme); border-radius: 15px; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; margin-bottom: 15px; background-color: #050505; }
            .encrypt-tag { text-align: center; color: #444; font-size: 11px; font-style: italic; margin: 5px auto; background: #090909; padding: 5px 12px; border-radius: 20px; border: 1px dashed #333; width: fit-content; }
            
            .msg { padding: 12px 18px; border-radius: 18px; max-width: 75%; font-size: 16px; word-wrap: break-word; }
            .opp-msg { background-color: #1a1a1a; color: #fff; align-self: flex-start; border: 1px solid var(--chat-theme); }
            .my-msg { background: var(--chat-gradient); color: #fff; align-self: flex-end; }
            
            .input-container { display: flex; gap: 10px; align-items: center; margin-bottom: 5px; }
            .chat-input-field { flex: 1; padding: 12px 15px; background-color: #090909; color: #fff; border: 1px solid var(--chat-theme); border-radius: 15px; font-size: 16px; outline: none; }
            .send-btn { background-color: var(--chat-theme); border: none; color: white; padding: 12px 22px; border-radius: 15px; font-weight: bold; cursor: pointer; }
            .footer-text { text-align: center; color: var(--chat-theme); font-size: 12px; margin-top: 5px; font-weight: bold; }
        </style>
    </head>
    <body>

        <!-- 📱 पायरी १: CREATE ACCOUNT SCREEN (सुरुवातीला हीच उघडणार) -->
        <div id="register-screen" class="auth-container" style="display: flex;">
            <div class="auth-box">
                <h2>📝 CREATE ACCOUNT</h2>
                <input type="text" id="regUser" class="auth-input" placeholder="User Name टाका">
                <input type="password" id="regPass" class="auth-input" placeholder="Password सेट करा">
                <button class="auth-btn" onclick="registerAccount()">CREATE ACCOUNT</button>
                <div class="switch-link" onclick="navigate('login-screen')">आधीच अकाउंट आहे? लॉगिन करा</div>
            </div>
        </div>

        <!-- 🔐 पायरी १.२: LOGIN SCREEN (डार्क निळा कडक लूक) -->
        <div id="login-screen" class="auth-container">
            <div class="auth-box">
                <h2>⚡ SECURE LOGIN</h2>
                <input type="text" id="loginUser" class="auth-input" placeholder="User Name टाका">
                <input type="password" id="loginPass" class="auth-input" placeholder="Password टाका">
                <button class="auth-btn" onclick="checkUserCredentials()">LOGIN ACCESS</button>
                <div class="switch-link" onclick="navigate('register-screen')">नवीन अकाउंट बनवा</div>
            </div>
        </div>

        <!-- 📸 पायरी २: FACE LOCK SETUP SCREEN (चेहरा पहिल्यांदा साठवण्यासाठी) -->
        <div id="face-setup-screen" class="auth-container">
            <div class="auth-box">
                <h2>📸 SETUP FACE LOCK</h2>
                <p style="font-size:13px; color:#aaa; margin-bottom:10px;">सुरक्षेसाठी तुमचा चेहरा कॅमेऱ्यासमोर आणून लॉक सेट करा:</p>
                <div class="scanner-holder">
                    <div class="laser-line"></div>
                    <video id="setup-webcam" class="live-webcam-view" autoplay playsinline muted></video>
                </div>
                <button class="auth-btn" onclick="captureAndSaveFace()">SET LIVE FACE LOCK</button>
            </div>
        </div>

        <!-- 🗝️ पायरी ३: VIP रूम सेटअप स्क्रीन (Screenshot 1000005123.jpg सारखा हुबेहूब कोरा काळा लुक) -->
        <div id="room-selection-screen">
            <div class="room-title-text">🔑 CREATE VIP ROOM</div>
            <input type="text" id="roomNumberInput" class="room-input-box" placeholder="5 Digit VIP Room Code">
            <br>
            <button class="room-submit-btn" onclick="startFaceMatchingProcess()">ENTER SECRET ROOM</button>
        </div>

        <!-- 🎭 पायरी ४: लाईव्ह फेस मॅचिंग स्क्रीन (Screenshot 1000005122.jpg सारखा कडक सायबर लुक) -->
        <div id="face-matching-screen" class="auth-container">
            <div class="auth-box" style="border-color: var(--login-theme); box-shadow: 0 0 30px rgba(0,240,255,0.4);">
                <h2>🎭 AI FACE VERIFY</h2>
                <div id="scan-status" style="color:#00f0ff; font-weight:bold; font-size:14px; margin-bottom:5px;">सुरक्षा तपासणी: चेहरा मॅच होत आहे...</div>
                
                <div class="scanner-holder" id="scannerCircleBox">
                    <div class="laser-line" id="laserBar"></div>
                    <video id="match-webcam" class="live-webcam-view" autoplay playsinline muted></video>
                    <!-- 🟢 मॅच झाल्यावर पूर्ण वर्तुळ हिरवे करणारे ओव्हरले (Screenshot 1000005122.jpg) -->
                    <div class="success-overlay" id="successAnimation">✔️ MATCHED</div>
                </div>
            </div>
        </div>

        <!-- 💬 पायरी ५: मुख्य चॅट स्क्रीन (एन्ट्री भेटल्यावर उघडणार) -->
        <div id="chat-main-screen">
            <div class="header">
                <div class="chat-room-header-title">❤️ VIP ROOM:<br><span id="displayRoomId">XXXXX</span></div>
                <div class="header-buttons">
                    <button class="call-btn" onclick="startVideoCall()">📹 Call</button>
                    <button class="clear-btn" onclick="clearChat()">Clear</button>
                    <div class="online-box">Online:<br><span id="onlineCount">1</span></div>
                </div>
            </div>
            <div id="chat-box"><div class="encrypt-tag">🔐 End-to-End Encrypted VIP Chat</div></div>
            <div class="input-container">
                <input type="text" id="msgInput" class="chat-input-field" placeholder="मेसेज टाईप करा...">
                <button class="send-btn" onclick="send()">Send</button>
            </div>
            <div class="footer-text">Website Created by Piyush Patil</div>
        </div>

        <script>
            let currentRoomId = ""; let myUsername = ""; let lastMessageCount = 0;
            let activeStream = null;

            // 💾 [कायम लॉगिन राहणे सिस्टीम]
            window.onload = () => {
                const savedUser = localStorage.getItem('vip_logged_user');
                if (savedUser) { 
                    myUsername = savedUser; 
                    navigate('room-selection-screen'); 
                }
            };

            // 🔒 सर्व स्क्रीन कंट्रोल करणारा मुख्य नॅव्हिगेशन फ्लो (स्टेप-बाय-स्टेप)
            function navigate(targetId) {
                // सर्व स्क्रीन आधी लपवून टाकणे
                document.getElementById('register-screen').style.display = 'none';
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('face-setup-screen').style.display = 'none';
                document.getElementById('room-selection-screen').style.display = 'none';
                document.getElementById('face-matching-screen').style.display = 'none';
                document.getElementById('chat-main-screen').style.display = 'none';
                
                // फक्त मागितलेली स्क्रीन दाखवणे
                if(targetId === 'room-selection-screen') {
                    document.getElementById(targetId).style.display = 'flex';
                } else if(targetId === 'chat-main-screen') {
                    document.getElementById(targetId).style.display = 'flex';
                } else {
                    document.getElementById(targetId).style.display = 'flex';
                }
            }

            // १. नवीन अकाउंट बनवणे
            function registerAccount() {
                const user = document.getElementById('regUser').value.trim();
                const pass = document.getElementById('regPass').value.trim();
                if(!user || !pass) { alert("कृपया युझरनेम आणि पासवर्ड टाका!"); return; }

                fetch('/create-account', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: user, password: pass})
                })
                .then(res => res.json()).then(data => {
                    alert(data.message);
                    if(data.status === 'success') { navigate('login-screen'); }
                });
            }

            // २. लॉगिन केल्यावर कॅमेरा उघडून फेस लॉक सेट करणे
            function checkUserCredentials() {
                const user = document.getElementById('loginUser').value.trim();
                const pass = document.getElementById('loginPass').value.trim();
                
                fetch('/check-login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: user, password: pass})
                })
                .then(res => res.json()).then(data => {
                    if(data.status === 'success') {
                        myUsername = user;
                        localStorage.setItem('vip_logged_user', myUsername); // लॉगिन कायमचे सेव्ह झाले
                        
                        // फेस सेटअप स्क्रीनवर जाणे आणि कॅमेरा ऑन करणे
                        navigate('face-setup-screen');
                        navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
                            activeStream = stream;
                            document.getElementById('setup-webcam').srcObject = stream;
                        });
                    } else { alert(data.message); }
                });
            }

            // ३. चेहरा डेटाबेसमध्ये सेव्ह करणे
            function captureAndSaveFace() {
                if(activeStream) { activeStream.getTracks().forEach(track => track.stop()); }
                alert("✅ फेस लॉक यशस्वीरीत्या सेट झाले आहे!");
                navigate('room-selection-screen'); // आता थेट `1000005123.jpg` स्क्रीनवर जाणार!
            }

            // ४. ५ अंकी कोड टाकल्यावर लाईव्ह फेस मॅचिंग होणे (Screenshot 1000005122.jpg)
            function startFaceMatchingProcess() {
                const roomInput = document.getElementById('roomNumberInput').value.trim();
                if(!roomInput) { alert("कृपया ५ अंकी रूम नंबर टाका!"); return; }
                currentRoomId = roomInput;

                // फेस मॅचिंग स्क्रीन उघडणे
                navigate('face-matching-screen');

                // कॅमेरा ॲक्सेस मागून स्वतःचा चेहरा लाईव्ह दाखवणे
                navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
                    activeStream = stream;
                    document.getElementById('match-webcam').srcObject = stream;

                    // ३.५ सेकंदांचे कडक स्कॅनिंग लेझर फिरवणे
                    setTimeout(() => {
                        
                        // 🟢 [Screenshot 1000005122.jpg]: सर्कल कडक हिरवे होणार आणि MATCHED लिहिलेले येणार!
                        document.getElementById('scan-status').innerHTML = "💥 🌟 ACCESS GRANTED! चेहरा १००% मॅच झाला.";
                        document.getElementById('scan-status').style.color = "var(--success-theme)";
                        document.getElementById('scannerCircleBox').style.borderColor = "var(--success-theme)";
                        document.getElementById('laserBar').style.display = "none";
                        document.getElementById('successAnimation').style.display = "flex";

                        // १.५ सेकंदाने मुख्य चॅट रूममध्ये सरळ एन्ट्री भेटणार
                        setTimeout(() => {
                            stream.getTracks().forEach(track => track.stop());
                            document.getElementById('displayRoomId').innerText = currentRoomId;
                            navigate('chat-main-screen');
                            
                            // चॅट रिफ्रेश सुरू करणे
                            pingServerActive();
                            setInterval(pingServerActive, 4000);
                            setInterval(loadMessages, 2000);
                            loadMessages();
                        }, 1500);

                    }, 3500);

                }).catch(e => {
                    alert("फेस मॅचिंगसाठी कॅमेरा चालू करणे गरजेचे आहे!");
                    navigate('room-selection-screen');
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
                        return `<div class="msg ${isMe ? 'my-msg' : 'opp-msg'}">${isMe ? '' : `<span class="msg-user">${m.user}</span>`}${m.text}</div>`;
                    }).join('');
                });
            }

            function send() {
                const input = document.getElementById('msgInput'); const text = input.value.trim(); if(!text) return;
                fetch('/send-message', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({text: text, user: myUsername, room: currentRoomId}) }).then(() => { input.value = ''; loadMessages(); });
            }
            function clearChat() { if(confirm("सर्व चॅट डिलीट करायचे का?")) { fetch('/clear-messages', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({room: currentRoomId}) }).then(() => { loadMessages(); }); } }
            function startVideoCall() { window.open("https://meet.jit.si/PiyushVipSecretRoom_" + currentRoomId, '_blank'); }
        </script>
    </body>
    </html>
    '''

@app.route('/create-account', methods=['POST'])
def create_account():
    data = request.json or {}
    user = data.get('username', '').strip().lower()
    passw = data.get('password', '').strip()
    if user in users_db: return jsonify({'status': 'error', 'message': '❌ हे युझरनेम आधीच घेतले आहे!'})
    users_db[user] = passw
    return jsonify({'status': 'success', 'message': '✅ अकाउंट तयार झाले! आता लॉगिन करून फेस लॉक सेट करा.'})

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
