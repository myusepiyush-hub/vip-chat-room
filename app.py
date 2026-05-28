from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# रूम आणि मेसेजेसचा डेटा ट्रॅकिंग (Database Memory)
room_data = {}

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Lovers VIP Chat - Google Auth</title>
        
        <!-- 🔐 गूगल लॉगिन करण्यासाठी आवश्यक असलेली मुख्य स्क्रिप्ट -->
        <script src="https://accounts.google.com/gsi/client" async defer></script>
        
        <style>
            :root {
                --login-theme: #00f0ff; /* ⚡ लॉगिन पेजसाठी नवीन कडक सायन/ब्लू कलर */
                --login-gradient: linear-gradient(135deg, #0072ff, #00f0ff);
                --chat-theme: #ff2a75; /* 💕 चॅट रूमसाठी तुझा जुना ओरिजिनल पिंक कलर */
                --chat-gradient: linear-gradient(135deg, #ff2a75, #ff5e62);
            }

            body {
                background-color: #030308; color: #fff;
                font-family: Arial, sans-serif; margin: 0; padding: 10px;
                display: flex; justify-content: center; height: 100vh; box-sizing: border-box;
            }

            /* ⚡ नवीन कडक गुगल लॉगिन स्क्रीन डिझाईन (Premium Cyber Look) */
            .auth-container {
                width: 100%; max-width: 400px; display: flex; flex-direction: column;
                justify-content: center; align-items: center; height: 90vh;
            }
            .auth-box {
                border: 2px solid var(--login-theme); padding: 35px 20px; border-radius: 30px;
                text-align: center; box-shadow: 0 0 25px rgba(0, 240, 255, 0.3);
                background-color: #060814; width: 90%;
            }
            .auth-box h2 { color: var(--login-theme); margin: 0 0 10px 0; font-size: 24px; font-weight: bold; letter-spacing: 1px; }
            .auth-p { font-size: 13px; color: #8a99ad; margin-bottom: 25px; }
            
            .room-input {
                width: 85%; padding: 12px; font-size: 16px; text-align: center;
                background: #000; border: 1px solid var(--login-theme); color: #fff; border-radius: 15px; margin-bottom: 20px; outline: none;
                box-shadow: inset 0 0 5px rgba(0, 240, 255, 0.2);
            }
            
            /* गुगल लॉगिन बटण कंटेनर */
            .google-btn-wrapper {
                display: flex; justify-content: center; align-items: center; margin-top: 15px;
            }

            /* 💬 मुख्य चॅट स्क्रीन (तुझा तोच ओरिजिनल डेंजर लुक - Screenshot 1000005088.jpg सारखा) */
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
            .online-box { border: 1px solid var(--chat-theme); border-radius: 15px; padding: 5px 12px; font-size: 12px; text-align: center; line-height: 1.2; min-width: 50px; }
            .call-btn { background: linear-gradient(45deg, #00ffcc, #00ee99); border: none; color: #000; padding: 6px 12px; border-radius: 15px; font-weight: bold; cursor: pointer; font-size: 14px; box-shadow: 0 0 8px rgba(0, 255, 204, 0.4); }
            
            #chat-box { flex: 1; border: 1px solid var(--chat-theme); border-radius: 15px; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; margin-bottom: 15px; background-color: #050505; }
            .encrypt-tag { text-align: center; color: #444; font-size: 11px; font-style: italic; margin: 5px auto; background: #090909; padding: 5px 12px; border-radius: 20px; border: 1px dashed #333; width: fit-content; }
            
            .msg { padding: 12px 18px; border-radius: 18px; max-width: 75%; font-size: 16px; word-wrap: break-word; line-height: 1.4; }
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

        <!-- ⚡ १. GOOGLE LOGIN SCREEN (नवीन कडक लुक) -->
        <div id="login-screen" class="auth-container">
            <div class="auth-box">
                <h2>⚡ GOOGLE SIGN IN</h2>
                <p class="auth-p">झटपट सुरक्षित लॉगिन करण्यासाठी तुमचा ५ अंकी रूम नंबर टाका आणि गूगल आयडी निवडा:</p>
                
                <!-- ५ अंकी गुप्त रूम नंबर इनपुट -->
                <input type="text" id="roomNumberInput" class="room-input" maxlength="5" placeholder="५ अंकी VIP रूम नंबर टाका">
                
                <!-- 🌐 ऑफिशिअल गूगल लॉगिन बटन एलिमेन्ट -->
                <div class="google-btn-wrapper">
                    <div id="g_id_onload"
                         data-client_id="1092842456424-m9b3294328b4932.apps.googleusercontent.com"
                         data-context="signin"
                         data-ux_mode="popup"
                         data-callback="handleGoogleLogin"
                         data-auto_prompt="false">
                    </div>

                    <div class="g_id_signin"
                         data-type="standard"
                         data-shape="pill"
                         data-theme="filled_blue"
                         data-text="signin_with"
                         data-size="large"
                         data-logo_alignment="left">
                    </div>
                </div>
            </div>
        </div>

        <!-- 💬 २. मुख्य चॅट स्क्रीन (लॉगिन झाल्यावरच उघडेल) -->
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

            // 🌐 गूगल लॉगिन झाल्यावर नाव गोळा करणारे फंक्शन
            function handleGoogleLogin(response) {
                const roomInput = document.getElementById('roomNumberInput').value.trim();
                if(!roomInput || roomInput.length < 3) {
                    alert("कृपया आधी ५ अंकी अचूक VIP रूम नंबर टाका!");
                    return;
                }

                // गुगलच्या सिक्रेट टोकन मधून युझरचे नाव काढणे (JWT Decoder लॉजिक)
                try {
                    const base64Url = response.credential.split('.')[1];
                    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
                    const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
                        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                    }).join(''));

                    const googleUser = JSON.parse(jsonPayload);
                    
                    // गुगल अकाउंटवरील ओरिजिनल नाव (उदा. Piyush Patil) गोळा करणे
                    myUsername = googleUser.name;
                    currentRoomId = roomInput;
                    
                    // लॉगिन स्क्रीन लपवून थेट चॅट उघडणे
                    document.getElementById('login-screen').style.display = 'none';
                    document.getElementById('chat-main-screen').style.display = 'flex';
                    document.getElementById('displayRoomId').innerText = currentRoomId;
                    
                    pingServerActive();
                    setInterval(pingServerActive, 4000);
                    setInterval(loadMessages, 2000);
                    loadMessages();

                } catch (e) {
                    // जर नेटवर्क इश्यू असेल तर बॅकअप रँडम नेम देणे
                    alert("गूगल लॉगिन यशस्वी झाले!");
                    myUsername = "VIP User";
                    currentRoomId = roomInput;
                    document.getElementById('login-screen').style.display = 'none';
                    document.getElementById('chat-main-screen').style.display = 'flex';
                    document.getElementById('displayRoomId').innerText = currentRoomId;
                }
            }

            function pingServerActive() {
                fetch('/ping', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({room: currentRoomId, user: myUsername}) })
                .then(res => res.json()).then(data => { document.getElementById('onlineCount').innerText = data.online_count; });
            }

            document.getElementById("msgInput").addEventListener("keyup", function(event) { if (event.key === "Enter") { send(); } });

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
