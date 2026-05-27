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
    <style>
        * { 
            box-sizing: border-box; 
            margin: 0; padding: 0; 
            -webkit-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        body {
            background: #0a0507;
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
            background: #140b0e;
            border: 2px solid #ff2a5f;
            border-radius: 20px;
            box-shadow: 0 0 35px rgba(255, 42, 95, 0.25);
            display: flex;
            flex-direction: column;
            height: 85vh;
            position: relative;
        }
        .chat-header {
            background: #221217;
            padding: 15px;
            border-bottom: 1px solid #3a1a23;
            display: flex;
            justify-content: space-between;
            align-items: center;
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
            border: 1px solid rgba(255, 42, 95, 0.3);
        }
        /* ३ पेक्षा जास्त युझर्स आले तर अलर्ट बॅनर */
        .intruder-alert {
            display: none;
            background: #7f1d1d;
            color: #fca5a5;
            padding: 8px;
            font-size: 0.9rem;
            text-align: center;
            font-weight: bold;
            border-bottom: 1px solid #ef4444;
            animation: flash 1s infinite alternate;
        }
        /* मेसेज क्लिअर करायचे स्पेशल बटण */
        .clear-btn {
            background: #221217;
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
            background: #0a0507;
        }
        .msg {
            max-width: 75%;
            padding: 11px 15px;
            border-radius: 15px;
            font-size: 1rem;
            line-height: 1.4;
            word-wrap: break-word;
        }
        .msg.sent {
            background: linear-gradient(135deg, #ff2a5f 0%, #ff5e3a 100%);
            color: #ffffff;
            align-self: flex-end;
            border-bottom-right-radius: 2px;
        }
        .msg.received {
            background: #221217;
            color: #f3e8ee;
            align-self: flex-start;
            border-bottom-left-radius: 2px;
            border: 1px solid #3a1a23;
        }
        .input-area {
            padding: 15px;
            background: #140b0e;
            border-top: 1px solid #3a1a23;
            display: flex;
            gap: 10px;
        }
        input[type="text"], input[type="number"] {
            flex: 1;
            padding: 12px;
            background: #0a0507;
            border: 1px solid #3a1a23;
            color: #ffffff;
            border-radius: 10px;
            outline: none;
            font-size: 1rem;
            -webkit-user-select: text;
            user-select: text;
        }
        input[type="text"]:focus, input[type="number"]:focus {
            border-color: #ff2a5f;
            box-shadow: 0 0 10px rgba(255, 42, 95, 0.2);
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
            background: #140b0e;
            border: 2px solid #ff2a5f;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
        }
        .login-box h1 {
            color: #ff2a5f;
            margin-bottom: 15px;
        }
        @keyframes flash {
            0% { background: #7f1d1d; }
            100% { background: #b91c1c; }
        }
    </style>
    <script src="https://cdn.ably.com/lib/ably.min-1.js"></script>
</head>
<body>

<div class="login-box" id="loginScreen">
    <h1>❤️ LOVERS VIP CHAT ❤️</h1>
    <p style="color: #a1979b; margin-bottom: 25px;">तुमची गुप्त व्हीआयपी रूम सुरू करण्यासाठी खाली कोणताही ५ अंकी कोड टाका. तुमच्या पार्टनरलाही तोच कोड टाकायला सांगा!</p>
    
    <input type="number" id="secretCode" placeholder="५ अंकी कोड टाका (उदा. १२३४५)" oninput="javascript: if (this.value.length > 5) this.value = this.value.slice(0, 5);" style="width:100%; padding:12px; margin-bottom:15px; background:#0a0507; border:1px solid #3a1a23; color:#ff2a5f; border-radius:10px; text-align:center; font-weight:bold; font-size:1.2rem;"><br>
    
    <button class="send-btn" style="width:100%; padding:12px;" onclick="joinChat()">रूममध्ये प्रवेश करा ➔</button>
</div>

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

    <div class="messages-box" id="msgBox"></div>

    <div class="input-area">
        <input type="text" id="msgInput" placeholder="मेसेज टाईप करा..." onkeypress="handleKeyPress(event)">
        <button class="send-btn" onclick="sendMsg()">Send</button>
    </div>
</div>

<script>
    let ably, channel, mySecretCode, randomUserID;
    const ABLY_KEY = '7uX80Q.9H_MvA:sA37_Z2y_ZgR9b6M2WJstU_F6rN-P3NHeu4-S0xW5C0'; 

    function joinChat() {
        mySecretCode = document.getElementById('secretCode').value.trim();
        
        if(mySecretCode.length !== 5) { 
            alert("कृपया बरोबर ५ अंकी कोड टाका भावा!"); 
            return; 
        }

        randomUserID = "User-" + Math.floor(1000 + Math.random() * 9000);

        document.getElementById('loginScreen').style.display = 'none';
        document.getElementById('chatScreen').style.display = 'flex';
        document.getElementById('roomTitle').innerText = "❤️ VIP ROOM: " + mySecretCode;

        ably = new Ably.Realtime({ key: ABLY_KEY, clientId: randomUserID });
        channel = ably.channels.get('room-' + mySecretCode);

        // लाईव्ह मेसेजेस ऐकणे
        channel.subscribe('message', function(msg) { 
            if(msg.data.text === "===SYSTEM_CLEAR_CHAT===") {
                document.getElementById('msgBox').innerHTML = ""; // सर्व स्क्रीन साफ करणे
            } else {
                displayMessage(msg.data.sender, msg.data.text); 
            }
        });

        channel.presence.subscribe('enter', updateOnlineCount);
        channel.presence.subscribe('leave', updateOnlineCount);
        channel.presence.enter();
        setInterval(getOnlineUsers, 1500); // वेगवान ट्रॅकिंगसाठी दर १.५ सेकंदाला अपडेट
    }

    function sendMsg() {
        const input = document.getElementById('msgInput');
        const text = input.value.trim();
        if(text === "") return;
        channel.publish('message', { sender: randomUserID, text: text });
        input.value = "";
    }

    // सर्व मेसेज साफ करून नवीन चॅट सुरू करण्याचे बटण लॉजिक
    function clearAllMessages() {
        channel.publish('message', { sender: randomUserID, text: "===SYSTEM_CLEAR_CHAT===" });
    }

    document.addEventListener('contextmenu', event => event.preventDefault());
    function handleKeyPress(e) { if(e.key === 'Enter') sendMsg(); }

    function displayMessage(sender, text) {
        const msgBox = document.getElementById('msgBox');
        const msgDiv = document.createElement('div');
        if(sender === randomUserID) { msgDiv.className = 'msg sent'; msgDiv.innerText = text; } 
        else { msgDiv.className = 'msg received'; msgDiv.innerText = text; }
        msgBox.appendChild(msgDiv);
        msgBox.scrollTop = msgBox.scrollHeight;
    }

    function getOnlineUsers() {
        channel.presence.get(function(err, members) {
            if(!err) {
                let count = members.length;
                document.getElementById('onlineCount').innerText = "Online: " + count;
                
                // जर ३ किंवा ३ पेक्षा जास्त युझर्स एकाच कोडवर आले तर अलर्ट बॅनर दाखवणे
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
