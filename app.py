from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# रूम वाईज मेसेजेस साठवण्यासाठी डिक्शनरी (मेमरी)
room_messages = {}

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Lovers VIP Chat</title>
        <style>
            body {
                background-color: #000;
                color: #fff;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 10px;
                display: flex;
                justify-content: center;
                height: 100vh;
                box-sizing: border-box;
            }
            
            /* 🔐 रूम सिलेक्ट करण्याची स्क्रीन (सुरुवातीला दिसेल) */
            #room-selection-screen {
                width: 100%;
                max-width: 450px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 90vh;
            }
            .room-box {
                border: 2px solid #ff2a75;
                padding: 30px 20px;
                border-radius: 25px;
                text-align: center;
                box-shadow: 0 0 20px rgba(255, 42, 117, 0.4);
                background-color: #050505;
                width: 85%;
            }
            .room-box h2 { color: #ff2a75; margin-bottom: 20px; font-size: 24px; }
            .room-input {
                width: 85%;
                padding: 12px;
                font-size: 18px;
                text-align: center;
                background: #000;
                border: 1px solid #ff2a75;
                color: #fff;
                border-radius: 15px;
                margin-bottom: 20px;
                outline: none;
                letter-spacing: 2px;
            }
            .room-btn {
                background: linear-gradient(135deg, #ff2a75, #ff5e62);
                border: none;
                color: white;
                padding: 12px 30px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 15px;
                cursor: pointer;
                width: 90%;
            }

            /* 💬 मुख्य चॅट स्क्रीन (ओरिजिनल डेंजर लुक - सुरवातीला लपवलेली असेल) */
            #chat-main-screen {
                display: none;
                width: 100%;
                max-width: 450px;
                border: 2px solid #ff2a75;
                border-radius: 25px;
                padding: 15px;
                flex-direction: column;
                background-color: #000;
                box-shadow: 0 0 20px rgba(255, 42, 117, 0.4);
                height: 95vh;
            }
            
            /* वरची पट्टी */
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }
            .room-title {
                color: #ff2a75;
                font-size: 18px;
                font-weight: bold;
                margin: 0;
                line-height: 1.2;
            }
            .header-buttons {
                display: flex;
                gap: 8px;
                align-items: center;
            }
            .clear-btn {
                background-color: #ff2a75;
                border: none;
                color: white;
                padding: 6px 14px;
                border-radius: 15px;
                font-weight: bold;
                cursor: pointer;
                font-size: 14px;
            }
            .online-box {
                border: 1px solid #ff2a75;
                border-radius: 15px;
                padding: 5px 12px;
                font-size: 12px;
                text-align: center;
                line-height: 1.2;
            }
            .call-btn {
                background: linear-gradient(45deg, #00ffcc, #00ee99);
                border: none;
                color: #000;
                padding: 6px 12px;
                border-radius: 15px;
                font-weight: bold;
                cursor: pointer;
                font-size: 14px;
                box-shadow: 0 0 8px rgba(0, 255, 204, 0.4);
            }
            
            /* चॅट बॉक्स डिझाईन */
            #chat-box {
                flex: 1;
                border: 1px solid #ff2a75;
                border-radius: 15px;
                padding: 15px;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 12px;
                margin-bottom: 15px;
                background-color: #050505;
            }
            .msg {
                padding: 12px 18px;
                border-radius: 18px;
                max-width: 75%;
                font-size: 16px;
                word-wrap: break-word;
                line-height: 1.4;
            }
            .opp-msg {
                background-color: #1a1a1a;
                color: #fff;
                align-self: flex-start;
                border: 1px solid #ff2a75;
            }
            .my-msg {
                background: linear-gradient(135deg, #ff2a75, #ff5e62);
                color: #fff;
                align-self: flex-end;
            }
            
            /* इनपुट पट्टी */
            .input-container {
                display: flex;
                gap: 10px;
                align-items: center;
                margin-bottom: 5px;
            }
            input {
                flex: 1;
                padding: 12px 15px;
                background-color: #090909;
                color: #fff;
                border: 1px solid #ff2a75;
                border-radius: 15px;
                font-size: 16px;
                outline: none;
            }
            .send-btn {
                background-color: #ff2a75;
                border: none;
                color: white;
                padding: 12px 22px;
                border-radius: 15px;
                font-weight: bold;
                font-size: 16px;
                cursor: pointer;
            }
            .footer-text {
                text-align: center;
                color: #ff2a75;
                font-size: 12px;
                margin-top: 5px;
                font-weight: bold;
            }
            
            /* 📹 व्हिडिओ कॉल स्क्रीन विंडो */
            #video-container {
                display: none;
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100%;
                background: #000;
                z-index: 10000;
            }
            #video-frame { width: 100%; height: calc(100% - 60px); border: none; }
            .end-call-btn { width: 100%; height: 60px; background: #ff0033; color: white; font-size: 18px; font-weight: bold; border: none; cursor: pointer; }
        </style>
    </head>
    <body>

        <div id="room-selection-screen">
            <div class="room-box">
                <h2>❤️ LOVERS VIP CHAT</h2>
                <p style="color: #aaa; font-size: 14px;">तुमचा कोणताही सिक्रेट ५ अंकी रूम नंबर टाका:</p>
                <input type="text" id="roomNumberInput" class="room-input" maxlength="5" placeholder="उदा. 50501">
                <br>
                <button class="room-btn" onclick="joinRoom()">CREATE / JOIN ROOM</button>
            </div>
        </div>

        <div id="chat-main-screen">
            <div class="header">
                <div class="room-title">❤️ VIP ROOM:<br><span id="displayRoomId">XXXXX</span></div>
                <div class="header-buttons">
                    <button class="call-btn" onclick="startVideoCall()">📹 Call</button>
                    <button class="clear-btn" onclick="clearChat()">Clear</button>
                    <div class="online-box">Online:<br>2</div>
                </div>
            </div>

            <div id="chat-box"></div>

            <div class="input-container">
                <input type="text" id="msgInput" placeholder="मेसेज टाईप करा...">
                <button class="send-btn" onclick="send()">Send</button>
            </div>

            <div class="footer-text">Website Created by Piyush Patil</div>
        </div>

        <div id="video-container">
            <iframe id="video-frame" allow="camera; microphone; fullscreen;"></iframe>
            <button class="end-call-btn" onclick="endVideoCall()">❌ CALL END</button>
        </div>

        <script>
            let currentRoomId = "";
            let lastMessageCount = 0;

            // रूम जॉईन करण्याचा मुख्य फंक्शन
            function joinRoom() {
                const roomInput = document.getElementById('roomNumberInput').value.trim();
                if(roomInput.length < 3) {
                    alert("कृपया किमान ३ किंवा ५ अंकी नंबर टाका!");
                    return;
                }
                
                currentRoomId = roomInput;
                document.getElementById('displayRoomId').innerText = currentRoomId;
                
                // पहिली स्क्रीन लपवणे आणि मुख्य चॅट रूम चालू करणे
                document.getElementById('room-selection-screen').style.display = 'none';
                document.getElementById('chat-main-screen').style.display = 'flex';
                
                // दर २ सेकंदाला फक्त आपल्याच रूमचे मेसेज लोड करणे सुरू करणे
                setInterval(loadMessages, 2000);
                loadMessages();
            }

            function loadMessages() {
                if(!currentRoomId) return;
                
                fetch('/get-messages?room=' + currentRoomId)
                .then(res => res.json())
                .then(data => {
                    const chatBox = document.getElementById('chat-box');
                    chatBox.innerHTML = data.map(m => {
                        const msgClass = m.user === 'Me' ? 'my-msg' : 'opp-msg';
                        return `<div class="msg ${msgClass}">${m.text}</div>`;
                    }).join('');
                    
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

                fetch('/send-message', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text, user: 'Me', room: currentRoomId})
                }).then(() => {
                    input.value = '';
                    loadMessages();
                });
            }

            function clearChat() {
                if(confirm("या रूमचे सर्व चॅट डिलीट करायचे आहे का?")) {
                    fetch('/clear-messages', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({room: currentRoomId})
                    })
                    .then(() => { lastMessageCount = 0; loadMessages(); });
                }
            }

            // 📹 व्हिडिओ कॉल सुरू करणे (रूम नुसार पूर्णपणे स्वतंत्र)
            function startVideoCall() {
                // जेणेकरून तुमच्या रूमचा कॉल दुसऱ्या कोणाला कनेक्ट होणार नाही
                const callUrl = "https://meet.jit.si/PiyushVipSecretRoom_" + currentRoomId;
                document.getElementById("video-frame").src = callUrl;
                document.getElementById("video-container").style.display = "block";
            }

            function endVideoCall() {
                document.getElementById("video-frame").src = "";
                document.getElementById("video-container").style.display = "none";
            }

            document.getElementById("msgInput").addEventListener("keyup", function(event) {
                if (event.key === "Enter") { send(); }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/get-messages', methods=['GET'])
def get_messages():
    room = request.args.get('room', 'default')
    return jsonify(room_messages.get(room, []))

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    if data and data.get('text'):
        room = data.get('room', 'default')
        if room not in room_messages:
            room_messages[room] = []
        room_messages[room].append({'user': data.get('user', 'User'), 'text': data.get('text', '')})
    return jsonify({'status': 'success'})

@app.route('/clear-messages', methods=['POST'])
def clear_messages():
    data = request.json
    room = data.get('room', 'default')
    if room in room_messages:
        room_messages[room] = []
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
