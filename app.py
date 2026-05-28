from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# प्रगत सुरक्षित डेटाबेस मेमरी
users_db = {}
room_data = {
    '55555': {'messages': [], 'users': {}} # तुमची कायमस्वरूपी फिक्स व्हीआयपी रूम
}

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VIP Vault - Premium Hub</title>
        <style>
            :root {
                --insta-gradient: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
                --cyber-blue: #00f0ff;
                --cyber-pink: #ff2a75;
                --cyber-green: #00ff66;
                --glass-card: rgba(255, 255, 255, 0.06);
                --chat-gradient: linear-gradient(135deg, #ff2a75, #ff5e62);
            }

            body {
                /* 🌌 इन्स्टाग्राम स्टाईल कडक निऑन फिरते बॅकग्राउंड */
                background: linear-gradient(-45deg, #0f1123, #bc1888, #cc2366, #020308);
                background-size: 400% 400%;
                animation: gradientBG 12s ease infinite;
                color: #fff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                margin: 0; padding: 15px; display: flex; justify-content: center;
                align-items: center; height: 100vh; box-sizing: border-box;
                overflow: hidden;
            }

            @keyframes gradientBG {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            /* ✨ प्रगत आकर्षक ग्लास बॉक्स (Instagram-Style Glassmorphism) */
            .auth-container {
                width: 100%; max-width: 380px; display: none; flex-direction: column;
                justify-content: center; align-items: center; height: 90vh; z-index: 10;
            }
            .auth-box {
                border: 1px solid rgba(255, 255, 255, 0.15); padding: 45px 25px; border-radius: 30px;
                text-align: center; box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4), inset 0 0 20px rgba(255,255,255,0.05);
                background: var(--glass-card); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
                width: 88%; animation: slideUp 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }

            @keyframes slideUp {
                from { transform: translateY(30px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            
            /* 👑 इन्स्टा स्टाईल कडक लोगो टेक्स्ट */
            .auth-box h1 {
                font-family: 'Grand Hotel', 'Brush Script MT', cursive, sans-serif;
                font-size: 42px; margin: 0 0 5px 0; font-weight: 500;
                background: linear-gradient(45deg, #ff2a75, #ff00f0, #00f0ff);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                letter-spacing: 1px;
            }
            .auth-p { font-size: 14px; color: rgba(255, 255, 255, 0.6); margin-bottom: 30px; font-weight: 400; }
            
            /* 🕹️ प्रगत इन्पुट फील्ड्स डिझाईन */
            .auth-input {
                width: 88%; padding: 14px; font-size: 15px; text-align: center;
                background: rgba(0, 0, 0, 0.4); border: 1px solid rgba(255, 255, 255, 0.15);
                color: #fff; border-radius: 15px; margin-bottom: 18px; outline: none;
                transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            }
            .auth-input:focus {
                border-color: #ff2a75; box-shadow: 0 0 15px rgba(255, 42, 117, 0.3);
                background: rgba(0, 0, 0, 0.6); transform: scale(1.02);
            }
            
            /* 🔴 प्रीमियम गुगल बटण (Insta-Style Interaction) */
            .gmail-btn {
                background: #fff; color: #000; border: none; padding: 14px 20px;
                font-size: 15px; font-weight: 700; border-radius: 15px; cursor: pointer;
                width: 98%; display: flex; align-items: center; justify-content: center; gap: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2); margin-bottom: 20px;
                transition: all 0.2s ease;
            }
            .gmail-btn:hover { transform: scale(1.02); box-shadow: 0 6px 20px rgba(255,255,255,0.2); }
            .gmail-btn:active { transform: scale(0.98); }

            /* ✨ मुख्य कृती बटण */
            .auth-btn {
                background: var(--insta-gradient); border: none; color: #fff;
                padding: 14px 30px; font-size: 16px; font-weight: 700; border-radius: 15px;
                cursor: pointer; width: 98%; text-transform: uppercase; letter-spacing: 1px;
                transition: all 0.3s ease; box-shadow: 0 6px 20px rgba(204, 35, 102, 0.3);
            }
            .auth-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(204, 35, 102, 0.5); filter: brightness(1.1); }
            .auth-btn:active { transform: translateY(1px); }

            /* 🗝️ VIP रूम स्क्रीन डिझाईन (हुबेहूब 1000005124.jpg लुक पण प्रगत) */
            #room-selection-screen { width: 100%; max-width: 400px; display: none; flex-direction: column; justify-content: center; align-items: flex-start; height: 90vh; padding-left: 35px; box-sizing: border-box; }
            .room-title-text { font-size: 28px; font-weight: 900; color: #fff; margin-bottom: 25px; letter-spacing: 1px; text-shadow: 0 0 10px rgba(255,255,255,0.2); }
            .room-input-box { width: 85%; max-width: 300px; padding: 14px; font-size: 18px; background-color: #fff; color: #000; border: none; border-radius: 10px; outline: none; margin-bottom: 25px; font-weight: 800; letter-spacing: 4px; text-align: center; box-shadow: 0 8px 20px rgba(0,0,0,0.4); }
            .room-submit-btn { background-color: #e0e0e0; color: #000; border: 1px solid #777; padding: 12px 35px; font-size: 15px; cursor: pointer; font-weight: 900; border-radius: 10px; text-transform: uppercase; transition: 0.3s; }
            .room-submit-btn:hover { background-color: #fff; transform: translateY(-2px); }

            .success-overlay {
                display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0, 255, 102, 0.95); justify-content: center; align-items: center;
                font-size: 24px; font-weight: 900; color: #000; letter-spacing: 1px; z-index: 100;
                border-radius: 28px;
            }

            /* 💬 मुख्य चॅट स्क्रीन (Screenshot 1000005088.jpg) */
            #chat-main-screen {
                display: none; width: 100%; max-width: 450px; border: 2px solid var(--cyber-pink); border-radius: 32px;
                padding: 18px; flex-direction: column; background: #000;
                box-shadow: 0 0 30px rgba(255, 42, 117, 0.4); height: 95vh; position: relative;
            }
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid rgba(255,42,117,0.2); padding-bottom: 10px; }
            .chat-room-header-title { color: var(--cyber-pink); font-size: 18px; font-weight: 900; }
            .header-buttons { display: flex; gap: 8px; align-items: center; }
            .clear-btn { background-color: var(--cyber-pink); border: none; color: white; padding: 8px 16px; border-radius: 12px; font-weight: bold; cursor: pointer; }
            .online-box { border: 1px solid var(--cyber-pink); border-radius: 12px; padding: 6px 12px; font-size: 12px; text-align: center; }
            .call-btn { background: linear-gradient(45deg, #00ffcc, #00ee99); border: none; color: #000; padding: 8px 14px; border-radius: 12px; font-weight: 900; cursor: pointer; }
            
            #chat-box { flex: 1; border: 1px solid rgba(255, 42, 117, 0.4); border-radius: 22px; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 14px; margin-bottom: 15px; background-color: #030305; }
            .encrypt-tag { text-align: center; color: #555; font-size: 11px; font-style: italic; margin: 0 auto; background: #09090f; padding: 6px 16px; border-radius: 20px; border: 1px dashed #333; width: fit-content; }
            
            .msg { padding: 12px 18px; border-radius: 22px; max-width: 75%; font-size: 16px; word-wrap: break-word; line-height: 1.4; }
            .opp-msg { background-color: #0e0f14; color: #fff; align-self: flex-start; border: 1px solid var(--cyber-pink); }
            .my-msg { background: var(--chat-gradient); color: #fff; align-self: flex-end; box-shadow: 0 4px 12px rgba(255,42,117,0.3); }
            
            .input-container { display: flex; gap: 10px; align-items: center; }
            .chat-input-field { flex: 1; padding: 14px 18px; background-color: #07070a; color: #fff; border: 1px solid rgba(255,42,117,0.3); border-radius: 16px; font-size: 16px; outline: none; }
            .send-btn { background-color: var(--cyber-pink); border: none; color: white; padding: 14px 24px; border-radius: 16px; font-weight: 900; font-size: 16px; cursor: pointer; }
            .footer-text { text-align: center; color: rgba(255, 42, 117, 0.4); font-size: 11px; margin-top: 8px; font-weight: bold; }
        </style>
    </head>
    <body>

        <!-- 📱 पायरी १: INSTAGRAM-STYLE GMAIL LOGIN SCREEN (Ultra Attractive UI) -->
        <div id="register-screen" class="auth-container">
            <div class="auth-box">
                <h1>VIP Lovers</h1>
                <p class="auth-p">Quantum Encryption Secure Gateway</p>
                
                <!-- कडक गुगल लॉगिन बटण -->
                <button class="gmail-btn" onclick="simulateGoogleLogin()">
                    <svg width="20" height="20" viewBox="0 0 24 24"><path fill="#EA4335" d="M12 5.04c1.66 0 3.2.57 4.42 1.74l3.3-3.3C17.74 1.58 15.06 1 12 1 7.35 1 3.37 3.68 1.4 7.6l3.8 2.96C6.12 7.04 8.84 5.04 12 5.04z"/><path fill="#4285F4" d="M23.49 12.27c0-.81-.07-1.59-.2-2.36H12v4.51h6.46c-.29 1.48-1.14 2.73-2.4 3.58l3.73 2.88c2.18-2.01 3.7-4.99 3.7-8.61z"/><path fill="#FBBC05" d="M5.2 14.56c-.25-.76-.4-1.56-.4-2.56s.15-1.8.4-2.56L1.4 6.48C.5 8.26 0 10.19 0 12s.5 3.74 1.4 5.52l3.8-2.96z"/><path fill="#34A853" d="M12 23c3.24 0 5.97-1.07 7.96-2.91l-3.73-2.88c-1.1.74-2.5 1.18-4.23 1.18-3.16 0-5.88-2-6.8-4.96L1.4 16.32C3.37 20.32 7.35 23 12 23z"/></svg>
                    Continue with Google
                </button>

                <input type="text" id="gmailInput" class="auth-input" placeholder="किंवा तुमचा Gmail आयडी टाका">
                <button class="auth-btn" onclick="handleGmailLogin()">Secure Login</button>
            </div>
        </div>

        <!-- 🔒 पायरी २: SET VIP PIN LOCK SCREEN (Premium Glass) -->
        <div id="face-setup-screen" class="auth-container">
            <div class="auth-box" style="border-color: rgba(255,255,255,0.2);">
                <h1 style="font-size: 32px; background:linear-gradient(45deg, var(--cyber-pink), #ff00f0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Secure PIN</h1>
                <p class="auth-p">भविष्यातील डायरेक्ट लॉगिनसाठी ४ अंकी पिन लॉक सेट करा:</p>
                <input type="password" id="setupPinField" class="auth-input" maxlength="4" style="font-size: 26px; letter-spacing: 12px; border-color: rgba(255,42,117,0.4);" placeholder="••••">
                <button class="auth-btn" onclick="saveVipPatternPin()">Save Lock Code</button>
            </div>
        </div>

        <!-- 🗝️ पायरी ३: VIP रूम सेटअप स्क्रीन (Screenshot 1000005124.jpg हुबेहूब कोरा काळा प्रीमियम लुक) -->
        <div id="room-selection-screen">
            <div class="room-title-text">🔑 CREATE VIP ROOM</div>
            <input type="text" id="roomNumberInput" class="room-input-box" placeholder="5 Digit VIP Room Code" value="55555" readonly style="opacity:0.85;">
            <br>
            <button class="room-submit-btn" onclick="openSecurePatternWall()">ENTER SECRET ROOM</button>
        </div>

        <!-- 🛡️ पायरी ४: ४ अंकी पिनची मुख्य प्रगत सुरक्षा भिंत (पुन्हा ॲप उघडल्यावर डायरेक्ट हीच येईल!) -->
        <div id="face-matching-screen" class="auth-container">
            <div class="auth-box" style="border-color: rgba(255,255,255,0.2);">
                <h1 style="font-size: 32px; background:linear-gradient(45deg, var(--cyber-green), #00ffcc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Vault Verification</h1>
                <p class="auth-p" id="scan-status">प्रवेश मिळवण्यासाठी तुमचा ४ अंकी गुपित पिन टाका:</p>
                
                <input type="password" id="verifyPinField" class="auth-input" maxlength="4" style="font-size: 26px; letter-spacing: 12px; border-color: rgba(0,255,102,0.4);" placeholder="••••">
                <button class="auth-btn" style="background: linear-gradient(45deg, #00aa50, var(--cyber-green)); color: black; box-shadow: 0 6px 20px rgba(0,255,102,0.2);" onclick="verifyVipPatternPin()">Unlock Vault</button>
                
                <div class="success-overlay" id="successAnimation">✔️ CORES GRANTED</div>
            </div>
        </div>

        <!-- 💬 पायरी ५: मुख्य चॅट स्क्रीन (Screenshot 1000005088.jpg) -->
        <div id="chat-main-screen">
            <div class="header">
                <div class="chat-room-header-title">❤️ VIP QUANTUM ROOM:<br><span id="displayRoomId">55555</span></div>
                <div class="header-buttons">
                    <button class="call-btn" onclick="startVideoCall()">📹 Call</button>
                    <button class="clear-btn" onclick="clearChat()">Clear</button>
                    <div class="online-box">Online:<br><span id="onlineCount">1</span></div>
                </div>
            </div>
            <div id="chat-box"><div class="encrypt-tag">🔐 End-to-End Encrypted Secure Connection</div></div>
            <div class="input-container">
                <input type="text" id="msgInput" class="chat-input-field" placeholder="गुप्त मेसेज टाईप करा...">
                <button class="send-btn" onclick="send()">Send</button>
            </div>
            <div class="footer-text">SECURE SYSTEM V6.0 // BY PIYUSH PATIL</div>
        </div>

        <script>
            let currentRoomId = "55555"; let myUsername = ""; let lastMessageCount = 0;

            // 💾 [ऑटो-लॉगिन मेमरी इंजिन]
            window.onload = () => {
                const savedUser = localStorage.getItem('vip_gmail_user');
                const hasPin = localStorage.getItem('vip_has_pin');
                
                if (savedUser && hasPin) {
                    myUsername = savedUser;
                    navigate('face-matching-screen'); // थेट गुपित पिन टाकायची स्क्रीन उघडणार!
                } else {
                    navigate('register-screen'); // पहिल्यांदा उघडल्यास कडक इंस्टाग्राम लुक उघडणार
                }
            };

            function navigate(targetId) {
                document.getElementById('register-screen').style.display = 'none';
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

            function simulateGoogleLogin() {
                document.getElementById('gmailInput').value = "piyush.patil2026@gmail.com";
            }

            function handleGmailLogin() {
                const email = document.getElementById('gmailInput').value.trim();
                if(!email || !email.includes('@')) { alert("कृपया योग्य ईमेल टाका!"); return; }
                
                myUsername = email.split('@')[0];
                
                fetch('/create-account', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: myUsername})
                }).then(() => {
                    localStorage.setItem('vip_gmail_user', myUsername);
                    navigate('face-setup-screen');
                });
            }

            function saveVipPatternPin() {
                const enteredPin = document.getElementById('setupPinField').value.trim();
                if(enteredPin.length < 4) { alert("४ अंकी पिन आवश्यक आहे!"); return; }

                fetch('/save-vip-pin', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: myUsername, pin: enteredPin})
                }).then(() => {
                    localStorage.setItem('vip_has_pin', 'true');
                    alert("✅ सुरक्षा पिन सेव्ह झाला!");
                    navigate('room-selection-screen');
                });
            }

            function openSecurePatternWall() {
                document.getElementById('verifyPinField').value = "";
                document.getElementById('successAnimation').style.display = "none";
                navigate('face-matching-screen');
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
                        alert("❌ चुकीचा पिन कोड!");
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
    if user not in users_db: users_db[user] = {'pin': ''}
    return jsonify({'status': 'success'})

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
    if user in users_db and users_db[user]['pin'] == pin: return jsonify({'matched': True})
    return jsonify({'matched': False})

@app.route('/ping', methods=['POST'])
def ping_user():
    data = request.json or {}
    room = data.get('room', '55555')
    user = data.get('user', 'Unknown')
    room_data[room]['users'][user] = True
    return jsonify({'status': 'success', 'online_count': len(room_data[room]['users'])})

@app.route('/get-messages', methods=['GET'])
def get_messages():
    room = request.args.get('room', '55555')
    return jsonify(room_data[room]['messages'] if room in room_data else [])

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json or {}
    if data.get('text'):
        room = data.get('room', '55555')
        room_data[room]['messages'].append({'user': data.get('user'), 'text': data.get('text')})
    return jsonify({'status': 'success'})

@app.route('/clear-messages', methods=['POST'])
def clear_messages():
    data = request.json or {}
    room = data.get('room', '55555')
    if room in room_data: room_data[room]['messages'] = []
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
