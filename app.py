import os
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="mr">
<head>
    <meta charset="UTF-8">
    <title>🏫 Patil College Connection 🏫</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: linear-gradient(135deg, #090a0f 0%, #020305 100%);
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 10px;
            overflow: hidden;
        }
        .app-container {
            width: 100%;
            max-width: 450px;
            height: 92vh;
            background: #11141a;
            border: 2px solid #ff0055;
            border-radius: 24px;
            padding: 15px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 0 30px rgba(255, 0, 85, 0.25);
            position: relative;
        }
        .header {
            text-align: center;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .header h1 {
            color: #ff0055;
            font-size: 1.4rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .header p {
            color: #33ff33;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        /* व्हिडिओ कॉलिंग एरिया */
        .video-grid {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin: 15px 0;
        }
        
        /* समोरच्याचा व्हिडिओ (स्ट्रेंजर) */
        .remote-video-box {
            flex: 1.2;
            background: #000;
            border-radius: 16px;
            overflow: hidden;
            border: 2px solid #00f0ff;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .stranger-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        /* स्वतःचा व्हिडिओ (लोकल कॅमेरा) */
        .local-video-box {
            flex: 0.8;
            background: #000;
            border-radius: 16px;
            overflow: hidden;
            border: 2px solid #33ff33;
            position: relative;
        }
        #localVideo {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transform: scaleX(-1);
        }
        
        .tag {
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(0,0,0,0.7);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: bold;
            letter-spacing: 1px;
            z-index: 10;
        }
        .tag-stranger { color: #00f0ff; }
        .tag-local { color: #33ff33; }
        
        /* कंट्रोल बटण */
        .control-area {
            padding-top: 5px;
        }
        .skip-btn {
            background: linear-gradient(135deg, #ff0055 0%, #990033 100%);
            color: white;
            border: none;
            padding: 16px;
            font-size: 1.2rem;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            width: 100%;
            box-shadow: 0 4px 15px rgba(255, 0, 85, 0.4);
            text-transform: uppercase;
            transition: all 0.2s ease;
            letter-spacing: 1px;
        }
        .skip-btn:active {
            transform: scale(0.95);
            box-shadow: 0 0 5px rgba(255, 0, 85, 0.2);
        }
    </style>
</head>
<body>

<div class="app-container">
    <div class="header">
        <h1>PATIL CONNECT</h1>
        <p>🟢 ऑनलाईन युझर्स: ७,४२०</p>
    </div>

    <div class="video-grid">
        <!-- समोरचा माणूस -->
        <div class="remote-video-box">
            <div class="tag tag-stranger">🔴 STRANGER [COLLEGE]</div>
            <img id="strangerView" class="stranger-img" src="https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=500&q=80" alt="Stranger">
        </div>
        
        <!-- स्वतःचा फेस -->
        <div class="local-video-box">
            <div class="tag tag-local">👦 तुम्ही (YOU)</div>
            <video id="localVideo" autoplay playsinline muted></video>
        </div>
    </div>

    <div class="control-area">
        <button class="skip-btn" id="skipBtn">NEXT (SKIP) ➔</button>
    </div>
</div>

<script>
    // वेगवेगळ्या ऑनलाईन लोकांचे फोटो (हुबेहूब व्हिडिओ कॉल सुरू असल्यासारखं दिसेल)
    const strangers = [
        "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=500&q=80",
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=500&q=80",
        "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=500&q=80",
        "https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?auto=format&fit=crop&w=500&q=80",
        "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=500&q=80"
    ];

    let currentIdx = 0;

    // स्वतःचा कॅमेरा सुरू करणे
    async function initCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            document.getElementById('localVideo').srcObject = stream;
        } catch (err) {
            console.error("Camera access denied", err);
        }
    }

    // SKIP बटण दाबल्यावर लगेच पुढचा माणूस आणणे
    document.getElementById('skipBtn').addEventListener('click', function() {
        const strangerImg = document.getElementById('strangerView');
        
        // एक छोटा 'Connecting' लुक देण्यासाठी तात्पुरतं ब्लॅक करणे
        strangerImg.style.opacity = "0.3";
        this.innerText = "SEARCHING...";
        
        setTimeout(() => {
            // पुढचा रँडम व्यक्ती निवडणे
            let nextIdx = Math.floor(Math.random() * strangers.length);
            while(nextIdx === currentIdx) { 
                nextIdx = Math.floor(Math.random() * strangers.length);
            }
            currentIdx = nextIdx;
            
            strangerImg.src = strangers[currentIdx];
            strangerImg.style.opacity = "1";
            this.innerText = "NEXT (SKIP) ➔";
        }, 400); // अवघ्या ०.४ सेकंदात कॉल कनेक्ट होईल
    });

    window.onload = initCamera;
</script>

</body>
</html>
    """)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
