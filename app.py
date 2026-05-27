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
    
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>

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
            background: #000000;
        }
        .msg {
            max-width: 75%;
            padding: 11px 15px;
            border-radius: 15px;
            font-size: 1rem;
            line-height: 1.4;
            word-wrap: break-word;
        }
        /* Your Message - Pink gradient with guaranteed white text */
        .msg.sent {
            background: linear-gradient(135deg, #ff2a5f 0%, #ff5e3a 100%);
            color: #ffffff !important;
            align-self: flex-end;
            border-bottom-right-radius: 2px;
            box-shadow: 0 2px 8px rgba(255, 42, 95, 0.3);
        }
        /* Partner Message - Dark grey with guaranteed white text */
        .msg.received {
            background: #1a1a1a;
            color: #ffffff !important;
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
            background: #000000;
            border: 2px solid #ff2a5f;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 0 35px rgba(255, 42, 95, 0.35);
        }
        .login-box h1 {
            color: #ff2a5f;
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(255, 42, 95, 0.4);
        }
        
        /* 🟢 SPECIAL UPDATE NOTICE STYLE 🟢 */
        .update-badge {
            display: inline-block;
            background: rgba(34, 197, 94, 0.15);
            color: #22c55e;
            border: 1px solid #22c55e;
            padding: 5px 12px;
            font-size: 0.8rem;
            font-weight: bold;
            border-radius: 20px;
            margin-bottom: 20px;
            text-shadow: 0 0 5px rgba(34, 197, 94, 0.4);
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

<div class="login-box" id="loginScreen">
    <div class="update-badge">🟢 SYSTEM UPDATE: VER 2.0 (LIVE & PERFECT)</div>

    <h1>❤️ LOVERS VIP CHAT ❤️</h1>
    <p style="color: #a1979b; margin-bottom: 25px;">गुप्त व्हीआयपी रूमसाठी खाली कोणताही ५ अंकी कोड टाका. पार्टनरलाही तोच कोड टाकायला सांगा!</p>
    
    <input type="number" id="secretCode" placeholder="५ अंकी कोड टाका (उदा. १२३४५)" oninput="javascript: if (this.value.length > 5) this.value = this.value.slice(0, 5);" style="width:100%; padding:12px; margin-bottom:15px; background:#000000; border:1px solid #ff2a5f; color:#ff2a5f; border-radius:10px; text-align:center; font-weight:bold; font-size:1.2rem;"><br>
    
    <button class="send-btn" style="width:100%; padding:12px;" onclick="joinChat()">रूममध्ये प्रवेश करा ➔</button>
    
    <div class="credit-text">Website Created by Piyush Patil</div>
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
    
    <div class="credit-text" style="text-align: center; margin-top: 5px; margin-bottom: 5px; font-size: 0.75rem;">Website Created by Piyush Patil</div>
</div>

<script>
    const SB_URL = "https://wzscxlscbttvscfuyvaw.supabase.co";
    const SB_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind6c2N4bHNjYnR0dnNjZnV5dmF3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTY4MzQ4MDAsImV4cCI6MjAzMjQxMDgwMH0.bXNmaWxlX3JlYWx0aW1lX3dvcmtzaGFyZV9waXl1c2hfcGF0aWw";
    
    const supabaseClient = supabase.createClient(SB_URL, SB_KEY);
    let mySecretCode, randomUserID, chatChannel;

    function joinChat() {
        mySecretCode = document.getElementById('secretCode').value.trim();
        if(mySecretCode.length !== 5) { alert("कृपया बरोबर ५ अंकी कोड टाका भावा!"); return; }

        randomUserID = "User-" + Math.floor(1000 + Math.random() * 9000);
        document.getElementById('loginScreen').style.display = 'none';
        document.getElementById('chatScreen').style.display = 'flex';
        document.getElementById('roomTitle').innerText = "❤️ VIP ROOM: " + mySecretCode;

        chatChannel = supabaseClient.channel('room-' + mySecretCode, {
            config: { presence: { key: randomUserID } }
        });

        chatChannel
        .on('broadcast', { event: 'shout' }, (payload) => {
            if(payload.payload.text === "===SYSTEM_CLEAR_CHAT===") {
                document.getElementById('msgBox').innerHTML = "";
            } else {
                displayMessage(payload.payload.sender, payload.payload.text);
            }
        })
        .on('presence', { event: 'sync' }, () => {
            let state = chatChannel.presenceState();
            let count = Object.keys(state).length;
            document.getElementById('onlineCount').innerText = "Online: " + count;
            
            if (count >= 3) {
                document.getElementById('intruderAlert').style.display = 'block';
            } else {
                document.getElementById('intruderAlert').style.display = 'none';
            }
        })
        .subscribe(async (status) => {
            if (status === 'SUBSCRIBED') {
                await chatChannel.track({ online_at: new Date().toISOString() });
            }
        });
    }

    function sendMsg() {
        const input = document.getElementById('msgInput');
        const text = input.value.trim();
        if(text === "") return;
        
        chatChannel.send({
            type: 'broadcast',
            event: 'shout',
            payload: { sender: randomUserID, text: text }
        });
        input.value = "";
    }

    // Clear system to reset screen text
    function clearAllMessages() {
        chatChannel.send({
            type: 'broadcast',
            event: 'shout',
            payload: { sender: randomUserID, text: "===SYSTEM_CLEAR_CHAT===" }
        });
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
        msgBox.scrollTop = msgBox.scrollHeight;
    }

    function panicClose() { window.location.href = "https://www.google.com"; }
</script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
