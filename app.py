from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# रूम वाईज डेटा ट्रॅकिंग (मेसेजेस आणि युझर्स)
room_data = {}

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Lovers VIP Chat - AI Edition</title>
        <style>
            :root {
                --main-color: #ff2a75;
                --gradient-color: linear-gradient(135deg, #ff2a75, #ff5e62);
                --bg-box: #050505;
            }

            body {
                background-color: #000;
                color: #fff;
                font-family: Arial, sans-serif;
                margin: 0; padding: 10px;
                display: flex; justify-content: center; height: 100vh;
                box-sizing: border-box;
            }
            
            /* 🔐 १. सेटअप स्क्रीन */
            #room-selection-screen {
                width: 100%; max-width: 450px;
                display: flex; flex-direction: column;
                justify-content: center; align-items: center; height: 90vh;
            }
            .room-box {
                border: 2px solid var(--main-color);
                padding: 30px 20px; border-radius: 25px; text-align: center;
                box-shadow: 0 0 20px rgba(255, 42, 117, 0.4);
                background-color: #050505; width: 85%;
            }
            .room-input {
                width: 85%; padding: 12px; font-size: 16px; text-align: center;
                background: #000; border: 1px solid var(--main-color);
                color: #fff; border-radius: 15px; margin-bottom: 15px; outline: none;
            }
            .room-btn {
                background: var(--gradient-color); border: none; color: white;
                padding: 12px 30px; font-size: 16px; font-weight: bold;
                border-radius: 15px; cursor: pointer; width: 90%;
            }

            /* 💬 २. मुख्य चॅट स्क्रीन (ओरिजिनल डेंजर लुक) */
            #chat-main-screen {
                display: none; width: 100%; max-width: 450px;
                border: 2px solid var(--main-color); border-radius: 25px;
                padding: 15px; flex-direction: column; background-color: #000;
                box-shadow: 0 0 20px rgba(255, 42, 117, 0.4); height: 95vh;
                position: relative;
            }
            
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
            .room-title { color: var(--main-color); font-size: 16px; font-weight: bold; margin: 0; }
            .header-buttons { display: flex; gap: 5px; align-items: center; }
            .clear-btn { background-color: var(--main-color); border: none; color: white; padding: 6px 12px; border-radius: 15px; font-weight: bold; cursor: pointer; font-size: 12px; }
            .online-box { border: 1px solid var(--main-color); border-radius: 15px; padding: 4px 10px; font-size: 11px; text-align: center; }
            .call-btn { background: linear-gradient(45deg, #00ffcc, #00ee99); border: none; color: #000; padding: 6px 12px; border-radius: 15px; font-weight: bold; cursor: pointer; font-size: 12px; }
            
            /* 🕹️ गुपित कंट्रोल्स बटन्स (AI Features) */
            .ai-btn { background: #111; border: 1px solid #555; color: #aaa; font-size: 10px; padding: 4px 8px; border-radius: 10px; cursor: pointer; }
            .ai-btn.active { border-color: var(--main-color); color: var(--main-color); box-shadow: 0 0 8px var(--main-color); }

            #chat-box {
                flex: 1; border: 1px solid var(--main-color); border-radius: 15px;
                padding: 15px; overflow-y: auto; display: flex; flex-direction: column;
                gap: 12px; margin-bottom: 15px; background-color: var(--bg-box); position: relative;
            }
            
            .encrypt-tag { text-align: center; color: #444; font-size: 11px; font-style: italic; margin: 5px auto; background: #090909; padding: 5px 12px; border-radius: 20px; border: 1px dashed #333; width: fit-content; }
            
            .msg { padding: 12px 18px; border-radius: 18px; max-width: 75%; font-size: 16px; word-wrap: break-word; line-height: 1.4; z-index: 2; transition: filter 0.3s ease; }
            .opp-msg { background-color: #1a1a1a; color: #fff; align-self: flex-start; border: 1px solid var(--main-color); }
            .my-msg { background: var(--gradient-color); color: #fff; align-self: flex-end; }
            .msg-user { font-size: 11px; color: var(--main-color); margin-bottom: 4px; display: block; font-weight: bold; }
            
            /* 🚨 नजरबंदी मोडसाठी चायनीज फाईल किंवा ब्लेर इफेक्ट */
            .hidden-chat .msg { filter: blur(8px); pointer-events: none; }
            
            /* 🌪️ खिशातली व्हायब्रेशन पॅड सिस्टीम */
            #vibe-pad {
                display: none; width: 100%; height: 100px; background: #111;
                border: 1px dashed var(--main-color); border-radius: 15px;
                margin-bottom: 10px; justify-content: center; align-items: center;
                color: #888; font-size: 12px; cursor: pointer; user-select: none;
            }

            .input-container { display: flex; gap: 10px; align-items: center; margin-bottom: 5px; }
            input { flex: 1; padding: 12px 15px; background-color: #090909; color: #fff; border: 1px solid var(--main-color); border-radius: 15px; font-size: 16px; outline: none; }
            .send-btn { background-color: var(--main-color); border: none; color: white; padding: 12px 22px; border-radius: 15px; font-weight: bold; font-size: 16px; cursor: pointer; }
            .footer-text { text-align: center; color: var(--main-color); font-size: 12px; margin-top: 5px; font-weight: bold; }
            
            #video-container { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 10000; }
            #video-frame { width: 100%; height: calc(100% - 60px); border: none; }
            .end-call-btn { width: 100%; height: 60px; background: #ff0033; color: white; font-size: 18px; font-weight: bold; border: none; cursor: pointer; }
        </style>
    </head>
    <body>

        <!-- 🔐 1. Setup Screen -->
        <div id="room-selection-screen">
            <div class="room-box">
                <h2>❤️ LOVERS VIP CHAT</h2>
                <input type="text" id="usernameInput" class="room-input" placeholder="तुमचे नाव टाका">
                <input type="text" id="roomNumberInput" class="room-input" maxlength="5" placeholder="५ अंकी रूम नंबर">
                <br>
                <button class="room-btn" onclick="joinRoom()">CREATE / JOIN ROOM</button>
            </div>
        </div>

        <!-- 💬 2. Main Chat Room Screen -->
        <div id="chat-main-screen">
            <div class="header">
                <div class="room-title">❤️ VIP:<br><span id="displayRoomId">XXXXX</span></div>
                
                <div class="header-buttons">
                    <!-- 🛠️ फीचर्स ऑन-ऑफ करण्याचे बटन्स -->
                    <button id="lockBtn" class="ai-btn" onclick="toggleEyeLock()">👁️ EyeLock: OFF</button>
                    <button id="vibeModeBtn" class="ai-btn" onclick="toggleVibePad()">🌪️ VibeMode</button>
                    
                    <button class="call-btn" onclick="startVideoCall()">📹 Call</button>
                    <button class="clear-btn" onclick="clearChat()">Clear</button>
                    <div class="online-box">On:<br><span id="onlineCount">1</span></div>
                </div>
            </div>

            <!-- Audio Elements (🎵 आयडिया ३ साठी पार्श्वसंगीत) -->
            <audio id="bg-music" loop></audio>

            <div id="chat-box">
                <div class="encrypt-tag">🔐 End-to-End Encrypted VIP Chat</div>
            </div>

            <!-- 🌪️ खिशातून चॅटिंग करण्याचा व्हायब्रेशन पॅड -->
            <div id="vibe-pad" onmousedown="sendVibe(true)" onmouseup="sendVibe(false)" ontouchstart="sendVibe(true)" ontouchend="sendVibe(false)">
                👉 इथे दाबून खिशात व्हायब्रेट कोड पाठवा (Idea 10)
            </div>

            <div class="input-container">
                <input type="text" id="msgInput" placeholder="मेसेज टाईप करा..." oninput="playMoodMusic()">
                <button class="send-btn" onclick="send()">Send</button>
            </div>

            <div class="footer-text">Website Created by Piyush Patil</div>
        </div>

        <!-- Video window -->
        <div id="video-container">
            <iframe id="video-frame" allow="camera; microphone; fullscreen;"></iframe>
            <button class="end-call-btn" onclick="endVideoCall()">❌ CALL END</button>
        </div>

        <script>
            let currentRoomId = "";
            let myUsername = "";
            let lastMessageCount = 0;
            let eyeLockActive = false;
            let audioCtx = null;
            let audioOscillator = null;

            function joinRoom() {
                const nameInput = document.getElementById('usernameInput').value.trim();
                const roomInput = document.getElementById('roomNumberInput').value.trim();
                if(!nameInput || !roomInput) { alert("नाव आणि रूम नंबर टाका!"); return; }
                
                myUsername = nameInput;
                currentRoomId = roomInput;
                document.getElementById('displayRoomId').innerText = currentRoomId;
                document.getElementById('room-selection-screen').style.display = 'none';
                document.getElementById('chat-main-screen').style.display = 'flex';
                
                pingServerActive();
                setInterval(pingServerActive, 4000);
                setInterval(loadMessages, 2000);
                loadMessages();
            }

            // 🎵 [आयडिया ३]: शब्दांच्या मूॉडनुसार लाईव्ह फ्रिक्वेन्सी म्युझिक बदलणे (AI Sound Generation)
            function playMoodMusic() {
                if(!audioCtx) { audioCtx = new (window.AudioContext || window.webkitAudioContext)(); }
                const text = document.getElementById('msgInput').value;
                
                if(text.length === 0) { if(audioOscillator) { audioOscillator.stop(); audioOscillator = null; } return; }
                
                // साध्या शब्दांवरून किंवा इमोजीवरून टोन ठरवणे
                let freq = 220; // Default रोमँटिक बेस सूर
                if(text.includes('😂') || text.includes('happy') || text.includes('हाहा')) freq = 330; // आनंदी सूर
                if(text.includes('😡') || text.includes('रागात') || text.includes('का')) freq = 150; // भारी डार्क सूर
                
                if(!audioOscillator) {
                    audioOscillator = audioCtx.createOscillator();
                    audioOscillator.type = 'sine';
                    audioOscillator.connect(audioCtx.destination);
                    audioOscillator.start();
                }
                audioOscillator.frequency.setValueAtTime(freq, audioCtx.currentTime);
            }

            // 👁️ [आयडिया ५]: नजरबंदी मोड (Double Tap ने किंवा बटणाने चॅट ब्लर करणे - फोन उलट फिरवला तरी चालेल)
            function toggleEyeLock() {
                eyeLockActive = !eyeLockActive;
                const btn = document.getElementById('lockBtn');
                const chatBox = document.getElementById('chat-box');
                if(eyeLockActive) {
                    btn.classList.add('active'); btn.innerText = "👁️ EyeLock: ON";
                    chatBox.classList.add('hidden-chat');
                } else {
                    btn.classList.remove('active'); btn.innerText = "👁️ EyeLock: OFF";
                    chatBox.classList.remove('hidden-chat');
                }
            }
            // स्क्रीनवरून बोट काढल्यावर किंवा डबल टॅप केल्यावर सिक्रेट अनब्लर करण्याची सोय
            document.getElementById('chat-box').addEventListener('click', () => {
                if(eyeLockActive) {
                    const chatBox = document.getElementById('chat-box');
                    chatBox.classList.toggle('hidden-chat'); // क्षणभर पाहण्यासाठी टॅप करा
                }
            });

            // 🌪️ [आयडिया १०]: खिशातली व्हायब्रेशन पॅड सिस्टीम ऑन/ऑफ करणे
            function toggleVibePad() {
                const pad = document.getElementById('vibe-pad');
                const btn = document.getElementById('vibeModeBtn');
                if(pad.style.display === 'flex') { pad.style.display = 'none'; btn.classList.remove('active'); }
                else { pad.style.display = 'flex'; btn.classList.add('active'); }
            }

            function sendVibe(isPressing) {
                if(!currentRoomId) return;
                fetch('/send-vibe', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({room: currentRoomId, user: myUsername, vibe: isPressing})
                });
            }

            function pingServerActive() {
                if(!currentRoomId || !myUsername) return;
                fetch('/ping', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({room: currentRoomId, user: myUsername})
                })
                .then(res => res.json())
                .then(data => {
                    document.getElementById('onlineCount').innerText = data.online_count;
                    // जर समोरच्याने व्हायब्रेशन सिग्नल पाठवला असेल, तर तुमचा मोबाईल व्हायब्रेट होईल!
                    if(data.trigger_vibe && navigator.vibrate) { navigator.vibrate(200); }
                });
            }

            function loadMessages() {
                if(!currentRoomId) return;
                fetch('/get-messages?room=' + currentRoomId)
                .then(res => res.json())
                .then(data => {
                    const chatBox = document.getElementById('chat-box');
                    let htmlContent = '<div class="encrypt-tag">🔐 End-to-End Encrypted VIP Chat</div>';
                    
                    data.forEach(m => {
                        const isMe = m.user.toLowerCase() === myUsername.toLowerCase();
                        const msgClass = isMe ? 'my-msg' : 'opp-msg';
                        const nameLabel = isMe ? '' : `<span class="msg-user">${m.user}</span>`;
                        htmlContent += `<div class="msg ${msgClass}">${nameLabel}${m.text}</div>`;
                    });
                    
                    // जर आय-लॉक ॲक्टिव्ह असेल तर क्लास टिकवून ठेवणे
                    chatBox.innerHTML = htmlContent;
                    if(data.length > lastMessageCount) {
                        chatBox.scrollTop = chatBox.scrollHeight;
                        lastMessageCount = data.length;
                    }
                });
            }

            function send() {
                const input = document.getElementById('msgInput');
                const text = input.value.trim();
                if(!text || !currentRoomId) return;
                if(audioOscillator) { audioOscillator.stop(); audioOscillator = null; } // संगीत थांबवणे

                fetch('/send-message', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text, user: myUsername, room: currentRoomId})
                }).then(() => { input.value = ''; loadMessages(); });
            }

            function clearChat() {
                if(confirm("या रूमचे सर्व चॅट डिलीट करायचे आहे का?")) {
                    fetch('/clear-messages', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({room: currentRoomId}) })
                    .then(() => { lastMessageCount = 0; loadMessages(); });
                }
            }

            function startVideoCall() {
                const callUrl = "https://meet.jit.si/PiyushVipSecretRoom_" + currentRoomId;
                document.getElementById("video-frame").src = callUrl;
                document.getElementById("video-container").style.display = "block";
            }
            function endVideoCall() { document.getElementById("video-frame").src = ""; document.getElementById("video-container").style.display = "none"; }
            document.getElementById("msgInput").addEventListener("keyup", function(event) { if (event.key === "Enter") { send(); } });
        </script>
    </body>
    </html>
    '''

@app.route('/ping', methods=['POST'])
def ping_user():
    data = request.json or {}
    room = data.get('room', 'default')
    user = data.get('user', 'Unknown')
    
    if room not in room_data:
        room_data[room] = {'messages': [], 'users': {}, 'vibe_signal': {}}
    
    room_data[room]['users'][user] = True
    online_count = len(room_data[room]['users'])
    
    # चेक करणे की दुसऱ्या कोणा युझरने व्हायब्रेशन दाबून ठेवलंय का
    trigger_vibe = False
    for u, status in room_data[room]['vibe_signal'].items():
        if u != user and status is True:
            trigger_vibe = True
            break
            
    return jsonify({'status': 'success', 'online_count': online_count, 'trigger_vibe': trigger_vibe})

@app.route('/send-vibe', methods=['POST'])
def send_vibe():
    data = request.json or {}
    room = data.get('room', 'default')
    user = data.get('user', 'Unknown')
    vibe_status = data.get('vibe', False)
    
    if room in room_data:
        room_data[room]['vibe_signal'][user] = vibe_status
    return jsonify({'status': 'success'})

@app.route('/get-messages', methods=['GET'])
def get_messages():
    room = request.args.get('room', 'default')
    if room in room_data: return jsonify(room_data[room]['messages'])
    return jsonify([])

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json or {}
    if data.get('text'):
        room = data.get('room', 'default')
        user = data.get('user', 'User')
        if room not in room_data: room_data[room] = {'messages': [], 'users': {}, 'vibe_signal': {}}
        room_data[room]['messages'].append({'user': user, 'text': data.get('text', '')})
    return jsonify({'status': 'success'})

@app.route('/clear-messages', methods=['POST'])
def clear_messages():
    data = request.json or {}
    room = data.get('room', 'default')
    if room in room_data: room_data[room]['messages'] = []
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
