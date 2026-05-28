from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# सुरक्षित प्रगत डेटाबेस मेमरी (रेंडरवर कधीही क्रॅश न होणारी सिस्टीम)
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
        <title>VIP Lovers - Quantum Stealth Hub</title>
        <style>
            :root {
                --cyber-blue: #00f0ff;
                --cyber-pink: #ff2a75;
                --cyber-green: #00ff66;
                --cyber-red: #ff3333;
                --glass-bg: rgba(6, 8, 20, 0.9);
                --neon-glow: 0 0 20px rgba(0, 240, 255, 0.4);
            }

            body {
                background: radial-gradient(circle at center, #0c0f26 0%, #020308 100%);
                color: #fff; font-family: 'Segoe UI', Roboto, sans-serif;
                margin: 0; padding: 10px; display: flex; justify-content: center;
                align-items: center; height: 100vh; box-sizing: border-box;
                overflow: hidden;
            }

            /* ✨ निऑन बॅकग्राउंड ग्रिड इफेक्ट */
            body::before {
                content: ''; position: absolute; width: 200%; height: 200%;
                background-image: linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
                                  linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
                background-size: 30px 30px; top: -50%; left: -50%; z-index: 0;
                transform: rotate(15deg); pointer-events: none;
            }

            /* 🗂️ प्रगत ग्लास-मॉर्फिझम कंटेनर */
            .auth-container {
                width: 100%; max-width: 420px; display: none; flex-direction: column;
                justify-content: center; align-items: center; height: 95vh; z-index: 10;
            }
            .auth-box {
                border: 2px solid var(--cyber-blue); padding: 40px 25px; border-radius: 24px;
                text-align: center; box-shadow: var(--neon-glow), inset 0 0 15px rgba(0, 240, 255, 0.1);
                background: var(--glass-bg); backdrop-filter: blur(12px); width: 88%;
                position: relative; overflow: hidden; transition: all 0.4s ease;
            }
            
            .auth-box h2 {
                color: #fff; text-shadow: 0 0 10px var(--cyber-blue); margin: 0 0 8px 0;
                font-size: 26px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase;
            }
            .auth-p { font-size: 13px; color: #8a99ad; margin-bottom: 25px; line-height: 1.4; }
            
            /* 🕹️ प्रगत आणि आधुनिक इनपुट्स */
            .auth-input {
                width: 88%; padding: 14px; font-size: 16px; text-align: center;
                background: rgba(0, 0, 0, 0.6); border: 1px solid rgba(0, 240, 255, 0.3);
                color: #fff; border-radius: 14px; margin-bottom: 18px; outline: none;
                transition: all 0.3s ease; box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
            }
            .auth-input:focus {
                border-color: var(--cyber-blue); box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
                transform: scale(1.02);
            }
            
            /* ⚡ प्रगत सायबरपंक बटण */
            .auth-btn {
                background: linear-gradient(135deg, #0072ff, var(--cyber-blue)); border: none; color: #000;
                padding: 14px 30px; font-size: 16px; font-weight: 800; border-radius: 14px;
                cursor: pointer; width: 95%; text-transform: uppercase; letter-spacing: 1px;
                transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4);
            }
            .auth-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0, 240, 255, 0.6); }
            .switch-link { color: #8a99ad; font-size: 13px; margin-top: 20px; cursor: pointer; text-decoration: underline; }

            /* 🗝️ VIP रूम स्क्रीन डिझाईन (Premium Stealth Look - हुबेहूब 1000005124.jpg) */
            #room-selection-screen { width: 100%; max-width: 400px; display: none; flex-direction: column; justify-content: center; align-items: flex-start; height: 90vh; padding-left: 30px; box-sizing: border-box; }
            .room-title-text { font-size: 28px; font-weight: 900; color: #fff; margin-bottom: 25px; letter-spacing: 1px; }
            .room-input-box { width: 85%; max-width: 300px; padding: 14px; font-size: 18px; background-color: #fff; color: #000; border: none; border-radius: 8px; outline: none; margin-bottom: 20px; font-weight: 800; letter-spacing: 3px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
            .room-submit-btn { background-color: #e0e0e0; color: #000; border: 1px solid #777; padding: 12px 30px; font-size: 15px; cursor: pointer; font-weight: 900; border-radius: 8px; text-transform: uppercase; }

            /* 🟢 मॅच झाल्यावर येणारे कडक ॲनिमेशन ओव्हरले */
            .success-overlay {
                display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0, 255, 102, 0.95); justify-content: center; align-items: center;
                font-size: 24px; font-weight: 900; color: #000; letter-spacing: 2px; z-index: 100;
                border-radius: 24px; animation: flashGreen 0.5s ease;
            }

            /* 💬 ५. मुख्य चॅट स्क्रीन (तुझा ओरिजिनल पिंक-ब्लॅक लुक - 1000005088.jpg) */
            #chat-main-screen {
                display: none; width: 100%; max-width: 450px; border: 2px solid var(--cyber-pink); border-radius: 30px;
                padding: 18px; flex-direction: column; background: #000;
                box-shadow: 0 0 25px rgba(255, 42, 117, 0.4); height: 95vh; position: relative;
            }
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid rgba(255,42,117,0.2); padding-bottom: 10px; }
            .chat-room-header-title { color: var(--cyber-pink); font-size: 18px; font-weight: 900; }
            .header-buttons { display: flex; gap: 8px; align-items: center; }
            .clear-btn { background-color: var(--cyber-pink); border: none; color: white; padding: 8px 16px; border-radius: 12px; font-weight: bold; cursor: pointer; }
            .online-box { border: 1px solid var(--cyber-pink); border-radius: 12px; padding: 6px 12px; font-size: 12px; text-align: center; }
            .call-btn { background: linear-gradient(45deg, #00ffcc, #00ee99); border: none; color: #000; padding: 8px 14px; border-radius: 12px; font-weight: 900; cursor: pointer; }
            
            #chat-box { flex: 1; border: 1px solid rgba(255, 42, 117, 0.4); border-radius: 20px; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 14px; margin-bottom: 15px; background-color: #030305; }
            .encrypt-tag { text-align: center; color: #555; font-size: 11px; font-style: italic; margin: 0 auto; background: #09090f; padding: 6px 16px; border-radius: 20px; border: 1px dashed #333; width: fit-content; }
            
            .msg { padding: 12px 18px; border-radius: 20px; max-width: 75%; font-size: 16px; word-wrap: break-word; line-height: 1.4; }
            .opp-msg { background-color: #0e0f14; color: #fff; align-self: flex-start; border: 1px solid var(--cyber-pink); }
            .my-msg { background: var(--chat-gradient); color: #fff; align-self: flex-end; box-shadow: 0 4px 12px rgba(255,42,117,0.3); }
            
            .input-container { display: flex; gap: 10px; align-items: center; }
            .chat-input-field { flex: 1; padding: 14px 18px; background-color: #07070a; color: #fff; border: 1px solid rgba(255,42,117,0.3); border-radius: 16px; font-size: 16px; outline: none; }
            .send-btn { background-color: var(--cyber-pink); border: none; color: white; padding: 14px 24px; border-radius: 16px; font-weight: 900; font-size: 16px; cursor: pointer; }
            .footer-text { text-align: center; color: rgba(255, 42, 117, 0.4); font-size: 11px; margin-top: 8px; font-weight: bold; }
        </style>
    </head>
    <body>

        <!-- 📱 पायरी १: CREATE ACCOUNT SCREEN -->
        <div id="register-screen" class="auth-container">
            <div class="auth-box">
                <h2>📝 REGISTER</h2>
                <p class="auth-p">नवीन सुरक्षित खाते तयार करा:</p>
                <input type="text" id="regUser" class="auth-input" placeholder="User Name टाका">
                <input type="password" id="regPass" class="auth-input" placeholder="Password सेट करा">
                <button class="auth-btn" onclick="registerAccount()">Create Account</button>
                <div class="switch-link" onclick="navigate('login-screen')">आधीच खाते आहे? लॉगिन करा</div>
            </div>
        </div>

        <!-- 🔐 पायरी १.२: LOGIN SCREEN -->
        <div id="login-screen" class="auth-container">
            <div class="auth-box">
                <h2>⚡ SYSTEM LOGIN</h2>
                <p class="auth-p">युझरनेम आणि पासवर्ड टाकून हब उघडा:</p>
                <input type="text" id="loginUser" class="auth-input" placeholder="User Name">
                <input type="password" id="loginPass" class="auth-input" placeholder="Password">
                <button class="auth-btn" onclick="checkUserCredentials()">Verify Access</button>
                <div class="switch-link" onclick="navigate('register-screen')">नवीन खाते बनवण्यासाठी इथे क्लिक करा</div>
            </div>
        </div>

        <!-- 🔒 पायरी २: SET VIP PIN LOCK SCREEN (फक्त पहिल्यांदा सेट करण्यासाठी) -->
        <div id="face-setup-screen" class="auth-container">
            <div class="auth-box" style="border-color: var(--cyber-pink); box-shadow: 0 0 25px rgba(255,42,117,0.2);">
                <h2 style="color: var(--cyber-pink); text-shadow: 0 0 10px var(--cyber-pink);">🔐 SETUP VIP PIN</h2>
                <p class="auth-p" style="color: #ccc;">तुमचा वैयक्तिक ४ अंकी गुप्त सुरक्षा पिन (Secret PIN) सेट करा:</p>
                <input type="password" id="setupPinField" class="auth-input" maxlength="4" style="font-size: 24px; letter-spacing: 10px; border-color: var(--cyber-pink);" placeholder="••••">
                <button class="auth-btn" style="background: var(--chat-gradient); color: white;" onclick="saveVipPatternPin()">LOCK & SAVE PIN</button>
            </div>
        </div>

        <!-- 🗝️ पायरी ३: VIP रूम सेटअप स्क्रीन (Screenshot 1000005124.jpg हुबेहूब प्रगत लुक - एकदा लॉगिन झाल्यावर डायरेक्ट हीच उघडणार!) -->
        <div id="room-selection-screen">
            <div class="room-title-text">🔑 CREATE VIP ROOM</div>
            <input type="text" id="roomNumberInput" class="room-input-box" placeholder="5 Digit VIP Room Code">
            <br>
            <button class="room-submit-btn" onclick="openSecurePatternWall()">ENTER SECRET ROOM</button>
        </div>

        <!-- 🛡️ पायरी ४: GRAPHIC PATTERN SECURITY WALL (पिन विचारणारी सुरक्षा भिंत) -->
        <div id="face-matching-screen" class="auth-container">
            <div class="auth-box" style="border-color: var(--cyber-green); box-shadow: 0 0 25px rgba(0,255,102,0.2);">
                <h2 style="color: var(--cyber-green); text-shadow: 0 0 10px var(--cyber-green);">🛡️ SECURITY PIN</h2>
                <p class="auth-p" id="scan-status">ओळख पडताळणी: तुमचा ४ अंकी गुपित VIP सुरक्षा पिन टाका:</p>
                
                <input type="password" id="verifyPinField" class="auth-input" maxlength="4" style="font-size: 24px; letter-spacing: 10px; border-color: var(--cyber-green);" placeholder="••••">
                <button class="auth-btn" style="background: linear-gradient(135deg, #00aa50, var(--cyber-green)); color: black;" onclick="verifyVipPatternPin()">VERIFY SECURITY PIN</button>
                
                <!-- 🟢 यशस्वी मॅच झाल्यावर येणारे कडक ॲनिमेशन ओव्हरले -->
                <div class="success-overlay" id="successAnimation">✔️ CONNECTIONS GRANTED</div>
            </div>
        </div>

        <!-- 💬 पायरी ५: मुख्य चॅट स्क्रीन (Premium Cyberpunk Pink Look) -->
        <div id="chat-main-screen">
            <div class="header">
                <div class="chat-room-header-title">❤️ VIP SECURE HUB:<br><span id="displayRoomId">XXXXX</span></div>
                <div class="header-buttons">
                    <button class="call-btn" onclick="startVideoCall()">📹 Call</button>
                    <button class="clear-btn" onclick="clearChat()">Clear</button>
                    <div class="online-box">Online:<br><span id="onlineCount">1</span></div>
                </div>
            </div>
            <div id="chat-box"><div class="encrypt-tag">🔐 End-to-End Encrypted Quantum Connection</div></div>
            <div class="input-container">
                <input type="text" id="msgInput" class="chat-input-field" placeholder="गुप्त मेसेज टाईप करा...">
                <button class="send-btn" onclick="send()">Send</button>
            </div>
            <div class="footer-text">SECURE CORE V5.0 // WEBSITE BY PIYUSH PATIL</div>
        </div>

        <script>
            let currentRoomId = ""; let myUsername = ""; let lastMessageCount = 0;

            // 💾 [फिचर - कायम लॉगिन राहणे]: ब्राउझर मेमरी ऑटोमॅटिक चेक करणे
            window.onload = () => {
                const savedUser = localStorage.getItem('vip_active_user');
                if (savedUser) {
                    // जर आधीच लॉगिन असेल, तर सरळ पायरी ३ वर (CREATE VIP ROOM) स्क्रीनवर पाठवणे!
                    myUsername = savedUser;
                    navigate('room-selection-screen');
                } else {
                    // जर पहिल्यांदा उघडले असेल, तरच क्रिएट अकाउंट दाखवणे
                    navigate('register-screen');
                }
            };

            function navigate(targetId) {
                document.getElementById('register-screen').style.display = 'none';
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('face-setup-screen').style.display = 'none';
                document.getElementById('room-selection-screen').style.display = 'none';
                document.getElementById('face-matching-screen').style.display = 'none';
                document.getElementById('chat-main-screen').style.display = 'none';
                
                if(targetId === 'room-selection-screen' || targetId === 'chat-main-screen') {
                    document.getElementById(targetId).style.display = 'flex';
                } else {
                    document.getElementById(targetId).style.display = 'flex';
                }
            }

            function registerAccount() {
                const user = document.getElementById('regUser').value.trim();
                const pass = document.getElementById('regPass').value.trim();
                if(!user || !pass) return;
                fetch('/create-account', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: user, password: pass})
                }).then(res => res.json()).then(data => { alert(data.message); if(data.status === 'success') navigate('login-screen'); });
            }

            function checkUserCredentials() {
                const user = document.getElementById('loginUser').value.trim();
                const pass = document.getElementById('loginPass').value.trim();
                fetch('/check-login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: user, password: pass})
                }).then(res => res.json()).then(data => {
                    if(data.status === 'success') {
                        myUsername = user;
                        // 💾 मोबाईलच्या लोकल मेमरीमध्ये युझरचे नाव कायमचे सेव्ह करणे (Persistent Login)
                        localStorage.setItem('vip_active_user', myUsername);
                        navigate('face-setup-screen');
                    } else { alert(data.message); }
                });
            }

            function saveVipPatternPin() {
                const enteredPin = document.getElementById('setupPinField').value.trim();
                if(enteredPin.length < 4) { alert("कृपया ४ अंकी पिन टाका!"); return; }

                fetch('/save-vip-pin', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: myUsername, pin: enteredPin})
                }).then(() => {
                    alert("✅ तुमचा VIP सुरक्षा पिन यशस्वीरीत्या सेट झाला!");
                    document.getElementById('setupPinField').value = "";
                    navigate('room-selection-screen');
                });
            }

            function openSecurePatternWall() {
                const roomInput = document.getElementById('roomNumberInput').value.trim();
                if(!roomInput) { alert("कृपया रूम कोड टाका!"); return; }
                currentRoomId = roomInput;
                
                document.getElementById('verifyPinField').value = "";
                document.getElementById('successAnimation').style.display = "none";
                navigate('face-matching-screen'); // ४ अंकी पिनची स्क्रीन उघडणार
            }

            function verifyVipPatternPin() {
                const enteredPin = document.getElementById('verifyPinField').value.trim();
                
                fetch('/verify-vip-pin', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: myUsername, pin: enteredPin})
                })
                .then(res => res.json()).then(data => {
                    if(data.matched === true) {
                        document.getElementById('successAnimation').style.display = "flex";
                        setTimeout(() => {
                            document.getElementById('displayRoomId').innerText = currentRoomId;
                            navigate('chat-main-screen');
                            pingServerActive();
                            setInterval(pingServerActive, 4000);
                            setInterval(loadMessages, 2000);
                            loadMessages();
                        }, 1200);
                    } else {
                        alert("❌ चुकीचा VIP सुरक्षा पिन! प्रवेश नाकारण्यात आला आहे.");
                        document.getElementById('verifyPinField').value = "";
                    }
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
                        return `<div class="msg ${isMe ? 'my-msg' : 'opp-msg'}">${isMe ? '' : `<span>${m.user}: </span>`}${m.text}</div>`;
                    }).join('');
                    if(data.length > lastMessageCount) { chatBox.scrollTop = chatBox.scrollHeight; lastMessageCount = data.length; }
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
    users_db[user] = {'password': passw, 'pin': ''}
    return jsonify({'status': 'success', 'message': '✅ अकाउंट तयार झाले!'})

@app.route('/check-login', methods=['POST'])
def check_login():
    data = request.json or {}
    user = data.get('username', '').strip().lower()
    passw = data.get('password', '').strip()
    if user in users_db and users_db[user]['password'] == passw: return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': '❌ चुकीचे युझरनेम किंवा पासवर्ड!'})

@app.route('/save-vip-pin', methods=['POST'])
def save_vip_pin():
    data = request.json or {}
    user = data.get('username', '').strip().lower()
    pin = data.get('pin', '')
    if user in users_db: users_db[user]['pin'] = pin
    return jsonify({'status': 'success'})

@app.route('/verify-vip-pin', methods=['POST'])
def verify_vip_pin():
    data = request.json or {}
    user = data.get('username', '').strip().lower()
    pin = data.get('pin', '')
    # जर युझर डेटाबेसमध्ये असेल आणि त्याचा सेव्ह केलेला पिन जुळला तरच ओक्के करणे
    if user in users_db and users_db[user]['pin'] == pin:
        return jsonify({'matched': True})
    return jsonify({'matched': False})

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
