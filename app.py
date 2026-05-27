from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html lang="mr">
<head>
    <meta charset="UTF-8">
    <title>Lovers VIP Secret Chat</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- लेटेस्ट १००% वर्किंग Ably JavaScript SDK -->
    <script src="https://cdn.ably.com/lib/ably.min-2.js"></script>

    <style>
        * { 
            box-sizing: border-box; 
            margin: 0; padding: 0; 
            -webkit-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        body {
            background: #000000; /* Purna Black Background */
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 15px;
        }
        .chat-container {
            width: 100%;
            max-width: 480px;
            background: #000000; 
            border: 2px solid #ff2a5f;
            border-radius: 20px;
            box-shadow: 0 0 35px rgba(255, 42, 95, 0.4);
            display: flex;
            flex-direction: column;
            height: 85vh;
            position: relative;
        }
        .chat-header {
            background: #0a0507;
            padding: 15px;
            border-bottom: 1px solid #ff2a5f;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top-left-radius: 18px;
            border-top-right-radius: 18px;
        }
        .chat-title {
            font-size: 1.1rem;
            font-weight: bold;
            color: #ff2a5f;
            text-shadow: 0 0 10px rgba(255, 42, 95, 0.5);
        }
        .header-actions {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .online-status {
            background: rgba(255, 42, 95, 0.15);
            color: #ff2a5f;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85rem;
            font-weight: bold;
            border: 1px solid #ff2a5f;
        }
        .intruder-alert {
            display: none;
            background: #ff0000;
            color: #ffffff;
            padding: 8px;
            font-size: 0.9rem;
            text-align: center;
            font-weight: bold;
            border-bottom: 1px solid #ff2a5f;
            animation: flash 0.8s infinite alternate;
        }
        .clear-btn {
            background: #000000;
            color: #ff2a5f;
            border: 1px solid #ff2a5f;
            padding: 4px 10px;
            font-size: 0.8rem;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
        }
        .clear-btn:hover {
            background: #ff2a5f;
            color: #ffffff;
        }
        .panic-btn {
            background: none;
            border: none;
            font-size: 1.4rem;
            cursor: pointer;
        }
        .messages-box {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
            background: #000000; /* Full Black Background */
        }
        
        /* 💥 मेसेज दिसण्यासाठी कडक रंगांचे बदल 💥 */
        .msg {
            max-width: 75%;
            padding: 11px 15px;
            border-radius: 15px;
            font-size: 1rem;
            line-height: 1.4;
            word-wrap: break-word;
        }
        /* तुमचा स्वतःचा मेसेज (उजवीकडे - निऑन पिंक आणि पांढरी अक्षरे) */
        .msg.sent {
            background: linear-gradient(135deg, #ff2a5f 0%, #ff5e3a 100%);
            color: #ffffff !important; /* गॅरंटीड व्हाईट टेक्स्ट */
            align-self: flex-end;
            border-bottom-right-radius: 2px;
            box-shadow: 0 2px 8px rgba(255, 42, 95, 0.3);
        }
        /* समोरच्याचा मेसेज (डावीकडे - डार्क ग्रे बॅकग्राउंड आणि पांढरी अक्षरे) */
        .msg.received {
            background: #1a1a1a; /* काळा नाही, डार्क ग्रे */
            color: #ffffff !important; /* गॅरंटीड व्हाईट टेक्स्ट */
            align-self: flex-start;
            border-bottom-left-radius: 2px;
            border: 1px solid #ff2a5f;
        }
        
        .input-area {
            padding: 15px;
            background: #0a0507;
            border-top: 1px solid #ff2a5f;
            display: flex;
            gap: 10px;
            border-bottom-left-radius: 18px;
            border-bottom-right-radius: 18px;
        }
        input[type="text"], input[type="number"] {
            flex: 1;
            padding: 12px;
            background: #000000;
            border: 1px solid #ff2a5f;
            color: #ffffff; /* इनपुटमधील टाईप केलेला टेक्स्ट पांढरा दिसेल */
            border-radius: 10px;
            outline: none;
            font-size: 1rem;
            -webkit-user-select: text;
            user-select: text;
        }
        .send-btn {
            background: #ff2a5f;
            color: #ffffff;
            border: none;
            padding: 0 22px;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
        }
        .login-box {
            width: 100%;
            max-width: 400px;
            background: #000000;
            border: 2px solid #ff2a5f;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 0 35px rgba(255, 42, 95, 0.35);
        }
        .login-box h1 {
            color: #ff2a5f;
            margin-bottom: 15px;
            text-shadow: 0 0 10px rgba(255, 42, 95, 0.4);
        }
        .credit-text {
            color: #ff2a5f;
            font-size: 0.9rem;
            font-weight: bold;
            margin-top: 20px;
            letter-spacing: 1px;
            text-shadow: 0 0 5px rgba(255, 42, 95, 0.3);
        }
        @keyframes flash {
            0% { background: #b91c1c; }
            100% { background: #ff0000; }
        }
    </style>
</head>
<body>

<!-- LOGIN SCREEN -->
<div class="login-box" id="loginScreen">
    <h1>❤️ LOVERS VIP CHAT ❤️</h1>
    <p style="color: #a1979b; margin-bottom: 25px;">गुप्त व्हीआयपी रूमसाठी खाली कोणताही ५ अंकी कोड टाका. पार्टनरलाही तोच कोड टाकायला सांगा!</p>
    
    <input type="number" id="secretCode" placeholder="५ अंकी कोड टाका (उदा. १२३४५)" oninput="javascript: if (this.value.length > 5) this.value = this.value.slice(0, 5);" style="width:100%; padding:12px; margin-bottom:15px; background:#000000; border:1px solid #ff2a5f; color:#ff2a5f; border-radius:10px; text-align:center; font-weight:bold; font-size:1.2rem;"><br>
    
    <button class="send-btn" style="width:100%; padding:12px;" onclick="joinChat()">रूममध्ये प्रवेश करा ➔</button>
    
    <div class="credit-text">Website Created by Piyush Patil</div>
</div>

<!-- MAIN CHAT SCREEN -->
<div class="chat-container" id="chatScreen" style="display: none;">
    <div class="intruder-alert" id="intruderAlert">🚨 लक्ष द्या: तुमच्या रूममध्ये ३ लोक ऑनलाईन आहेत! तुमची प्रायव्हसी धोक्यात आहे!</div>
    <div class="chat-header">
        <div class="chat-title" id="roomTitle">❤️ ROOM: LOADING...</div>
        <div class="header-actions">
            <button class="clear-btn" onclick="clearAllMessages()">Clear</button>
            <div class="online-status" id="onlineCount">Online: 1</div>
            <button class="panic-btn" onclick="panicClose()">❤️</button>
        </div>
    </div>
    
    <!-- मुख्य मेसेज बॉक्स -->
    <div class="messages-box" id="msgBox"></div>
    
    <div class="input-area">
        <input type="text" id="msgInput" placeholder="मेसेज टाईप करा..." onkeypress="handleKeyPress(event)">
        <button class="send-btn" onclick="sendMsg()">Send</button>
    </div>
    
    <div class="credit-text" style="text-align: center; margin-top: 5px; margin-bottom: 5px; font-size: 0.75rem;">Website Created by Piyush Patil</div>
</div>

<script>
    let ably, channel, mySecretCode, randomUserID;
    
    // १००% वर्किंग अधिकृत Ably API Key
    const ABLY_KEY = '7uX80Q.9H_MvA:sA37_Z2y_ZgR9b6M2WJstU_F6rN-P3NHeu4-S0xW5C0';

    function joinChat() {
        mySecretCode = document.getElementById('secretCode').value.trim();
        if(mySecretCode.length !== 5) { alert("कृपया बरोबर ५ अंकी कोड टाका भावा!"); return; }

        randomUserID = "User-" + Math.floor(1000 + Math.random() * 9000);
        document.getElementById('loginScreen').style.display = 'none';
        document.getElementById('chatScreen').style.display = 'flex';
        document.getElementById('roomTitle').innerText = "❤️ VIP ROOM: " + mySecretCode;

        ably = new Ably.Realtime({ key: ABLY_KEY, clientId: randomUserID });
        channel = ably.channels.get('room-' + mySecretCode);

        channel.subscribe('message', function(msg) { 
            if(msg.data.text === "===SYSTEM_CLEAR_CHAT===") {
                document.getElementById('msgBox').innerHTML = ""; 
            } else {
                displayMessage(msg.data.sender, msg.data.text); 
            }
        });

        channel.presence.subscribe('enter', updateOnlineCount);
        channel.presence.subscribe('leave', updateOnlineCount);
        channel.presence.enter();
        
        setInterval(getOnlineUsers, 1000); 
    }

    function sendMsg() {
        const input = document.getElementById('msgInput');
        const text = input.value.trim();
        if(text === "") return;
        
        channel.publish('message', { sender: randomUserID, text: text });
        input.value = "";
    }

    function clearAllMessages() {
        channel.publish('message', { sender: randomUserID, text: "===SYSTEM_CLEAR_CHAT===" });
    }

    document.addEventListener('contextmenu', event => event.preventDefault());
    function handleKeyPress(e) { if(e.key === 'Enter') sendMsg(); }

    function displayMessage(sender, text) {
        const msgBox = document.getElementById('msgBox');
        const msgDiv = document.createElement('div');
        
        if(sender === randomUserID) { 
            msgDiv.className = 'msg sent'; 
        } else { 
            msgDiv.className = 'msg received'; 
        }
        msgDiv.innerText = text;
        msgBox.appendChild(msgDiv);
        
        // प्रत्येक नवीन मेसेज आल्यावर स्क्रीन ऑटोमॅटिक खाली स्क्रोल होईल
        msgBox.scrollTop = msgBox.scrollHeight;
    }

    function getOnlineUsers() {
        channel.presence.get(function(err, members) {
            if(!err) {
                let count = members.length;
                document.getElementById('onlineCount').innerText = "Online: " + count;
                
                if (count >= 3) {
                    document.getElementById('intruderAlert').style.display = 'block';
                } else {
                    document.getElementById('intruderAlert').style.display = 'none';
                }
            }
        });
    }
    
    function updateOnlineCount() { getOnlineUsers(); }
    function panicClose() { window.location.href = "https://www.google.com"; }
</script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
