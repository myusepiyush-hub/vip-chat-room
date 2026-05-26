import os
from flask import Flask, render_template_string, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# API Key Configuration
GEMINI_API_KEY = "AIzaSyDsPfScvWhfrWonRKT_KlaKFWUj7a_SJ3s"
genai.configure(api_key=GEMINI_API_KEY)

def get_ai_response(user_input):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET'])
def index():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Piyush AI Chatroom</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #0b141a;
            color: #e9edef;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .chat-container {
            width: 100%;
            max-width: 500px;
            height: 100vh;
            background: #111b21;
            display: flex;
            flex-direction: column;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        @media (min-width: 501px) {
            .chat-container { height: 90vh; border-radius: 15px; overflow: hidden; }
        }
        .chat-header {
            background: #202c33;
            padding: 16px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: bold;
            color: #00a884;
            border-bottom: 1px solid #2a3942;
        }
        .chat-box {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background-image: radial-gradient(circle, #0b141a 10%, transparent 11%);
            background-size: 12px 12px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .message {
            max-width: 75%;
            padding: 10px 14px;
            border-radius: 12px;
            font-size: 0.95rem;
            line-height: 1.4;
            word-wrap: break-word;
            box-shadow: 0 1px 2px rgba(0,0,0,0.2);
        }
        .user-message {
            background-color: #005c4b;
            color: #e9edef;
            align-self: flex-end;
            border-top-right-radius: 0;
        }
        .ai-message {
            background-color: #202c33;
            color: #e9edef;
            align-self: flex-start;
            border-top-left-radius: 0;
        }
        .typing {
            color: #8696a0;
            font-style: italic;
            font-size: 0.85rem;
            align-self: flex-start;
        }
        .input-area {
            background: #202c33;
            padding: 10px 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .input-area input {
            flex: 1;
            background: #2a3942;
            border: none;
            padding: 12px 18px;
            border-radius: 24px;
            color: #e9edef;
            font-size: 1rem;
            outline: none;
        }
        .input-area input::placeholder { color: #8696a0; }
        .input-area button {
            background: #00a884;
            border: none;
            width: 45px;
            height: 45px;
            border-radius: 50%;
            color: #111b21;
            font-size: 1.2rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="chat-header">
        🤖 पियुषची स्मार्ट एआय चॅटरूम
    </div>
    <div class="chat-box" id="chatBox">
        <div class="message ai-message">नमस्कार! मी तुमचा एआय मित्र आहे. मला काहीही विचारा...</div>
    </div>
    <div class="input-area">
        <input type="text" id="userInput" placeholder="एआय ला काहीही विचारा..." autocomplete="off">
        <button id="sendBtn">➔</button>
    </div>
</div>

<script>
    const chatBox = document.getElementById('chatBox');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');

    userInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    sendBtn.addEventListener("click", function() {
        sendMessage();
    });

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        appendMessage(text, 'user-message');
        userInput.value = '';

        const typingId = 'typing-' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message typing';
        typingDiv.id = typingId;
        typingDiv.innerText = 'AI विचार करत आहे...';
        chatBox.appendChild(typingDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            const response = await fetch('/get_response', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ msg: text })
            });
            const data = await response.json();
            
            const typingElement = document.getElementById(typingId);
            if(typingElement) typingElement.remove();
            
            appendMessage(data.response, 'ai-message');
        } catch (error) {
            const typingElement = document.getElementById(typingId);
            if(typingElement) typingElement.remove();
            appendMessage("Error: Could not connect to server.", 'ai-message');
        }
    }

    function appendMessage(text, className) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${className}`;
        messageDiv.innerText = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
</script>

</body>
</html>
    """)

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_msg = data.get('msg', '')
    ai_reply = get_ai_response(user_msg)
    return jsonify({'response': ai_reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
