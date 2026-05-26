import os
from flask import Flask, render_template_string, request
import google.generativeai as genai

app = Flask(__name__)

# तुझी एआय चावी (API Key)
GEMINI_API_KEY = "AIzaSyDsPfScvWhfrWonRKT_KlaKFWUj7a_SJ3s"
genai.configure(api_key=GEMINI_API_KEY)

def get_ai_response(user_input):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"काहीतरी गडबड झाली: {str(e)}"

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
                background-image: linear-gradient(rgba(11,20,26,0.95), rgba(11,20,26,0.95)), url('https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png');
                display: flex; 
                flex-direction: column; 
                gap: 15px; 
            }
            .message { 
                max-width: 85%; 
                padding: 10px 14px; 
                border-radius: 10px; 
                font-size: 1rem; 
                line-height: 1.4;
                word-wrap: break-word;
                box-shadow: 0 1px 2px rgba(0,0,0,0.2);
                animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }
            .user-message { 
                background: #005c4b; 
                color: #e9edef;
                align-self: flex-end; 
                border-top-right-radius: 0; 
            }
            .ai-message { 
                background: #202c33; 
                color: #e9edef;
                align-self: flex-start; 
                border-top-left-radius: 0; 
                white-space: pre-wrap;
            }
            .chat-input-area { 
                padding: 12px; 
                background: #202c33; 
                border-top: 1px solid #2a3942; 
            }
            form { display: flex; gap: 8px; align-items: center; }
            input[type="text"] { 
                flex: 1; 
                padding: 12px 18px; 
                background: #2a3942;
                border: none;
                border-radius: 24px; 
                font-size: 1rem; 
                color: #e9edef;
                outline: none; 
            }
            input[type="text"]::placeholder { color: #8696a0; }
            button { 
                background: #00a884; 
                color: #111b21; 
                border: none; 
                width: 45px;
                height: 45px;
                border-radius: 50%; 
                font-size: 1rem; 
                cursor: pointer; 
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: transform 0.2s, background-color 0.2s;
            }
            button:hover { background: #00c69b; transform: scale(1.05); }
            button:active { transform: scale(0.95); }

            /* ॲनिमेशन्स */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes popIn {
                from { opacity: 0; transform: scale(0.9); }
                to { opacity: 1; transform: scale(1); }
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">
                <span>🤖</span> पियुषची स्मार्ट एआय चॅटरूम
            </div>
            <div class="chat-box">
                {% if user_msg %}
                    <div class="message user-message">{{ user_msg }}</div>
                {% endif %}
                {% if response %}
                    <div class="message ai-message">{{ response }}</div>
                {% endif %}
            </div>
            <div class="chat-input-area">
                <form method="POST">
                    <input type="text" name="msg" placeholder="एआय ला काहीही विचारा..." autocomplete="off" required>
                    <button type="submit">➔</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    """, response=response, user_msg=user_msg)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
