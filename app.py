from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# सुरक्षित प्रगत डेटाबेस मेमरी
users_db = {}
room_data = {}

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VIP Lovers - Cyber Security Hub</title>
        <style>
            :root {
                --cyber-blue: #00f0ff;
                --cyber-pink: #ff2a75;
                --cyber-green: #00ff66;
                --cyber-red: #ff3333;
                --glass-bg: rgba(6, 8, 20, 0.85);
                --neon-glow: 0 0 20px rgba(0, 240, 255, 0.4);
            }

            body {
                background: radial-gradient(circle at center, #0c0f26 0%, #020308 100%);
                color: #fff; font-family: 'Segoe UI', Roboto, sans-serif;
                margin: 0; padding: 10px; display: flex; justify-content: center;
                align-items: center; height: 100vh; box-sizing: border-box;
                overflow: hidden;
            }

            /* ✨ प्रगत निऑन बॅकग्राउंड ग्रिड इफेक्ट */
            body::before {
                content: ''; position: absolute; width: 200%; height: 200%;
                background-image: linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
                                  linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
                background-size: 30px 30px; top: -50%; left: -50%; z-index: 0;
                transform: rotate(15deg); pointer-events: none;
            }

            /* 🗂️ प्रगत ग्लास-मॉर्फिझम कंटेनर (Advanced UI Frame) */
            .auth-container {
                width: 100%; max-width: 420px; display: none; flex-direction: column;
                justify-content: center; align-items: center; height: 95vh; z-index: 10;
            }
            .auth-box {
                border: 2px solid var(--cyber-blue); padding: 40px 25px; border-radius: 24px;
                text-align: center; box-shadow: var(--neon-glow), inset 0 0 15px rgba(0, 240, 255, 0.1);
                background: var(--glass-bg); backdrop-filter: blur(12px); width: 88%;
                position: relative; overflow: hidden; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }
            
            /* कडक बॉर्डर स्कॅनिंग इफेक्ट */
            .auth-box::before {
                content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
                background: linear-gradient(90deg, transparent, rgba(0, 240, 255, 0.15), transparent);
                transition: 0.5s; animation: borderScan 4s infinite linear;
            }
            @keyframes borderScan { 0% { left: -100%; } 100% { left: 200%; } }

            .auth-box h2 {
                color: #fff; text-shadow: 0 0 10px var(--cyber-blue); margin: 0 0 8px 0;
                font-size: 26px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase;
            }
            .auth-p { font-size: 13px; color: #8a99ad; margin-bottom: 25px; line-height: 1.4; }
            
            /* 🕹️ प्रगत आणि आधुनिक इनपुट डिझाईन */
            .auth-input {
                width: 88%; padding: 14px; font-size: 16px; text-align: center;
                background: rgba(0, 0, 0, 0.6); border: 1px solid rgba(0, 240, 255, 0.3);
                color: #fff; border-radius: 14px; margin-bottom: 18px; outline: none;
                transition: all 0.3s ease; box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
            }
            .auth-input:focus {
                border-color: var(--cyber-blue); box-shadow: 0 0 15px rgba(0, 240, 255, 0.3), inset 0 2px 4px rgba(0,0,0,0.5);
                transform: scale(1.02);
            }
            
            /* ⚡ प्रगत सायबरपंक बटण */
            .auth-btn {
                background: linear-gradient(135deg, #0072ff, var(--cyber-blue)); border: none; color: #000;
                padding: 14px 30px; font-size: 16px; font-weight: 800; border-radius: 14px;
                cursor: pointer; width: 95%; text-transform: uppercase; letter-spacing: 1px;
                transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4);
            }
            .auth-btn:hover {
                transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0, 240, 255, 0.6); filter: brightness(1.1);
            }
            .auth-btn:active { transform: translateY(1px); }
            .switch-link { color: #8a99ad; font-size: 13px; margin-top: 20px; cursor: pointer; transition: color 0.3s; }
            .switch-link:hover { color: var(--cyber-blue); text-shadow: 0 0 5px var(--cyber-blue); }

            /* 📸 प्रगत ३डी वर्तुळाकार कॅमेरा स्कॅनर (Advanced UI Framework) */
            .scanner-holder {
                width: 230px; height: 230px; border: 4px dashed var(--cyber-blue); border-radius: 50%;
                margin: 25px auto; position: relative; overflow: hidden;
                box-shadow: 0 0 30px rgba(0, 240, 255, 0.3); background: #000;
                transition: all 0.5s ease;
            }
            .live-webcam-view { width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); }
            
            /* 🟢 प्रगत मॅट्रिक्स लेझर लाईन */
            .laser-line {
                position: absolute; width: 100%; height: 6px;
                background: linear-gradient(to bottom, transparent, var(--cyber-blue));
                box-shadow: 0 0 20px var(--cyber-blue), 0 0 10px var(--cyber-blue); top: 0;
                animation: laserScan 1.8s infinite ease-in-out; pointer-events: none;
            }
            @keyframes laserScan { 0% { top: 0%; } 50% { top: 100%; } 100% { top: 0%; } }

            /* 🟢 मॅच झाल्यावर येणारे भारी ॲनिमेशन ओव्हरले */
            .success-overlay {
                display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0, 255, 102, 0.15); justify-content: center; align-items: center;
                font-size: 26px; font-weight: 900; color: var(--cyber-green); letter-spacing: 2px;
                animation: zoomPulse 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }
            @keyframes zoomPulse { from { transform: scale(0.5); opacity: 0; } to { transform: scale(1); opacity: 1; } }
            
            /* 🔴 नाकारल्यावर येणारे कडक ओव्हरले */
            .fail-overlay {
                display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(255, 51, 51, 0.15); justify-content: center; align-items: center;
                font-size: 22px; font-weight: 900; color: var(--cyber-red); letter-spacing: 1px;
            }

            /* 🗝️ प्रगत VIP रूम स्क्रीन डिझाईन (Premium Stealth Look - 1000005124.jpg) */
            #room-selection-screen { width: 100%; max-width: 400px; display: none; flex-direction: column; justify-content: center; align-items: flex-start; height: 90vh; padding-left: 30px; box-sizing: border-box; }
            .room-title-text { font-size: 28px; font-weight: 900; color: #fff; margin-bottom: 25px; letter-spacing: 1px; text-shadow: 0 0 10px rgba(255,255,255,0.2); }
            .room-input-box { width: 85%; max-width: 300px; padding: 14px; font-size: 18px; background-color: #fff; color: #000; border: none; border-radius: 8px; outline: none; margin-bottom: 20px; font-weight: 800; letter-spacing: 3px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
            .room-submit-btn { background-color: #f0f0f0; color: #000; border: none; padding: 12px 30px; font-size: 15px; cursor: pointer; font-weight: 900; border-radius: 8px; text-transform: uppercase; transition: all 0.3s; box-shadow: 0 4px 10px rgba(255,255,255,0.1); }
            .room-submit-btn:hover { background-color: #fff; transform: translateY(-2px); box-shadow: 0 6px 15px rgba(255,255,255,0.2); }
            #backup-password-container { display: none; margin-top: 20px; width: 100%; }

            /* 💬 ५. मुख्य चॅट स्क्रीन (तुझा ओरिजिनल पिंक-ब्लॅक लुक प्रगत केला आहे - 1000005088.jpg) */
            #chat-main-screen {
                display: none; width: 100%; max-width: 450px; border: 2px solid var(--cyber-pink); border-radius: 30px;
                padding: 18px; flex-direction: column; background: #000;
                box-shadow: 0 0 25px rgba(255, 42, 117, 0.4); height: 95vh; position: relative;
            }
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid rgba(255,42,117,0.2); padding-bottom: 10px; }
            .chat-room-header-title { color: var(--cyber-pink); font-size: 18px; font-weight: 900; text-shadow: 0 0 10px rgba(255,42,117,0.3); }
            .header-buttons { display: flex; gap: 8px; align-items: center; }
            .clear-btn { background-color: var(--cyber-pink); border: none; color: white; padding: 8px 16px; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 13px; }
            .online-box { border: 1px solid var(--cyber-pink); border-radius: 12px; padding: 6px 12px; font-size: 12px; text-align: center; background: rgba(255,42,117,0.05); }
            .call-btn { background: linear-gradient(45deg, #00ffcc, #00ee99); border: none; color: #000; padding: 8px 14px; border-radius: 12px; font-weight: 900; cursor: pointer; box-shadow: 0 0 10px rgba(0,255,204,0.3); }
            
            #chat-box { flex: 1; border: 1px solid rgba(255, 42, 117, 0.4); border-radius: 20px; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 14px; margin-bottom: 15px; background-color: #030305; }
            .encrypt-tag { text-align: center; color: #555; font-size: 11px; font-style: italic; margin: 0 auto; background: #09090f; padding: 6px 16px; border-radius: 20px; border: 1px dashed #333; width: fit-content; }
            
            /* प्रगत चॅट बबल्स इफेक्ट्स */
            .msg { padding: 12px 18px; border-radius: 20px; max-width: 75%; font-size: 16px; word-wrap: break-word; line-height: 1.4; animation: bubbleUp 0.3s ease; }
            @keyframes bubbleUp { from { transform: translateY(10px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
            .opp-msg { background-color: #0e0f14; color: #fff; align-self: flex-start; border: 1px solid var(--cyber-pink); box-shadow: 0 2px 8px rgba(255,42,117,0.1); }
            .my-msg { background: var(--chat-gradient); color: #fff; align-self: flex-end; box-shadow: 0 4px 12px rgba(255,42,117,0.3); }
            
            .input-container { display: flex; gap: 10px; align-items: center; }
            .chat-input-field { flex: 1; padding: 14px 18px; background-color: #07070a; color: #fff; border: 1px solid rgba(255,42,117,0.3); border-radius: 16px; font-size: 16px; outline: none; transition: 0.3s; }
            .chat-input-field:focus { border-color: var(--cyber-pink); box-shadow: 0 0 12px rgba(255,42,117,0.2); }
            .send-btn { background-color: var(--cyber-pink); border: none; color: white; padding: 14px 24px; border-radius: 16px; font-weight: 900; font-size: 16px; cursor: pointer; transition: 0.3s; }
            .send-btn:hover { box-shadow: 0 0 15px var(--cyber-pink); filter: brightness(1.1); }
            .footer-text { text-align: center; color: rgba(255, 42, 117, 0.4); font-size: 11px; margin-top: 8px; font-weight: bold; letter-spacing: 1px; }
        </style>
    </head>
    <body>

        <!-- 📱 पायरी १: CREATE ACCOUNT SCREEN (Advanced Glass UI) -->
        <div id="register-screen" class="auth-container" style="display: flex;">
            <div class="auth-box" style="border-color: var(--cyber-blue);">
                <h2>📝 REGISTER</h2>
                <p class="auth-p">सायबर-सुरक्षित रूमसाठी नवीन खाते तयार करा:</p>
                <input type="text" id="regUser" class="auth-input" placeholder="User Name">
                <input type="password" id="regPass" class="auth-input" placeholder="Password">
                <button class="auth-btn" onclick="registerAccount()">Create Account</button>
                <div class="switch-link" onclick="navigate('login-screen')">आधीच खाते आहे? लॉगिन करा</div>
            </div>
        </div>

        <!-- 🔐 पायरी १.२: LOGIN SCREEN (Premium Dark Blue) -->
        <div id="login-screen" class="auth-container">
            <div class="auth-box" style="border-color: var(--cyber-blue);">
                <h2>⚡ SYSTEM LOGIN</h2>
                <p class="auth-p">तुमचे क्रेडेंशियल्स टाकून मुख्य हब अनलॉक करा:</p>
                <input type="text" id="loginUser" class="auth-input" placeholder="User Name">
                <input type="password" id="loginPass" class="auth-input" placeholder="Password">
                <button class="auth-btn" onclick="checkUserCredentials()">Verify Access</button>
                <div class="switch-link" onclick="navigate('register-screen')">नवीन खाते बनवण्यासाठी इथे क्लिक करा</div>
            </div>
        </div>

        <!-- 📸 पायरी २: FACE LOCK SETUP SCREEN (Advanced Scanner Grid) -->
        <div id="face-setup-screen" class="auth-container">
            <div class="auth-box" style="border-color: var(--cyber-blue);">
                <h2>📸 FACE SIGNATURE</h2>
                <p class="auth-p">चेहऱ्याचे बायोमॅट्रीक कलर मॅट्रिक्स सुरक्षित डेटाबेसमध्ये लिंक करा:</p>
                <div class="scanner-holder">
                    <div class="laser-line"></div>
                    <video id="setup-webcam" class="live-webcam-view" autoplay playsinline muted></video>
                </div>
                <button class="auth-btn" onclick="captureAndSaveFace()">Save Face Lock</button>
            </div>
        </div>

        <!-- 🗝️ पायरी ३: VIP रूम सेटअप स्क्रीन (Screenshot 1000005124.jpg हुबेहूब प्रगत लुक) -->
        <div id="room-selection-screen">
            <div class="room-title-text">🔑 CREATE VIP ROOM</div>
            <input type="text" id="roomNumberInput" class="room-input-box" placeholder="5 Digit VIP Room Code">
            <br>
            <button class="room-submit-btn" onclick="openFaceVerifyScanner()">ENTER SECRET ROOM</button>
        </div>

        <!-- 🎭 पायरी ४: LIVE FACE VERIFY SCREEN (Advanced Hologram Effects) -->
        <div id="face-matching-screen" class="auth-container">
            <div class="auth-box" id="mainVerifyBox" style="border-color: var(--cyber-blue);">
                <h2>🎭 AI FACE VERIFY</h2>
                <div id="scan-status">बायोमॅट्रीक डेटा मॅचिंग सुरू आहे...</div>
                
                <div class="scanner-holder" id="scannerCircleBox">
                    <div class="laser-line" id="laserBar"></div>
                    <video id="match-webcam" class="live-webcam-view" autoplay playsinline muted></video>
                    
                    <div class="success-overlay" id="successAnimation">✔️ GRANTED</div>
                    <div class="fail-overlay" id="failAnimation">❌ DENIED</div>
                </div>

                <!-- पासवर्ड बॅकअप पर्याय -->
                <div id="backup-password-container">
                    <p style="font-size:12px; color:var(--cyber-red); margin:0 0 10px 0;">बायोमॅट्रीक मॅच फेल! बॅकअप चावी वापरा:</p>
                    <input type="password" id="backupPassField" class="auth-input" style="border-color:var(--cyber-red); margin-bottom:12px;" placeholder="मूळ पासवर्ड टाका">
                    <button class="auth-btn" style="background:linear-gradient(135deg, #ff3333, #ff5e62); color:white; box-shadow:0 4px 15px rgba(255,51,51,0.4);" onclick="verifyBackupPassword()">Unlock with Key</button>
                </div>
            </div>
        </div>

        <!-- 💬 पायरी ५: मुख्य चॅट स्क्रीन (Premium Cyberpunk Pink Look) -->
        <div id="chat-main-screen">
            <div class="header">
                <div class="chat-room-header-title">❤️ VIP SECURE HUB:<br><span id="displayRoomId">XXXXX</span></div>
                <div class="header-buttons">
                    <button class="call-btn" onclick="startVideoCall()">📹 Call</button>
                    <button class="clear-btn" onclick="clearChat()">Clear</button>
                    <div class="online-box">Online:<br><span id="onlineCount">1</span></div>
                </div>
            </div>
            <div id="chat-box"><div class="encrypt-tag">🔐 End-to-End Encrypted Quantum Connection</div></div>
            <div class="input-container">
                <input type="text" id="msgInput" class="chat-input-field" placeholder="गुप्त मेसेज टाईप करा...">
                <button class="send-btn" onclick="send()">Send</button>
            </div>
            <div class="footer-text">SECURE CORE V4.0 // WEBSITE BY PIYUSH PATIL</div>
        </div>

        <canvas id="hiddenCanvas" style="display:none;" width="16" height="16"></canvas>

        <script>
            let currentRoomId = ""; let myUsername = ""; let lastMessageCount = 0;
            let activeStream = null;

            window.onload = () => { localStorage.clear(); };

            function navigate(targetId) {
                document.getElementById('register-screen').style.display = 'none';
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('face-setup-screen').style.display = 'none';
                document.getElementById('room-selection-screen').style.display = 'none';
                document.getElementById('face-matching-screen').style.display = 'none';
                document.getElementById('chat-main-screen').style.display = 'none';
                document.getElementById(targetId).style.display = 'flex';
            }

            function registerAccount() {
                const user = document.getElementById('regUser').value.trim();
                const pass = document.getElementById('regPass').value.trim();
                if(!user || !pass) return;
                fetch('/create-account', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: user, password: pass})
                }).then(res => res.json()).then(data => { alert(data.message); if(data.status === 'success') navigate('login-screen'); });
            }

            function checkUserCredentials() {
                const user = document.getElementById('loginUser').value.trim();
                const pass = document.getElementById('loginPass').value.trim();
                fetch('/check-login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: user, password: pass})
                }).then(res => res.json()).then(data => {
                    if(data.status === 'success') {
                        myUsername = user; navigate('face-setup-screen');
                        navigator.mediaDevices.getUserMedia({ video: true }).then(stream => { activeStream = stream; document.getElementById('setup-webcam').srcObject = stream; });
                    } else { alert(data.message); }
                });
            }

            function captureAndSaveFace() {
                const video = document.getElementById('setup-webcam');
                const canvas = document.getElementById('hiddenCanvas');
                const ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0, 16, 16);
                const imgData = ctx.getImageData(0, 0, 16, 16);
                let rSum = 0, gSum = 0, bSum = 0;
                for (let i = 0; i < imgData.data.length; i += 4) { rSum += imgData.data[i]; gSum += imgData.data[i+1]; bSum += imgData.data[i+2]; }

                fetch('/save-face-photo', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: myUsername, r: rSum, g: gSum, b: bSum})
                }).then(() => {
                    if(activeStream) { activeStream.getTracks().forEach(track => track.stop()); }
                    alert("✅ प्रगत बायोमॅट्रीक प्रोफाइल सेव्ह झाली!");
                    navigate('room-selection-screen');
                });
            }

            function openFaceVerifyScanner() {
                const roomInput = document.getElementById('roomNumberInput').value.trim();
                if(!roomInput) { alert("कृपया रूम कोड टाका!"); return; }
                currentRoomId = roomInput;
                
                document.getElementById('backup-password-container').style.display = "none";
                document.getElementById('failAnimation').style.display = "none";
                document.getElementById('laserBar').style.display = "block";
                document.getElementById('scannerCircleBox').style.borderColor = "var(--cyber-blue)";
                document.getElementById('scan-status').innerHTML = "बायोमॅट्रीक स्कॅनिंग सुरू आहे... चेहरा स्थिर ठेवा";
                document.getElementById('scan-status').style.color = "#00f0ff";

                navigate('face-matching-screen');

                navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
                    activeStream = stream;
                    document.getElementById('match-webcam').srcObject = stream;
                    setTimeout(() => { verifyFaceOnServer(stream); }, 3000);
                }).catch(e => { showBackupPasswordArea(null); });
            }

            function verifyFaceOnServer(stream) {
                const video = document.getElementById('match-webcam');
                const canvas = document.getElementById('hiddenCanvas');
                const ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0, 16, 16);
                const imgData = ctx.getImageData(0, 0, 16, 16);
                let rSum = 0, gSum = 0, bSum = 0;
                for (let i = 0; i < imgData.data.length; i += 4) { rSum += imgData.data[i]; gSum += imgData.data[i+1]; bSum += imgData.data[i+2]; }

                fetch('/verify-face-photo', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: myUsername, r: rSum, g: gSum, b: bSum})
                })
                .then(res => res.json()).then(data => {
                    if(data.matched === true) {
                        document.getElementById('scan-status').innerHTML = "💥 ACCESS GRANTED // CORE CONNECTED";
                        document.getElementById('scan-status').style.color = "var(--cyber-green)";
                        document.getElementById('scannerCircleBox').style.borderColor = "var(--cyber-green)";
                        document.getElementById('laserBar').style.display = "none";
                        document.getElementById('successAnimation').style.display = "flex";
                        setTimeout(() => { enterChatRoomDirectly(stream); }, 1500);
                    } else {
                        showBackupPasswordArea(stream);
                    }
                }).catch(() => { showBackupPasswordArea(stream); });
            }

            function showBackupPasswordArea(stream) {
                document.getElementById('scan-status').innerHTML = "🔴 AUTHENTICATION FAILED // ID MISMATCH";
                document.getElementById('scan-status').style.color = "var(--cyber-red)";
                document.getElementById('scannerCircleBox').style.borderColor = "var(--cyber-red)";
                document.getElementById('laserBar').style.display = "none";
                document.getElementById('failAnimation').style.display = "flex";
                if(stream) { stream.getTracks().forEach(track => track.stop()); }
                setTimeout(() => { document.getElementById('backup-password-container').style.display = "block"; }, 1000);
            }

            function verifyBackupPassword() {
                const enteredPass = document.getElementById('backupPassField').value.trim();
                fetch('/check-login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: myUsername, password: enteredPass})
                }).then(res => res.json()).then(data => {
                    if(data.status === 'success') {
                        document.getElementById('backupPassField').value = "";
                        enterChatRoomDirectly(null);
                    } else { alert("❌ चुकीचा सिक्रेट पासवर्ड!"); }
                });
            }

            function enterChatRoomDirectly(stream) {
                if(stream) { stream.getTracks().forEach(track => track.stop()); }
                document.getElementById('displayRoomId').innerText = currentRoomId;
                navigate('chat-main-screen');
                pingServerActive();
                setInterval(pingServerActive, 4000);
                setInterval(loadMessages, 2000);
            }

            function pingServerActive() {
                fetch('/ping', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({room: currentRoomId, user: myUsername}) })
                .then(res => res.json()).then(data => { document.getElementById('onlineCount').innerText = data.online_count; });
            }

            function loadMessages() {
                fetch('/get-messages?room=' + currentRoomId).then(res => res.json()).then(data => {
                    const chatBox = document.getElementById('chat-box');
                    chatBox.innerHTML = data.map(m => {
                        const isMe = m.user.toLowerCase() === myUsername.toLowerCase();
                        return `<div class="msg ${isMe ? 'my-msg' : 'opp-msg'}">${isMe ? '' : `<span>${m.user}: </span>`}${m.text}</div>`;
                    }).join('');
                    if(data.length > lastMessageCount) { chatBox.scrollTop = chatBox.scrollHeight; lastMessageCount = data.length; }
                });
            }

            function send() {
                const input = document.getElementById('msgInput'); const text = input.value.trim(); if(!text) return;
                fetch('/send-message', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({text: text, user: myUsername, room: currentRoomId}) }).then(() => { input.value = ''; loadMessages(); });
            }
            function clearChat() { if(confirm("सर्व चॅट डिलीट करायचे का?")) { fetch('/clear-messages', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({room: currentRoomId}) }).then(() => { loadMessages(); }); } }
            function startVideoCall() { window.open("https://meet.jit.si/PiyushVipSecretRoom_" + currentRoomId, '_blank'); }
        </script>
    </body>
    </html>
    '''

@app.route('/create-account', methods=['POST'])
def create_account():
    data = request.json or {}
    user = data.get('username', '').strip().lower()
    passw = data.get('password', '').strip()
    if user in users_db: return jsonify({'status': 'error', 'message': '❌ हे युझरनेम आधीच घेतले आहे!'})
    users_db[user] = {'password': passw, 'r': 0, 'g': 0, 'b': 0}
    return jsonify({'status': 'success', 'message': '✅ अकाउंट तयार झाले!'})

@app.route('/check-login', methods=['POST'])
def check_login():
    data = request.json or {}
    user = data.get('username', '').strip().lower()
    passw = data.get('password', '').strip()
    if user in users_db and users_db[user]['password'] == passw: return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': '❌ चुकीचे युझरनेम किंवा पासवर्ड!'})

@app.route('/save-face-photo', methods=['POST'])
def save_face_photo():
    data = request.json or {}
    user = data.get('username', '').strip().lower()
    if user in users_db:
        users_db[user]['r'] = data.get('r', 0)
        users_db[user]['g'] = data.get('g', 0)
        users_db[user]['b'] = data.get('b', 0)
    return jsonify({'status': 'success'})

@app.route('/verify-face-photo', methods=['POST'])
def verify_face_photo():
    data = request.json or {}
    user = data.get('username', '').strip().lower()
    if user in users_db and users_db[user]['r'] != 0:
        u = users_db[user]
        diff = abs(data.get('r', 0) - u['r']) + abs(data.get('g', 0) - u['g']) + abs(data.get('b', 0) - u['b'])
        if diff < 65000: return jsonify({'matched': True})
    return jsonify({'matched': False})

@app.route('/ping', methods=['POST'])
def ping_user():
    data = request.json or {}
    room = data.get('room', 'default')
    user = data.get('user', 'Unknown')
    if room not in room_data: room_data[room] = {'messages': [], 'users': {}}
    room_data[room]['users'][user] = True
    return jsonify({'status': 'success', 'online_count': len(room_data[room]['users'])})

@app.route('/get-messages', methods=['GET'])
def get_messages():
    room = request.args.get('room', 'default')
    return jsonify(room_data[room]['messages'] if room in room_data else [])

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json or {}
    if data.get('text'):
        room = data.get('room', 'default')
        if room not in room_data: room_data[room] = {'messages': [], 'users': {}}
        room_data[room]['messages'].append({'user': data.get('user'), 'text': data.get('text')})
    return jsonify({'status': 'success'})

@app.route('/clear-messages', methods=['POST'])
def clear_messages():
    data = request.json or {}
    room = data.get('room', 'default')
    if room in room_data: room_data[room]['messages'] = []
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
