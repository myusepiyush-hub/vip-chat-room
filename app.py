from flask import Flask, render_template_string, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'piyush_ultra_secure_chat_2026'
socketio = SocketIO(app, cors_allowed_origins="*")

# 🔒 डेटाबेऐवजी तात्पुरती मेमरी (सर्व्हर चालू असेपर्यंत युजर्स आणि रूम्स राहतील)
# तुम्ही कोणताही युझरनेम आणि पासवर्ड टाकून लॉगिन करू शकता!
USERS = {} 
ROOMS = {} # रूम कोड आणि त्यातील मेसेज साठवण्यासाठी

html_template = '''
<!DOCTYPE html>
<html lang="mr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VIP Room Chat System</title>
    <script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
    <style>
        :root {
            --bg-dark: #111b21; --panel-bg: #202c33; --wa-green: #00a884;
            --text-light: #e9edef; --text-muted: #8696a0; --msg-sent: #005c4b; --msg-rcv: #202c33;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: var(--bg-dark); color: var(--text-light); display: flex; justify-content: center; align-items: center; height: 100vh; }
        
        .container { width: 100%; max-width: 450px; height: 90vh; background: #0b141a; display: flex; flex-direction: column; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 25px rgba(0,0,0,0.5); }
        .header { background: var(--panel-bg); padding: 15px; text-align: center; font-size: 18px; font-weight: bold; border-bottom: 1px solid #2f3b43; color: var(--wa-green); }
        
        /* Forms styling */
        .page-box { padding: 30px; display: flex; flex-direction: column; gap: 15px; justify-content: center; height: 100%; }
        input { width: 100%; padding: 12px 16px; border: 1px solid #2f3b43; border-radius: 8px; background: var(--panel-bg); color: white; font-size: 15px; outline: none; }
        input:focus { border-color: var(--wa-green); }
        button { width: 100%; padding: 12px; background: var(--wa-green); color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.2s; }
        button:hover { background: #008069; }
        .error { color: #f25c5c; font-size: 13px; text-align: center; }

        /* Chat Window styling */
        .chat-area { flex: 1; display: flex; flex-direction: column; height: 100%; }
        .room-info { background: var(--panel-bg); padding: 10px 15px; font-size: 13px; color: var(--text-muted); display: flex; justify-content: space-between; align-items: center; }
        .chat-messages { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; background-image: url('https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png'); }
        
        .msg { max-width: 75%; padding: 8px 12px; border-radius: 8px; font-size: 15px; line-height: 1.4; word-wrap: break-word; }
        .sent { background: var(--msg-sent); align-self: flex-end; border-top-right-radius: 0; }
        .rcv { background: var(--msg-rcv); align-self: flex-start; border-top-left-radius: 0; }
        .msg-user { font-size: 11px; font-weight: bold; color: #53bdeb; margin-bottom: 2px; display: block; }
        .system-msg { background: rgba(255,255,255,0.05); color: var(--text-muted); align-self: center; font-size: 12px; padding: 4px 10px; border-radius: 6px; }

        .chat-footer { padding: 10px; background: #1f2c34; display: flex; gap: 8px; align-items: center; }
        .chat-footer input { flex: 1; border-radius: 20px; }
        .chat-footer button { width: 42px; height: 42px; border-radius: 50%; padding: 0; display: flex; align-items: center; justify-content: center; }
    </style>
</head>
<body>

    <div class="container">
        <!-- १. लॉगिन पेज -->
        {% if page == 'login' %}
            <div class="header">🔐 VIP Secure Login</div>
            <form class="page-box" method="POST" action="/login">
                <input type="text" name="username" placeholder="युझरनेम टाका..." required>
                <input type="password" name="password" placeholder="पासवर्ड सेट करा..." required>
                <button type="submit">लॉगिन / रजिस्ट्रेशन करा</button>
                {% if error %}<div class="error">{{ error }}</div>{% endif %}
            </form>

        <!-- २. रूम सिलेक्ट करण्याचा पेज -->
        {% elif page == 'dashboard' %}
            <div class="header">👋 स्वागत आहे, {{ username }}!</div>
            <div class="page-box">
                <form method="POST" action="/join-room" style="display:flex; flex-direction:column; gap:12px;">
                    <h4 style="color: var(--text-muted);">प्रायव्हेट रूम जॉईन करा:</h4>
                    <input type="text" name="room_code" placeholder="गुपीत रूम कोड टाका (उदा. 9999)..." required>
                    <button type="submit">रूममध्ये प्रवेश करा ➔</button>
                </form>
                <hr style="border: 0; border-top: 1px solid #2f3b43; margin: 10px 0;">
                <a href="/logout" style="text-align:center; color:#f25c5c; text-decoration:none; font-size:14px;">लॉगआउट करा</a>
            </div>

        <!-- ३. मुख्य लाईव्ह चॅटिंग रूम -->
        {% elif page == 'chat' %}
            <div class="chat-area">
                <div class="header">💬 {{ room_code }} - प्रायव्हेट रूम</div>
                <div class="room-info">
                    <span>युझर: <b>{{ username }}</b></span>
                    <a href="/dashboard" style="color: #f25c5c; text-decoration: none; font-weight:bold;">रूम सोडा ❌</a>
                </div>
                
                <div class="chat-messages" id="chatBox">
                    <!-- जुने मेसेजेस लोड करणे -->
                    {% for m in history %}
                        <div class="msg {% if m.user == username %}sent{% else %}rcv{% endif %}">
                            <span class="msg-user">{{ m.user }}</span>
                            <div>{{ m.text }}</div>
                        </div>
                    {% endfor %}
                </div>

                <div class="chat-footer">
                    <input type="text" id="msgInput" placeholder="मेसेज टाईप करा चीफ..." autocomplete="off">
                    <button onclick="sendLiveMsg()">➔</button>
                </div>
            </div>

            <script>
                const socket = io();
                const chatBox = document.getElementById('chatBox');
                const msgInput = document.getElementById('msgInput');
                
                chatBox.scrollTop = chatBox.scrollHeight;

                // रूममध्ये ऑटोमॅटिकली कनेक्ट होणे (Socket Rooms)
                socket.emit('join', { username: "{{ username }}", room: "{{ room_code }}" });

                // सर्व्हरकडून येणारे मेसेज स्क्रीनवर दाखवणे
                socket.on('message', function(data) {
                    const div = document.createElement('div');
                    if (data.user === "System") {
                        div.className = "system-msg";
                        div.innerText = data.text;
                    } else {
                        div.className = "msg " + (data.user === "{{ username }}" ? "sent" : "rcv");
                        div.innerHTML = `<span class="msg-user">${data.user}</span><div>${data.text}</div>`;
                    }
                    chatBox.appendChild(div);
                    chatBox.scrollTop = chatBox.scrollHeight;
                });

                function sendLiveMsg() {
                    const txt = msgInput.value.trim();
                    if(txt !== "") {
                        socket.emit('text_message', { text: txt, room: "{{ room_code }}", username: "{{ username }}" });
                        msgInput.value = "";
                    }
                }

                msgInput.addEventListener("keyup", function(e) { if(e.key === "Enter") sendLiveMsg(); });
            </script>
        {% endif %}
    </div>

</body>
</html>
'''

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template_string(html_template, page='login')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    
    if not username or not password:
        return render_template_string(html_template, page='login', error="कृपया सर्व माहिती भरा.")
    
    # सोपी रजिस्ट्रेशन आणि लॉगिन सिस्टीम
    if username in USERS:
        if USERS[username] != password:
            return render_template_string(html_template, page='login', error="पासवर्ड चुकीचा आहे!")
    else:
        USERS[username] = password # नवीन युझर सेव्ह करा
        
    session['username'] = username
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session: return redirect(url_for('home'))
    return render_template_string(html_template, page='dashboard', username=session['username'])

@app.route('/join-room', methods=['POST'])
def join_user_room():
    if 'username' not in session: return redirect(url_for('home'))
    room_code = request.form.get('room_code').strip().upper()
    
    if not room_code: return redirect(url_for('dashboard'))
    
    session['room'] = room_code
    if room_code Pallavi not in ROOMS:
        ROOMS[room_code] = [] # नवीन रूम तयार करा
        
    return render_template_string(html_template, page='chat', username=session['username'], room_code=room_code, history=ROOMS[room_code])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# 🌐 SOCKET.IO इव्हेंट्स (रूम मॅनेजमेंट)
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room) # युझरला त्या विशिष्ट रूम कोडच्या ग्रुपमध्ये पाठवणे
    emit('message', {'user': 'System', 'text': f'🔹 {username} रूममध्ये सामील झाला आहे.'}, room=room)

@socketio.on('text_message')
def on_message(data):
    room = data['room']
    msg_data = {'user': data['username'], 'text': data['text']}
    ROOMS[room].append(msg_data) # मेसेज रूमच्या हिस्ट्रीमध्ये सेव्ह करा
    emit('message', msg_data, room=room) # फक्त त्याच रूममधील लोकांना मेसेज पाठवा

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port)
