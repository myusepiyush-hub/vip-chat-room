import os
from flask import Flask, render_template_string, request
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

@app.route('/', methods=['GET', 'POST'])
def chat():
    response = ""
    user_msg = ""
    if request.method == 'POST':
        user_msg = request.form.get('msg')
        if user_msg:
            response = get_ai_response(user_msg)

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
            animation: fadeIn 0.5s ease-in-out;
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
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
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
            transition: background 0.2s;
        }
        .input-area button:hover { background: #00bf96; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="chat-header">
        🤖 पियुषची स्मार्ट एआय चॅटरूम
    </div>
    <div class="chat-box" id="chatBox">
        {% if user_msg %}
            <div class="message user-message">{{ user_msg }}</div>
        {% endif %}
        {% if response %}
            <div class="message ai-message">{{ response }}</div>
        {% endif %}
    </div>
    <form class="input-area" method="POST" action="/">
        <input type="text" name="msg" placeholder="एआय ला काहीही विचारा..." required autocomplete="off">
        <button type="submit">➔</button>
    </form>
</div>

<script>
    var chatBox = document.getElementById('chatBox');
    chatBox.scrollTop = chatBox.scrollHeight;
</script>

</body>
</html>
    """)

if __name__ == '__main__':
    app.run(debug=True)
