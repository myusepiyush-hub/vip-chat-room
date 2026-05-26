import os
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Piyush VIP Surprise</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #0f0c20 0%, #06040a 100%);
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }
        .container {
            text-align: center;
            padding: 30px;
            width: 100%;
            max-width: 450px;
        }
        .glitch-title {
            font-size: 2.5rem;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 3px;
            color: #00ffcc;
            text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
            margin-bottom: 20px;
            animation: pulse 2s infinite;
        }
        .subtitle {
            color: #8a85a0;
            font-size: 1rem;
            margin-bottom: 40px;
        }
        .surprise-btn {
            background: transparent;
            border: 2px solid #ff007f;
            color: #ff007f;
            padding: 15px 40px;
            font-size: 1.2rem;
            font-weight: bold;
            text-transform: uppercase;
            border-radius: 50px;
            cursor: pointer;
            outline: none;
            box-shadow: 0 0 15px rgba(255, 0, 127, 0.2);
            transition: all 0.4s ease;
        }
        .surprise-btn:hover {
            background: #ff007f;
            color: #fff;
            box-shadow: 0 0 25px #ff007f, 0 0 50px #ff007f;
            transform: scale(1.05);
        }
        .box-content {
            display: none;
            margin-top: 30px;
            padding: 25px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            animation: slideUp 0.6s ease forwards;
        }
        .box-content h2 {
            color: #00ffcc;
            font-size: 1.8rem;
            margin-bottom: 15px;
        }
        .box-content p {
            color: #e0e0e0;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        .emoji-rain {
            font-size: 3rem;
            margin-top: 15px;
            animation: bounce 1s infinite alternate;
        }
        @keyframes pulse {
            0% { transform: scale(1); text-shadow: 0 0 10px #00ffcc; }
            50% { transform: scale(1.02); text-shadow: 0 0 20px #00ffcc, 0 0 30px #00ffcc; }
            100% { transform: scale(1); text-shadow: 0 0 10px #00ffcc; }
        }
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes bounce {
            from { transform: translateY(0); }
            to { transform: translateY(-10px); }
        }
    </style>
</head>
<body>

<div class="container">
    <div class="glitch-title">PIYUSH VIP</div>
    <div class="subtitle">काहीतरी वेगळं आणि कडक शोधणाऱ्यांसाठी...</div>
    
    <button class="surprise-btn" id="clickBtn">इथे क्लिक कर भावा</button>
    
    <div class="box-content" id="surpriseBox">
        <h2>🔥 विषयच एंड भावा! 🔥</h2>
        <p>जेव्हा आपल्याला माहित नसतं की नक्की काय करायचंय, तेव्हाच काहीतरी इतिहास रचणारं बनतं! तुझी ही पूर्ण वेबसाईट आता विना-एरर आणि सुपरफास्ट झाली आहे.</p>
        <div class="emoji-rain">😎🚀👑</div>
    </div>
</div>

<script>
    document.getElementById('clickBtn').addEventListener('click', function() {
        const box = document.getElementById('surpriseBox');
        this.style.display = 'none'; // बटन लपवून टाका
        box.style.display = 'block'; // सरप्राईज दाखवा
    });
</script>

</body>
</html>
    """)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
