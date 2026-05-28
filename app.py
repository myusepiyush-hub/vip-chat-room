from flask import Flask, render_template, request, jsonify
import urllib.request
import json
import re

app = Flask(__name__)

# 🌐 इंटरनेटवरून खरोखरची आणि अचूक माहिती शोधणारे गुप्त इंजिन
def fetch_live_search(query):
    try:
        # विकिपीडियाच्या लाईव्ह डेटाबेसला सुरक्षित कनेक्ट करणे
        url = f"https://mr.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=1&explaintext=1&titles={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=5)
        data = json.loads(response.read().decode('utf-8'))
        
        pages = data.get('query', {}).get('pages', {})
        for page_id in pages:
            extract = pages[page_id].get('extract', '')
            if extract:
                return extract[:500] # पहिल्या ५०० अक्षरांची कडक अचूक माहिती देणे
        
        # जर मराठीत नाही सापडली तर इंग्लिश डेटाबेस चेक करणे
        url_en = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=1&explaintext=1&titles={urllib.parse.quote(query)}"
        req_en = urllib.request.Request(url_en, headers={'User-Agent': 'Mozilla/5.0'})
        response_en = urllib.request.urlopen(req_en, timeout=5)
        data_en = json.loads(response_en.read().decode('utf-8'))
        
        pages_en = data_en.get('query', {}).get('pages', {})
        for page_id in pages_en:
            extract_en = pages_en[page_id].get('extract', '')
            if extract_en:
                return extract_en[:500]
                
        return f"बॉस, '{query}' बद्दल माहिती इंटरनेटवर शोधली, पण अचूक संदर्भ सापडला नाही. कृपया दुसरा शब्द शोधून बघा!"
    except Exception as e:
        return f"इंटरनेट कनेक्शन स्लो आहे बॉस! तुम्ही शोधलेला शब्द: '{query}' पुन्हा एकदा सर्च करून बघा."

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VIP Cyber Search - Live Engine</title>
        <style>
            :root {
                --insta-gradient: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
                --cyber-blue: #00f0ff;
                --cyber-pink: #ff2a75;
                --cyber-green: #00ff66;
                --glass-card: rgba(255, 255, 255, 0.04);
            }

            body {
                background: radial-gradient(circle at center, #0c0f26 0%, #020308 100%);
                color: #fff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0; padding: 15px; display: flex; flex-direction: column;
                align-items: center; justify-content: center; min-height: 100vh;
                box-sizing: border-box; overflow-x: hidden;
            }

            /* ✨ प्रीमियम फिरता निऑन बॅकग्राउंड इफेक्ट */
            body::before {
                content: ''; position: absolute; width: 200%; height: 200%;
                background-image: linear-gradient(rgba(255, 42, 117, 0.02) 1px, transparent 1px),
                                  linear-gradient(90deg, rgba(0, 240, 255, 0.02) 1px, transparent 1px);
                background-size: 400% 400%; top: -50%; left: -50%; z-index: 0;
                pointer-events: none;
            }

            .search-container {
                width: 100%; max-width: 480px; text-align: center; z-index: 10;
                animation: fadeIn 0.6s ease;
            }

            @keyframes fadeIn { from { opacity: 0; transform: translateY(-2px); } to { opacity: 1; transform: translateY(0); } }

            h1 {
                font-family: 'Grand Hotel', 'Brush Script MT', cursive, sans-serif;
                font-size: 52px; margin: 0 0 10px 0; font-weight: 500;
                background: linear-gradient(45deg, #ff2a75, #ff00f0, #00f0ff);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                text-shadow: 0 0 30px rgba(255, 42, 117, 0.3);
            }

            .tagline { font-size: 13px; color: rgba(255, 255, 255, 0.5); margin-bottom: 35px; letter-spacing: 2px; text-transform: uppercase; }

            /* 🔍 प्रगत हुबेहूब कोरा काळा सायबर सर्च बार */
            .search-box {
                position: relative; width: 100%; display: flex; align-items: center;
                background: rgba(0, 0, 0, 0.6); border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px; padding: 4px; box-sizing: border-box;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                margin-bottom: 25px;
            }
            .search-box:focus-within {
                border-color: var(--cyber-pink);
                box-shadow: 0 0 25px rgba(255, 42, 117, 0.4);
                transform: scale(1.02);
            }

            .search-input {
                flex: 1; border: none; background: transparent; color: #fff;
                padding: 16px 20px; font-size: 16px; outline: none; font-weight: 500;
            }

            .search-btn {
                background: var(--insta-gradient); border: none; color: white;
                padding: 14px 28px; font-size: 15px; font-weight: 700; border-radius: 16px;
                cursor: pointer; transition: 0.3s; margin-right: 4px;
            }
            .search-btn:active { transform: scale(0.96); }

            /* 🗂️ रिझल्ट कार्ड डिझाईन */
            .result-card {
                display: none; width: 100%; background: var(--glass-card);
                border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 26px;
                padding: 25px; text-align: left; box-sizing: border-box;
                backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.4);
                animation: slideUp 0.4s ease-out;
            }
            @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

            .result-header { color: var(--cyber-blue); font-size: 14px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px; display: flex; justify-content: space-between; }
            .result-text { font-size: 16px; line-height: 1.6; color: rgba(255, 255, 255, 0.9); margin-bottom: 20px; font-weight: 400; }

            /* 🎨 व्हायरल व्हॉट्सॲप स्टेटस क्रिएटर कार्ड */
            .status-card-preview {
                display: none; width: 100%; max-width: 340px; height: 500px;
                background: linear-gradient(135deg, #120c1f 0%, #05020a 100%);
                border: 3px solid var(--cyber-pink); border-radius: 24px; padding: 30px 20px;
                box-sizing: border-box; position: relative; margin-top: 25px;
                box-shadow: 0 15px 35px rgba(255,42,117,0.3);
                animation: popCard 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }
            @keyframes popCard { from { transform: scale(0.9); opacity:0; } to { transform: scale(1); opacity:1; } }

            .status-title { font-size: 26px; font-weight: 900; color: #fff; margin-bottom: 15px; border-left: 4px solid var(--cyber-blue); padding-left: 10px; }
            .status-desc { font-size: 14px; line-height: 1.5; color: rgba(255,255,255,0.85); font-style: italic; }
            .status-footer { position: absolute; bottom: 20px; left: 0; width: 100%; text-align: center; color: var(--cyber-pink); font-size: 11px; font-weight: 800; letter-spacing: 2px; }

            .action-btn {
                background: transparent; border: 1px solid rgba(255,255,255,0.2); color: #fff;
                padding: 10px 20px; font-size: 14px; font-weight: 600; border-radius: 12px;
                cursor: pointer; transition: 0.3s; margin-right: 10px;
            }
            .action-btn:hover { background: #fff; color: #000; border-color: #fff; }

            .footer-brand { margin-top: 40px; font-size: 11px; color: rgba(255,255,255,0.2); font-weight: 800; letter-spacing: 1px; }
        </style>
    </head>
    <body>

        <div class="search-container">
            <h1>VIP Search</h1>
            <div class="tagline">Quantum Live Search Engine</div>

            <!-- 🔍 मुख्य सायबर सर्च बार -->
            <div class="search-box">
                <input type="text" id="queryInput" class="search-input" placeholder="काहीपण सर्च करा बॉस...">
                <button class="search-btn" onclick="performLiveSearch()">SEARCH</button>
            </div>

            <!-- 🗂️ माहिती रिझल्ट बॉक्स -->
            <div class="result-card" id="resultCard">
                <div class="result-header">
                    <span>📡 LIVE CORE DATA</span>
                    <span style="color:var(--cyber-green);" id="statusIndicator">● ONLINE</span>
                </div>
                <div class="result-text" id="resultText">माहिती लोड होत आहे...</div>
                
                <button class="action-btn" style="border-color:var(--cyber-pink); color:var(--cyber-pink);" onclick="generateViralStatus()">✨ Create Status Card</button>
                <button class="action-btn" onclick="clearSearch()">Clear</button>
            </div>

            <!-- 🎨 व्हायरल सोशल मीडिया स्टेटस कार्ड प्रिव्ह्यू -->
            <div class="status-card-preview" id="statusCard">
                <div id="statusCardTitle" class="status-title">TRENDING</div>
                <div id="statusCardDesc" class="status-desc">माहिती कार्ड...</div>
                <div class="status-footer">🎯 SEARCHED VIA VIP ENGINE // BY PIYUSH</div>
            </div>

            <div class="footer-brand">POWERED BY VIP SEARCH NETWORK v1.0</div>
        </div>

        <script>
            // 🔊 [मॅजिकल बोलणारे एआई इंजिन]
            function speakVipVoice(textMessage) {
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                    let utterance = new SpeechSynthesisUtterance(textMessage);
                    utterance.lang = 'mr-IN'; utterance.rate = 1.0; utterance.pitch = 1.1;
                    window.speechSynthesis.speak(utterance);
                }
            }

            // 🔍 खरोखरचा लाईव्ह सर्च मारणे
            function performLiveSearch() {
                const query = document.getElementById('queryInput').value.trim();
                if(!query) { alert("कृपया शोधण्यासाठी काहीतरी टाईप करा!"); return; }

                document.getElementById('resultCard').style.display = 'none';
                document.getElementById('statusCard').style.display = 'none';

                fetch('/search-engine?q=' + encodeURIComponent(query))
                .then(res => res.json())
                .then(data => {
                    document.getElementById('resultText').innerText = data.result;
                    document.getElementById('resultCard').style.display = 'block';
                    
                    // 🔊 अचूक रिझल्ट येताच एआई कडक आवाजात बोलेल:
                    speakVipVoice("बॉस, तुम्ही शोधलेली कडक माहिती मी इंटरनेटवरून शोधून आणली आहे, नीट वाचून घ्या!");
                });
            }

            // 🎨 १-क्लिकमध्ये व्हायरल स्टेटस निऑन कार्ड बनवणे
            function generateViralStatus() {
                const query = document.getElementById('queryInput').value.trim();
                const text = document.getElementById('resultText').innerText;
                
                document.getElementById('statusCardTitle').innerText = query.toUpperCase();
                document.getElementById('statusCardDesc').innerText = text.substring(0, 280) + "...";
                
                document.getElementById('statusCard').style.display = 'block';
                window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
                
                speakVipVoice("तुमचा व्हायरल स्टेटस कार्ड रेडी आहे बॉस!");
            }

            function clearSearch() {
                document.getElementById('queryInput').value = "";
                document.getElementById('resultCard').style.display = 'none';
                document.getElementById('statusCard').style.display = 'none';
            }

            // एंटर बटन दाबल्यावर पण सर्च होणे
            document.getElementById("queryInput").addEventListener("keyup", function(e) {
                if(e.key === "Enter") { performLiveSearch(); }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/search-engine', methods=['GET'])
def search_engine():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'result': 'कृपया वैध शब्द टाईप करा!'})
    
    # थेट लाईव्ह विकिपीडिया आणि गुगल डेटा फेच सिस्टीम कॉल करणे
    live_info = fetch_live_search(query)
    return jsonify({'result': live_info})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
