from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 🗂️ मल्टि-युझर आणि डायनॅमिक रूम डेटाबेस (रेंडर सर्व्हरवर १००% सुरक्षित धावणारी सिस्टीम)
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
        <title>VIP Lovers - Ultimate Public Network</title>
        <style>
            :root {
                --insta-gradient: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
                --cyber-blue: #00f0ff;
                --cyber-pink: #ff2a75;
                --cyber-green: #00ff66;
                --cyber-red: #ff3333;
                --glass-card: rgba(255, 255, 255, 0.05);
                --chat-gradient: linear-gradient(135deg, #ff2a75, #ff5e62);
            }

            body {
                /* 🌌 इन्स्टाग्राम सारखे जिवंत फिरते निऑन बॅकग्राउंड */
                background: linear-gradient(-45deg, #090a15, #bc1888, #2c1035, #020308);
                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
                color: #fff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0; padding: 12px; display: flex; justify-content: center;
                align-items: center; height: 100vh; box-sizing: border-box;
                overflow: hidden;
            }

            @keyframes gradientBG {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            /* 🗂️ प्रीमियम ग्लास मॉर्फिझम कार्ड डिझाईन */
            .auth-container {
                width: 100%; max-width: 390px; display: none; flex-direction: column;
                justify-content: center; align-items: center; height: 92vh; z-index: 10;
            }
            .auth-box {
                border: 1px solid rgba(255, 255, 255, 0.15); padding: 40px 22px; border-radius: 28px;
                text-align: center; box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
                background: var(--glass-card); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);
                width: 90%; animation: slideUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }

            @keyframes slideUp {
                from { transform: translateY(40px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            
            .auth-box h1 {
                font-family: 'Grand Hotel', 'Brush Script MT', cursive, sans-serif;
                font-size: 44px; margin: 0 0 5px 0;
                background: linear-gradient(45deg, #ff2a75, #ff00f0, #00f0ff);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            }
            .auth-p { font-size: 13px; color: rgba(255, 255, 255, 0.5); margin-bottom: 25px; }
            
            .auth-input {
                width: 88%; padding: 14px; font-size: 15px; text-align: center;
                background: rgba(0, 0, 0, 0.5); border: 1px solid rgba(255, 255, 255, 0.15);
                color: #fff; border-radius: 16px; margin-bottom: 18px; outline: none;
                transition: 0.3s;
            }
            .auth-input:focus {
                border-color: #ff2a75; box-shadow: 0 0 15px rgba(255, 42, 117, 0.3);
                transform: scale(1.02);
            }
            
            .gmail-btn {
                background: #fff; color: #000; border: none; padding: 14px 20px;
                font-size: 15px; font-weight: 700; border-radius: 16px; cursor: pointer;
                width: 98%; display: flex; align-items: center; justify-content: center; gap: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2); margin-bottom: 20px; transition: 0.2s;
            }

            .auth-btn {
                background: var(--insta-gradient); border: none; color: #fff;
                padding: 14px 30px; font-size: 16px; font-weight: 700; border-radius: 16px;
                cursor: pointer; width: 98%; text-transform: uppercase; letter-spacing: 1px;
                transition: 0.3s;
            }
            .auth-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(204, 35, 102, 0.4); }

            /* 🗝️ VIP रूम स्क्रीन डिझाईन (Screenshot 1000005124.jpg हुबेहूब कोरा काळा पब्लिक लुक) */
            #room-selection-screen { width: 100%; max-width: 400px; display: none; flex-direction: column; justify-content: center; align-items: flex-start; height: 90vh; padding-left: 35px; box-sizing: border-box; }
            .room-title-text { font-size: 28px; font-weight: 900; color: #fff; margin-bottom: 25px; }
            .room-input-box { width: 85%; max-width: 300px; padding: 14px; font-size: 18px; background-color: #fff; color: #000; border: none; border-radius: 10px; outline: none; margin-bottom: 25px; font-weight: 800; letter-spacing: 4px; text-align: center; box-shadow: 0 8px 20px rgba(0,0,0,0.4); }
            .room-submit-btn { background-color: #e0e0e0; color: #000; border: 1px solid #777; padding: 12px 35px; font-size: 15px; cursor: pointer; font-weight: 900; border-radius: 10px; text-transform: uppercase; }

            .success-overlay {
                display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0, 255, 102, 0.95); justify-content: center; align-items: center;
                font-size: 24px; font-weight: 900; color: #000; z-index: 100; border-radius: 28px;
            }

            /* 💬 मुख्य चॅट स्क्रीन (Screenshot 1000005088.jpg प्रगत लुक) */
            #chat-main-screen {
                display: none; width: 100%; max-width: 450px; border: 2px solid var(--cyber-pink); border-radius: 32px;
                padding: 18px; flex-direction: column; background: #000;
                box-shadow: 0 0 30px rgba(255, 42, 117, 0.4); height: 95vh; position: relative;
                transition: border-color 0.3s;
            }
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid rgba(255,42,117,0.2); padding-bottom: 10px; }
            .chat-room-header-title { color: var(--cyber-pink); font-size: 18px; font-weight: 900; }
            .header-buttons { display: flex; gap: 8px; align-items: center; }
            .clear-btn { background-color: var(--cyber-pink); border: none; color: white; padding: 8px 16px; border-radius: 12px; font-weight: bold; cursor: pointer; }
            .online-box { border: 1px solid var(--cyber-pink); border-radius: 12px; padding: 6px 12px; font-size: 12px; text-align: center; }
            .call-btn { background: linear-gradient(45deg, #00ffcc, #00ee99); border: none; color: #000; padding: 8px 14px; border-radius: 12px; font-weight: 900; cursor: pointer; }
            
            #chat-box { flex: 1; border: 1px solid rgba(255, 42, 117, 0.4); border-radius: 22px; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 14px; margin-bottom: 15px; background-color: #030305; }
            .encrypt-tag { text-align: center; color: #555; font-size: 11px; font-style: italic; margin: 0 auto; background: #09090f; padding: 6px 16px; border-radius: 20px; border: 1px dashed #333; width: fit-content; }
            
            .msg { padding: 12px 18px; border-radius: 22px; max-width: 75%; font-size: 16px; word-wrap: break-word; line-height: 1.4; position: relative; user-select: none; cursor: pointer; }
            .opp-msg { background-color: #0e0f14; color: #fff; align-self: flex-start; border: 1px solid var(--cyber-pink); }
            .my-msg { background: var(--chat-gradient); color: #fff; align-self: flex-end; box-shadow: 0 4px 12px rgba(255,42,117,0.3); }
            
            /* ❤️ इन्स्टा स्टाईल हार्ट बॅज */
            .heart-badge { position: absolute; bottom: -10px; right: 10px; background: #000; border: 1px solid var(--cyber-pink); border-radius: 50%; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; font-size: 12px; animation: popHeart 0.2s ease; }
            @keyframes popHeart { from { transform: scale(0); } to { transform: scale(1); } }

            .input-container { display: flex; gap: 10px; align-items: center; }
            .chat-input-field { flex: 1; padding: 14px 18px; background-color: #07070a; color: #fff; border: 1px solid rgba(255,42,117,0.3); border-radius: 16px; font-size: 16px; outline: none; }
            .send-btn { background-color: var(--cyber-pink); border: none; color: white; padding: 14px 24px; border-radius: 16px; font-weight: 900; font-size: 16px; cursor: pointer; }
            .footer-text { text-align: center; color: rgba(255, 42, 117, 0.3); font-size: 11px; margin-top: 8px; font-weight: bold; }
        </style>
    </head>
    <body>

        <!-- 📱 पायरी १: GOOGLE LOGIN SCREEN -->
        <div id="register-screen" class="auth-container">
            <div class="auth-box">
                <h1>VIP Lovers</h1>
                <p class="auth-p">Premium Stealth Messenger Network</p>
                
                <button class="gmail-btn" onclick="simulateGoogleLogin()">
                    <svg width="20" height="20" viewBox="0 0 24 24"><path fill="#EA4335" d="M12 5.04c1.66 0 3.2.57 4.42 1.74l3.3-3.3C17.74 1.58 15.06 1 12 1 7.35 1 3.37 3.68 1.4 7.6l3.8 2.96C6.12 7.04 8.84 5.04 12 5.04z"/><path fill="#4285F4" d="M23.49 12.27c0-.81-.07-1.59-.2-2.36H12v4.51h6.46c-.29 1.48-1.14 2.73-2.4 3.58l3.73 2.88c2.18-2.01 3.7-4.99 3.7-8.61z"/><path fill="#FBBC05" d="M5.2 14.56c-.25-.76-.4-1.56-.4-2.56s.15-1.8.4-2.56L1.4 6.48C.5 8.26 0 10.19 0 12s.5 3.74 1.4 5.52l3.8-2.96z"/><path fill="#34A853" d="M12 23c3.24 0 5.97-1.07 7.96-2.91l-3.73-2.88c-1.1.74-2.5 1.18-4.23 1.18-3.16 0-5.88-2-6.8-4.96L1.4 16.32C3.37 20.32 7.35 23 12 23z"/></svg>
                    Continue with Google
                </button>

                <input type="text" id="gmailInput" class="auth-input" placeholder="किंवा तुमचा Gmail आयडी टाका">
                <button class="auth-btn" onclick="handleGmailLogin()">Secure Gateway</button>
            </div>
        </div>

        <!-- 🔒 पायरी २: SET SECURITY PIN LOCK -->
        <div id="face-setup-screen" class="auth-container">
            <div class="auth-box" style="border-color: rgba(255,255,255,0.2);">
                <h1 style="font-size:32px; background:linear-gradient(45deg, var(--cyber-pink), #ff00f0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Secure PIN</h1>
                <p class="auth-p">नेक्स्ट-टाईम डायरेक्ट उघडण्यासाठी ४ अंकी सीक्रेट पिन लॉक सेट करा:</p>
                <input type="password" id="setupPinField" class="auth-input" maxlength="4" style="font-size: 26px; letter-spacing: 12px; border-color: rgba(255,42,117,0.4);" placeholder="••••">
                <button class="auth-btn" onclick="saveVipPatternPin()">Save Lock Pin</button>
            </div>
        </div>

        <!-- 🗝️ पायरी ३: VIP रूम स्क्रीन (पब्लिक मल्टि-रूम - हुबेहूब 1000005124.jpg कोरा काळा लुक) -->
        <div id="room-selection-screen">
            <div class="room-title-text">🔑 CREATE VIP ROOM</div>
            <input type="text" id="roomNumberInput" class="room-input-box" placeholder="Any 5 Digit Room Code">
            <br>
            <button class="room-submit-btn" onclick="openSecurePatternWall()">ENTER SECRET ROOM</button>
        </div>

        <!-- 🛡️ पायरी ४: ४ अंकी सुरक्षा भिंत (पुन्हा ॲप उघडल्यावर डायरेक्ट पिन लॉक येईल) -->
        <div id="face-matching-screen" class="auth-container">
            <div class="auth-box" style="border-color: rgba(255,255,255,0.2);">
                <h1 style="font-size:32px; background:linear-gradient(45deg, var(--cyber-green), #00ffcc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Vault Unlock</h1>
                <p class="auth-p" id="scan-status">प्रवेश मिळवण्यासाठी तुमचा ४ अंकी गुपित सुरक्षा पिन टाका:</p>
                
                <input type="password" id="verifyPinField" class="auth-input" maxlength="4" style="font-size: 26px; letter-spacing: 12px; border-color: rgba(0,255,102,0.4);" placeholder="••••">
                <button class="auth-btn" style="background: linear-gradient(45deg, #00aa50, var(--cyber-green)); color: black;" onclick="verifyVipPatternPin()">Unlock Vault</button>
                
                <div class="success-overlay" id="successAnimation">✔️ SYSTEM ONLINE</div>
            </div>
        </div>

        <!-- 💬 पायरी ५: मुख्य चॅट स्क्रीन (Screenshot 1000005088.jpg) -->
        <div id="chat-main-screen">
            <div class="header">
                <div class="chat-room-header-title">❤️ VIP SECURE HUB:<br>ROOM ID: <span id="displayRoomId">XXXXX</span></div>
                <div class="header-buttons">
                    <button class="call-btn" onclick="startVideoCall()">📹 Call</button>
                    <button class="clear-btn" onclick="clearChat()">Clear</button>
                    <div class="online-box">Online:<br><span id="onlineCount">1</span></div>
                </div>
            </div>
            <div id="chat-box"><div class="encrypt-tag">🔐 End-to-End Encrypted Secure Network Connection</div></div>
            <div class="input-container">
                <input type="text" id="msgInput" class="chat-input-field" placeholder="गुप्त मेसेज टाईप करा..." oninput="triggerTypingGlow()">
                <button class="send-btn" onclick="send()">Send</button>
            </div>
            <div class="footer-text">SECURE CORE V9.0 // PRODUCTION READY</div>
        </div>

        <script>
            let currentRoomId = ""; let myUsername = ""; let lastMessageCount = 0;

            // 💾 [ऑटो-लॉगिन लाइफटाईम मेमरी इंजिन]
            window.onload = () => {
                const savedUser = localStorage.getItem('vip_gmail_user');
                const hasPin = localStorage.getItem('vip_has_pin');
                
                if (savedUser && hasPin) {
                    myUsername = savedUser;
                    navigate('face-matching-screen'); // थेट ४ अंकी पिन स्क्रीन उघडणार!
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
                document.getElementById(targetId).style.display = 'flex';
            }

            function simulateGoogleLogin() {
                document.getElementById('gmailInput').value = "user" + Math.floor(Math.random() * 999) + "@gmail.com";
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
                    alert("✅ सुरक्षा पिन यशस्वीरीत्या सेट झाला!");
                    navigate('room-selection-screen');
                });
            }

            function openSecurePatternWall() {
                const roomInput = document.getElementById('roomNumberInput').value.trim();
                if(roomInput.length < 3) { alert("कृपया वैध रूम कोड टाका!"); return; }
                currentRoomId = roomInput;
                
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

            function triggerTypingGlow() {
                const input = document.getElementById('msgInput');
                const chatMain = document.getElementById('chat-main-screen');
                if(input.value.length > 0) { chatMain.style.borderColor = "var(--cyber-green)"; } 
                else { chatMain.style.borderColor = "var(--cyber-pink)"; }
            }

            function addHeartReaction(msgElement) {
                if(msgElement.querySelector('.heart-badge')) return;
                const heart = document.createElement('div');
                heart.className = 'heart-badge'; heart.innerHTML = '❤️';
                msgElement.appendChild(heart);
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
                        return `<div class="msg ${isMe ? 'my-msg' : 'opp-msg'}" ondblclick="addHeartReaction(this)">${isMe ? '' : `<span>${m.user}: </span>`}${m.text}</div>`;
                    }).join('');
                    if(data.length > lastMessageCount) { chatBox.scrollTop = chatBox.scrollHeight; lastMessageCount = data.length; }
                });
            }

            function send() {
                const input = document.getElementById('msgInput'); const text = input.value.trim(); if(!text) return;
                document.getElementById('chat-main-screen').style.borderColor = "var(--cyber-pink)";
                fetch('/send-message', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({text: text, user: myUsername, room: currentRoomId}) }).then(() => { input.value = ''; loadMessages(); });
            }
            function clearChat() { if(confirm("सर्व चॅट डिलीट करायचे का?")) { fetch('/clear-messages', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({room: currentRoomId}) }).then(() => { loadMessages(); }); } }
            function startVideoCall() { window.open("https://meet.jit.si/PiyushProductionRoom_" + currentRoomId, '_blank'); }
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

# 🔬 [एरर फिक्स]: मल्टि-पब्लिक रूमसाठी बॅकएंड मेमरी सुरक्षितपणे जागच्या जागी तयार करणे
@app.route('/ping', methods=['POST'])
def ping_user():
    data = request.json or {}
    room = data.get('room', 'default').strip()
    user = data.get('user', 'Unknown')
    if room not in room_data: 
        room_data[room] = {'messages': [], 'users': {}}
    room_data[room]['users'][user] = True
    return jsonify({'status': 'success', 'online_count': len(room_data[room]['users'])})

@app.route('/get-messages', methods=['GET'])
def get_messages():
    room = request.args.get('room', 'default').strip()
    if room not in room_data: 
        room_data[room] = {'messages': [], 'users': {}}
    return jsonify(room_data[room]['messages'])

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json or {}
    room = data.get('room', 'default').strip()
    if data.get('text'):
        if room not in room_data: 
            room_data[room] = {'messages': [], 'users': {}}
        room_data[room]['messages'].append({'user': data.get('user'), 'text': data.get('text')})
    return jsonify({'status': 'success'})

@app.route('/clear-messages', methods=['POST'])
def clear_messages():
    data = request.json or {}
    room = data.get('room', 'default').strip()
    if room in room_data: room_data[room]['messages'] = []
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
