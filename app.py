from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'piyush_whatsapp_secret_key_2026'

# Render वर WebSocket व्यवस्थित चालण्यासाठी cors_allowed_origins ला * ठेवलं आहे
socketio = SocketIO(app, cors_allowed_origins="*")

# 📝 मेसेज सेव्ह करण्यासाठी एक तात्पुरती लिस्ट (सर्व्हर चालू असेपर्यंत मेसेज राहतील)
messages_history = []

@app.route('/')
def index():
    # आपण HTML आणि CSS कोड थेट इथेच लिहिला आहे, जेणेकरून वेगळा फोल्डर बनवायची गरज पडणार नाही
    html_template = '''
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VIP WhatsApp Clone</title>
        <script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
        <style>
            :root {
                --wa-bg: #efeae2;
                --wa-header: #008069;
                --wa-btn: #00a884;
                --chat-bg: #ffffff;
                --my-msg: #d9fdd3;
            }
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { font-family: Segoe UI, Helvetica Neue, Arial, sans-serif; background-color: #111b21; display: flex; justify-content: center; height: 100vh; }
            
            .chat-container { width: 100%; max-width: 500px; height: 100%; background: var(--wa-bg); display: flex; flex-direction: column; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
            
            /* Header */
            .chat-header { background: var(--wa-header); color: white; padding: 14px 18px; display: flex; align-items: center; gap: 10px; font-size: 18px; font-weight: bold; }
            .chat-header .status { font-size: 11px; color: #b3ffeb; font-weight: normal; margin-top: 2px; }
            
            /* Name Input Section */
            #name-block { background: #202c33; padding: 12px; display: flex; gap: 8px; border-bottom: 1px solid #2a3942; }
            #username-input { flex: 1; padding: 8px 14px; border: none; border-radius: 8px; outline: none; background: #2a3942; color: white; font-size: 14px; }
            
            /* Chat Box Area */
            .chat-box { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; background-image: url('https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png'); background-opacity: 0.4; }
            
            /* Message Bubbles */
            .msg { max-width: 75%; padding: 8px 12px; border-radius: 8px; font-size: 15px; line-height: 1.4; word-wrap: break-word; position: relative; box-shadow: 0 1px 1px rgba(0,0,0,0.1); }
            .msg-received { background: var(--chat-bg); color: #111b21; align-self: flex-start; border-top-left-radius: 0; }
            .msg-sent { background: var(--my-msg); color: #111b21; align-self: flex-end; border-top-right-radius: 0; }
            
            .msg-user { font-size: 11px; font-weight: bold; color: #53bdeb; margin-bottom: 2px; display: block; }
            .msg-sent .msg-user { color: #008069; }
            
            /* Footer Input */
            .chat-footer { background: #f0f2f5; padding: 10px 14px; display: flex; align-items: center; gap: 8px; }
            #message-input { flex: 1; padding: 11px 16px; border: none; border-radius: 20px; outline: none; font-size: 15px; background: white; }
            #send-btn { background: var(--wa-btn); color: white; border: none; width: 42px; height: 42px; border-radius: 50%; cursor: pointer; font-size: 18px; display: flex; align-items: center; justify-content: center; font-weight: bold; }
            #send-btn:hover { background: #008069; }
        </style>
    </head>
    <body>

        <div class="chat-container">
            <div class="chat-header">
                <div>
                    <div>🟢 VIP Live Chat</div>
                    <div class="status">सिस्टीम ऑनलाईन आहे बॉस...</div>
                </div>
            </div>

            <!-- नाव टाकण्यासाठी जागा -->
            <div id="name-block">
                <input type="text" id="username-input" placeholder="तुमचं नाव टाका (उदा. पीयुष पाटील)" value="User">
            </div>

            <!-- मेसेज दिसण्याची जागा -->
            <div class="chat-box" id="chatBox">
                <!-- आधीचे मेसेजेस लोड होतील -->
                {% for msg in history %}
                    <div class="msg {% if msg.id == session_id %}msg-sent{% else %}msg-received{% endif %}">
                        <span class="msg-user">{{ msg.user }}</span>
                        <div>{{ msg.text }}</div>
                    </div>
                {% endfor %}
            </div>

            <!-- मेसेज टाईप करण्याची जागा -->
            <div class="chat-footer">
                <input type="text" id="message-input" placeholder="मेसेज टाईप करा चीफ..." autocomplete="off">
                <button id="send-btn" onclick="sendMessage()">➔</button>
            </div>
        </div>

        <script>
            // Render च्या सर्व्हरशी लाईव्ह कनेक्शन जोडणे
            const socket = io();

            const chatBox = document.getElementById('chatBox');
            const messageInput = document.getElementById('message-input');
            const usernameInput = document.getElementById('username-input');

            // स्क्रीन नेहमी स्क्रोल करून खाली ठेवण्यासाठी
            chatBox.scrollTop = chatBox.scrollHeight;

            // सर्व्हरवरून नवीन मेसेज आल्यावर तो स्क्रीनवर दाखवणे
            socket.on('receive_message', function(data) {
                const msgDiv = document.createElement('div');
                msgDiv.classList.add('msg');
                
                // मेसेज स्वतःचा आहे की दुसऱ्याचा त्यानुसार डिझाईन ठरवणे
                if (data.sender_id === socket.id) {
                    msgDiv.classList.add('msg-sent');
                } else {
                    msgDiv.classList.add('msg-received');
                }

                msgDiv.innerHTML = `<span class="msg-user">${data.user}</span><div>${data.text}</div>`;
                chatBox.appendChild(msgDiv);
                chatBox.scrollTop = chatBox.scrollHeight; // ऑटो स्क्रोल खाली जाण्यासाठी
            });

            // मेसेज पाठवणारे फंक्शन
            function sendMessage() {
                const text = messageInput.value.trim();
                const user = usernameInput.value.trim() || "Anonymous";

                if (text !== "") {
                    // सर्व्हरला मेसेज पाठवा
                    socket.emit('send_message', {
                        text: text,
                        user: user
                    });
                    messageInput.value = '';
                }
            }

            // Enter बटण दाबलं तरी मेसेज गेला पाहिजे
            messageInput.addEventListener("keyup", function(event) {
                if (event.key === "Enter") {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_template, history=messages_history)

# 🌐 लाईव्ह मेसेज हँडलर
@socketio.on('send_message')
def handle_message(data):
    msg_data = {
        'text': data['text'],
        'user': data['user'],
        'sender_id': request.sid  # युझरचा युनिक आयडी
    }
    # मेसेज हिस्ट्रीमध्ये सेव्ह करा
    messages_history.append(msg_data)
    
    # हा मेसेज सर्वांना एकाच वेळी स्क्रीनवर लाईव्ह पाठवा
    emit('receive_message', msg_data, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    # Render वर लाईव्ह चॅटिंगसाठी socketio.run वापरणे आवश्यक आहे
    socketio.run(app, host='0.0.0.0', port=port)
