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
            font-size: 1.2rem;
            font-weight: bold;
            color: #ff2a5f;
            text-shadow: 0 0 10px rgba(255, 42, 95, 0.5);
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
        .panic-btn {
            background: none;
            border: none;
            font-size: 1.4rem;
            cursor: pointer;
            animation: pulse 1.2s infinite;
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
        input[type="text"] {
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
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.15); }
            100% { transform: scale(1); }
        }
    </style>
    <script src="https://cdn.ably.com/lib/ably.min-1.js"></script>
</head>
<body>

<div class="login-box" id="loginScreen">
    <h1>❤️ LOVERS PRIVATE CHAT ❤️</h1>
    <p style="color: #a1979b; margin-bottom: 25px;">पेज रिफ्रेश होताच सर्व गप्पा कायमच्या नष्ट होतील. मेसेज कॉपी करणे ब्लॉक आहे!</p>
    <input type="text" id="username" placeholder="तुमचे नाव टाका..." style="width:100%; padding:12px; margin-bottom:15px; background:#0a0507; border:1px solid #3a1a23; color:#fff; border-radius:10px; text-align:center; -webkit-user-select: text; user-select: text;"><br>
    <button class="send-btn" style="width:100%; padding:12px;" onclick="joinChat()">प्रवेश करा ➔</button>
</div>

<div class="chat-container" id="chatScreen" style="display: none;">
    <div class="chat-header">
        <div class="chat-title">❤️ LOVERS ROOM</div>
        <div style="display: flex; align-items: center; gap: 10px;">
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
    let ably, channel, myName;
    const ABLY_KEY = '7uX80Q.9H_MvA:sA37_Z2y_ZgR9b6M2WJstU_F6rN-P3NHeu4-S0xW5C0'; 

    function joinChat() {
        myName = document.getElementById('username').value.trim();
        if(myName === "") { alert("कृपया नाव टाका!"); return; }
        document.getElementById('loginScreen').style.display = 'none';
        document.getElementById('chatScreen').style.display = 'flex';
        ably = new Ably.Realtime({ key: ABLY_KEY, clientId: myName });
        channel = ably.channels.get('lovers-secret-room');
        channel.subscribe('message', function(msg) { displayMessage(msg.data.sender, msg.data.text); });
        channel.presence.subscribe('enter', updateOnlineCount);
        channel.presence.subscribe('leave', updateOnlineCount);
        channel.presence.enter();
        setInterval(getOnlineUsers, 2000);
    }
    function sendMsg() {
        const input = document.getElementById('msgInput');
        const text = input.value.trim();
        if(text === "") return;
        channel.publish('message', { sender: myName, text: text });
        input.value = "";
    }
    document.addEventListener('contextmenu', event => event.preventDefault());
    function handleKeyPress(e) { if(e.key === 'Enter') sendMsg(); }
    function displayMessage(sender, text) {
        const msgBox = document.getElementById('msgBox');
        const msgDiv = document.createElement('div');
        if(sender === myName) { msgDiv.className = 'msg sent'; msgDiv.innerText = text; } 
        else { msgDiv.className = 'msg received'; msgDiv.innerText = sender + ": " + text; }
        msgBox.appendChild(msgDiv);
        msgBox.scrollTop = msgBox.scrollHeight;
    }
    function getOnlineUsers() {
        channel.presence.get(function(err, members) {
            if(!err) document.getElementById('onlineCount').innerText = "Online: " + members.length;
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
