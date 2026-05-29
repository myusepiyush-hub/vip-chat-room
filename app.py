from flask import Flask, render_template, request, jsonify
import urllib.request
import json
import re
from datetime import datetime

app = Flask(__name__)

# 🌐 प्रगत कोर इंजिन - फायनान्स मॅट्रिक्स, एआय डिक्शनरी आणि फॉर्च्युनर कोडिंग नेटवर्क
def fetch_complete_google_matrix(query):
    query_clean = query.strip().lower()
    
    # 👑 पीयुष पाटील स्पेशल किंग ओनरशिप ब्रँडिंग लॉक
    if any(x in query_clean for x in ["banavla", "who made you", "owner", "creator", "piyush", "पीयुष"]):
        return {
            "type": "branding",
            "company": "👑 PIYUSH PATIL COMMAND CORE",
            "ai_answer": "नादच खुळा बॉस! या अल्ट्रा-व्हायरल VIP सर्च इंजिन नेटवर्कला जळगावच्या 'पीयुष पाटील' यांनी स्वतः माझं कोडिंग लिहून बनवलं आहे. ही पीयुष पाटील यांची स्वतःची कडक सायबर सिस्टीम आहे!",
            "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
            "links": [{"title": "👑 System Founder: PIYUSH PATIL (Official Command)", "url": "https://github.com", "snippet": "Official database locked securely under Piyush Patil encryption networks."}]
        }

    # 🕒 लाईव्ह घड्याळ सिग्नल
    if any(x in query_clean for x in ["time", "tame", "वेळ", "tarikh", "date", "तारीख"]):
        return {"type": "time", "ai_answer": "सध्याचा चालू लाईव्ह रिअल-टाइम खाली घड्याळ विजेटमध्ये सतत पळत आहे चीफ!", "links": []}

    # 📈 [परफेक्ट फिक्स - Screenshot 1000005732.jpg]: मल्टि-कंपनी स्टॉक फायनान्स इंजिन
    if any(x in query_clean for x in ["irfc", "share", "shere", "stock", "tata", "reliance", "market", "zomato", "sbi"]):
        company_name = "Indian Railway Finance Corp Ltd"
        ticker = "NSE: IRFC"
        price = "99.38"
        change = "+0.19 (0.19%)"
        open_p, high_p, low_p, mcap = "99.24", "100.14", "98.82", "1.30LCr"

        if "tata" in query_clean:
            company_name, ticker, price, change, open_p, high_p, low_p, mcap = "Tata Motors Limited", "NSE: TATAMOTORS", "945.20", "+11.45 (1.23%)", "932.00", "951.00", "930.10", "3.15LCr"
        elif "reliance" in query_clean:
            company_name, ticker, price, change, open_p, high_p, low_p, mcap = "Reliance Industries Ltd", "NSE: RELIANCE", "2,450.10", "+34.20 (1.41%)", "2,420.00", "2,465.00", "2,415.00", "16.50LCr"
        elif "zomato" in query_clean:
            company_name, ticker, price, change, open_p, high_p, low_p, mcap = "Zomato Limited", "NSE: ZOMATO", "198.40", "+4.15 (2.14%)", "194.00", "201.50", "193.10", "1.75LCr"

        return {
            "type": "stock_finance",
            "company": company_name,
            "ticker": ticker,
            "price": price,
            "change": change,
            "open": open_p, "high": high_p, "low": low_p, "mcap": mcap,
            "ai_answer": f"📉 शेअर मार्केट ट्रॅकर: सध्या {company_name} ({ticker}) चा आलेख अतिशय मजबूत चालला आहे. पीयुष फायनान्स सर्व्हरनुसार हा स्टॉक सुरक्षित झोनमध्ये ट्रेड करत आहे.",
            "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=800&q=80",
            "links": [
                {"title": f"{company_name} Live Charts - Google Finance", "url": "https://www.google.com/finance", "snippet": f"Get real-time stock quotes, dynamic historical charts and investment metrics for {company_name}."},
                {"title": f"{company_name} Technical Analysis - Moneycontrol", "url": "https://www.moneycontrol.com", "snippet": "Live volume metrics, moving averages and market capitalization stats."}
            ]
        }

    # ⚡ [प्रगत एआई डिक्शनरी उत्तर]: गुगलच्या आधी थेट अचूक उत्तर लिहिणे
    ai_generated_response = f"Chief, I have completed a global matrix scan for '{query.capitalize()}'. Safe connections are established."
    if "king" in query_clean or "raja" in query_clean:
        ai_generated_response = "👑 नादच खुळा! इतिहास साक्ष आहे की सिंहासनावर कोणीही बसो, डिजिटल विश्वाचा खरा किंग जळगावचा 'पीयुष पाटील' हाच आहे! विषय एंड!"
    elif "jalgaon" in query_clean:
        ai_generated_response = "📍 जळगाव (गोल्ड सिटी): महाराष्ट्रातील सर्वात कडक जिल्हा, जो केळीच्या बागा आणि शुद्ध सोन्यासाठी प्रसिद्ध आहे! आणि 'पीयुष पाटील' देखील याच कडक मातीचे सुपुत्र आहेत!"

    # खऱ्या ओपेन वेब नेटवर्कवरून माहिती स्क्रॅप करणे
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=opensearch&format=json&limit=4&search={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=5)
        data = json.loads(response.read().decode('utf-8'))
        
        titles = data[1]
        snippets = data[2]
        links = data[3]
        
        results = []
        for i in range(len(titles)):
            results.append({
                "title": f"{titles[i]} - Verified System Resource",
                "url": links[i],
                "snippet": snippets[i] if snippets[i] else f"Explore verified database parameters, current updates, and cloud vectors for {titles[i]} safely."
            })
        
        # 📸 [इमेज फिक्स]: थेट अनस्प्लॅशवरून त्या विशिष्ट की-वर्डचाच ब्रँड न्यू फोटो सिंक करणे
        img_url = f"https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80"
        if "bmw" in query_clean: img_url = "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=800&q=80"
        elif "car" in query_clean: img_url = "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=800&q=80"
        elif "gaming" in query_clean: img_url = "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=800&q=80"

        if results:
            return {"type": "normal", "ai_answer": ai_generated_response, "image": img_url, "links": results}
    except Exception:
        pass

    return {
        "type": "normal", "ai_answer": ai_generated_response, "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
        "links": [{"title": f"{query.capitalize()} - Global System Search", "url": "https://www.google.com", "snippet": "Continuous data streams and search parameters loaded from secure cloud networks."}]
    }

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Google Premium</title>
        <style>
            :root {
                --google-bg: #0d0e12; --google-card: #161722; --google-text: #e8eaed; --google-link: #66a0ff; --google-sub: #a1a5b5;
                --google-green: #81c995; --google-neon: #ff2a75;
            }

            body {
                background-color: var(--google-bg); color: var(--google-text); font-family: Roboto, Helvetica, sans-serif;
                margin: 0; padding: 12px; display: flex; flex-direction: column; align-items: center; min-height: 100vh; box-sizing: border-box;
            }

            .top-header-bar { display: flex; justify-content: space-between; width: 100%; max-width: 480px; align-items: center; margin-bottom: 5px; font-size: 11px; font-weight: bold; color: var(--google-green); }

            .search-container { width: 100%; max-width: 480px; text-align: center; position: relative; }

            .google-logo-text { font-size: 42px; font-weight: 900; margin-bottom: 18px; letter-spacing: -1px; user-select: none; text-shadow: 0 0 15px rgba(102,160,255,0.2); }
            .g-blue { color: #4285F4; } .g-red { color: #EA4335; } .g-yellow { color: #FBBC05; } .g-green { color: #34A853; }

            .search-wrapper { position: relative; width: 100%; margin-bottom: 12px; }

            /* 🔍 प्रगत आरजीबी निऑन ग्लो सर्च बॉक्स */
            .search-box { 
                display: flex; align-items: center; background: var(--google-card); border: 2px solid rgba(255,255,255,0.04); border-radius: 28px; padding: 5px 16px; box-sizing: border-box;
                box-shadow: 0 8px 24px rgba(0,0,0,0.5);
            }
            .search-box:focus-within { border-color: var(--google-neon); box-shadow: 0 0 15px rgba(255,42,117,0.3); }
            .search-input { flex: 1; border: none; background: transparent; color: var(--google-text); padding: 10px; font-size: 16px; outline: none; }
            .voice-btn { background: none; border: none; font-size: 18px; cursor: pointer; outline: none; }

            /* 🎰 लकी फॉर्च्युनर रिवॉर्ड पॅनेल */
            .lucky-wheel-panel { background: linear-gradient(135deg, #161722 0%, #202232 100%); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 12px 16px; margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between; }
            .wheel-title { font-size: 14px; font-weight: bold; color: #fff; text-align: left; }
            .spin-btn { background: linear-gradient(45deg, #ff2a75, #ff00f0); border: none; color: #fff; font-weight: bold; padding: 8px 16px; font-size: 12px; border-radius: 20px; cursor: pointer; box-shadow: 0 4px 10px rgba(255,42,117,0.3); }

            .neon-reward-popup { display: none; background: rgba(0,0,0,0.95); border: 2px solid var(--google-neon); border-radius: 20px; padding: 20px; text-align: center; position: absolute; top: 120px; left: 5%; width: 90%; z-index: 999; box-shadow: 0 0 30px var(--google-neon); }

            /* 🎮 [माय सीक्रेट एआई आयडिया]: १००% वर्किंग इन-बिल्ट स्नेक गेम विजेट बॉक्स */
            .game-panel-box { background: #161722; border-radius: 16px; padding: 15px; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.05); }
            .game-canvas { background: #000; border: 2px solid #333; display: block; margin: 10px auto; border-radius: 8px; }
            .game-control-btn { background: #333; border: none; color: #fff; padding: 6px 12px; font-size: 12px; border-radius: 4px; cursor: pointer; margin: 2px; }

            /* 📊 १००% वर्किंग ऑल-ऑप्शन्स नेव्हिगेशन बार */
            .google-options-bar { display: flex; gap: 16px; overflow-x: auto; padding: 10px 4px; margin-bottom: 15px; width: 100%; font-size: 14px; color: var(--google-sub); border-bottom: 1px solid rgba(255,255,255,0.05); }
            .opt-item { padding-bottom: 6px; white-space: nowrap; cursor: pointer; user-select: none; color: var(--google-sub); }
            .opt-item.active { color: #8ab4f8; border-bottom: 3px solid #8ab4f8; font-weight: bold; }

            .location-bar { display: flex; align-items: center; gap: 8px; color: var(--google-sub); font-size: 13px; text-align: left; width: 100%; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 15px; }

            .result-card { display: none; width: 100%; text-align: left; box-sizing: border-box; }

            /* ⚡ एआई इन्स्टंट उत्तर विजेट */
            .piyush-ai-box { background: rgba(66, 133, 244, 0.08); border-radius: 16px; padding: 16px; margin-bottom: 20px; border-left: 5px solid #4285f4; }
            .ai-badge { font-size: 11px; font-weight: 900; background: #4285f4; color: #fff; padding: 3px 8px; border-radius: 10px; margin-bottom: 8px; display: inline-block; }

            /* 📈 [Screenshot 1000005732.jpg फिक्स]: हुबेहूब गुगल स्टॉक मार्केट चार्ट युआय */
            .google-stock-card { display: none; background: #18191e; border: 1px solid #282a36; border-radius: 16px; padding: 18px; margin-bottom: 22px; }
            .stock-comp-name { font-size: 21px; font-weight: bold; color: #fff; }
            .stock-ticker { font-size: 13px; color: var(--google-sub); margin-bottom: 8px; }
            .stock-price-row { display: flex; align-items: baseline; gap: 8px; margin-bottom: 15px; }
            .stock-current-price { font-size: 38px; font-weight: bold; color: #fff; font-family: sans-serif; }
            .stock-green-status { font-size: 16px; color: var(--google-green); font-weight: bold; }
            .stock-graph-box { width: 100%; height: 110px; border-bottom: 1px dashed #444; position: relative; margin-bottom: 15px; }
            .stock-data-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; font-size: 13px; color: var(--google-sub); }
            .grid-label-row { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,0.02); }

            .google-news-container { display: none; width: 100%; margin-bottom: 20px; }
            .news-card { background: var(--google-card); border-radius: 12px; padding: 14px; margin-bottom: 10px; border-left: 3px solid var(--google-green); }
            .news-title { font-size: 16px; font-weight: bold; color: #fff; }

            .google-images-grid { display: none; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 25px; }
            .grid-img { width: 100%; height: 130px; border-radius: 8px; object-fit: cover; }

            .live-image-frame { display: none; width: 100%; height: 210px; border-radius: 12px; margin-bottom: 22px; object-fit: cover; }

            .web-link-block { margin-bottom: 22px; }
            .web-title { font-size: 19px; color: var(--google-link); text-decoration: none; font-weight: bold; display: inline-block; margin-bottom: 4px; }
            .web-snippet { font-size: 14px; line-height: 1.5; color: var(--google-sub); }

            .live-clock-card { display: none; background: var(--google-card); border-radius: 16px; padding: 20px; margin-bottom: 22px; text-align: center; }
            .clock-time { font-size: 44px; font-weight: bold; color: var(--google-link); font-family: monospace; }

            .action-btn { background: var(--google-card); border: 1px solid #444; color: var(--google-text); padding: 10px 18px; font-size: 13px; border-radius: 20px; cursor: pointer; }
            .footer-brand { margin-top: 40px; font-size: 11px; color: var(--google-sub); text-align: center; font-weight: bold; }
        </style>
    </head>
    <body>

        <div class="top-header-bar">
            <div>⚡ PIYUSH PATIL MASTER SERVER v10.0</div>
            <div>STATUS: SECURE LIVE</div>
        </div>

        <div class="search-container">
            <div class="google-logo-text">
                <span class="g-blue">V</span><span class="g-red">I</span><span class="g-yellow">P</span>
                <span class="g-blue">G</span><span class="g-red">o</span><span class="g-yellow">o</span><span class="g-blue">g</span><span class="g-green">l</span><span class="g-red">e</span>
            </div>

            <div class="search-wrapper">
                <div class="search-box">
                    <input type="text" id="queryInput" class="search-input" placeholder="Google वर सर्च करा चीफ...">
                    <button class="voice-btn" onclick="triggerVoiceSearch()">🎙️</button>
                </div>
            </div>

            <!-- 🎰 लकी फॉर्च्युनर रिवॉर्ड पॅनेल -->
            <div class="lucky-wheel-panel" id="luckyWheelBlock">
                <div class="wheel-title">🎁 Daily Piyush Patil Rewards Active<br><span style="font-size:11px; font-weight:normal; color:var(--google-sub);">Claim your VIP matrix coins now.</span></div>
                <button class="spin-btn" onclick="spinLuckyWheelNow()">SPIN</button>
            </div>

            <!-- 🎮 १००% वर्किंग इन-बिल्ट स्नेक गेम पॅनेल (होम स्क्रीनसाठी) -->
            <div class="game-panel-box" id="homepageGameBlock">
                <div style="font-size:13px; font-weight:bold; color:#fff; text-align:left;">🎮 Piyush Matrix Snake Game Timepass</div>
                <canvas id="snakeGameCanvas" class="game-canvas" width="280" height="140"></canvas>
                <div style="text-align:center;">
                    <button class="game-control-btn" onclick="changeSnakeDir('up')">🔼 UP</button><br>
                    <button class="game-control-btn" onclick="changeSnakeDir('left')">◀️ LEFT</button>
                    <button class="game-control-btn" onclick="changeSnakeDir('right')">▶️ RIGHT</button><br>
                    <button class="game-control-btn" onclick="changeSnakeDir('down')">🔽 DOWN</button>
                </div>
            </div>

            <div class="neon-reward-popup" id="rewardPopupBox">
                <h2 style="color:#fff; margin-top:0;">🎉 BIG WIN CHIEF! 🎉</h2>
                <p style="color:var(--google-sub);">You have claimed <b style="color:var(--google-green);">500 VIP Coins</b> securely!</p>
                <button class="action-btn" onclick="closeRewardPopup()">THANKS!</button>
            </div>

            <!-- 📊 १००% वर्किंग ऑल-ऑप्शन्स नेव्हिगेशन बार -->
            <div class="google-options-bar">
                <div class="opt-item" id="tabAI" onclick="switchGoogleTab('ai')">AI Mode</div>
                <div class="opt-item active" id="tabAll" onclick="switchGoogleTab('all')">All</div>
                <div class="opt-item" id="tabFinance" onclick="switchGoogleTab('finance')">Finance</div>
                <div class="opt-item" id="tabNews" onclick="switchGoogleTab('news')">News</div>
                <div class="opt-item" id="tabImages" onclick="switchGoogleTab('images')">Images</div>
            </div>

            <div class="location-bar">
                <span>📍</span>
                <div><span>Jalgaon, Maharashtra 425001 · Dynamic IP Synchronized</span></div>
            </div>

            <div class="result-card" id="resultCard">
                
                <div class="piyush-ai-box" id="aiInstantBox">
                    <div class="ai-badge">🤖 PIYUSH TURBO INSTANT ANSWER</div>
                    <div class="ai-text-content" id="lblAiInstantMsg"></div>
                </div>

                <!-- 📈 [Screenshot 1000005732.jpg फिक्स]: अधिकृत शेअर मार्केट लाइव्ह ग्राफ विजेट -->
                <div class="google-stock-card" id="stockCardBlock">
                    <div class="stock-comp-name" id="lblStockCompany">Indian Railway Finance Corp Ltd</div>
                    <div class="stock-ticker" id="lblStockTicker">NSE: IRFC</div>
                    <div class="stock-price-row">
                        <div class="stock-current-price" id="lblStockPrice">99.38</div>
                        <div style="font-size:13px; color:var(--google-sub); margin-left:3px; margin-right:5px;">INR</div>
                        <div class="stock-green-status" id="lblStockChange">+0.19 (0.19%) ↑ today</div>
                    </div>
                    <div class="stock-graph-box">
                        <svg style="width:100%; height:100%; position:absolute; top:0; left:0;">
                            <path d="M0,85 Q40,15 80,65 T160,35 T240,75 T320,20 T400,8" fill="none" stroke="#81c995" stroke-width="3"/>
                            <circle cx="400" cy="8" r="5" fill="#81c995"/>
                        </svg>
                    </div>
                    <div class="stock-data-grid">
                        <div class="grid-label-row"><span>Open</span><b style="color:#fff;" id="lblStockOpen">99.24</b></div>
                        <div class="grid-label-row"><span>Mkt cap</span><b style="color:#fff;" id="lblStockMcap">1.30LCr</b></div>
                        <div class="grid-label-row"><span>High</span><b style="color:#fff;" id="lblStockHigh">100.14</b></div>
                        <div class="grid-label-row"><span>Low</span><b style="color:#fff;" id="lblStockLow">98.82</b></div>
                    </div>
                </div>

                <div class="google-news-container" id="newsGridBlock"></div>
                <div class="google-images-grid" id="imagesGridBlock"></div>
                <div class="live-clock-card" id="liveClockBlock"><div class="clock-time" id="lblClockTime">00:00:00 AM</div></div>
                <img id="liveImage" class="live-image-frame" src="" alt="Live Image">
                
                <div id="webLinksBlock"><div id="linksContainer"></div></div>
                
                <br>
                <button class="action-btn" onclick="clearSearch()">Clear x</button>
            </div>

            <div class="footer-brand">OWNED AND DEPLOYED BY PIYUSH PATIL © 2026</div>
        </div>

        <script>
            let clockInterval = null;
            let cacheStockData = null; let cacheImage = "";
            
            // 🎮 स्नेक गेम व्हेरिएबल्स
            let canvas = document.getElementById("snakeGameCanvas");
            let ctx = canvas.getContext("2d");
            let snake = [{x: 10, y: 10}]; let food = {x: 5, y: 5};
            let dx = 1; let dy = 0;

            function speakVipVoice(textMessage) {
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                    let utterance = new SpeechSynthesisUtterance(textMessage);
                    utterance.lang = 'mr-IN'; window.speechSynthesis.speak(utterance);
                }
            }

            function spinLuckyWheelNow() { document.getElementById('rewardPopupBox').style.display = 'block'; speakVipVoice("कॉइन्स क्रेडिट झाले आहेत बॉस!"); }
            function closeRewardPopup() { document.getElementById('rewardPopupBox').style.display = 'none'; }

            function triggerVoiceSearch() {
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    const recognition = new SpeechRecognition(); recognition.lang = 'mr-IN';
                    speakVipVoice("हा बोला चीफ..."); recognition.start();
                    recognition.onresult = function(e) { document.getElementById('queryInput').value = e.results[0][0].transcript; performLiveSearch(); };
                }
            }

            function switchGoogleTab(tabName) {
                const items = document.getElementsByClassName('opt-item');
                for(let item of items) { item.classList.remove('active'); }
                
                document.getElementById('aiInstantBox').style.display = 'none';
                document.getElementById('stockCardBlock').style.display = 'none';
                document.getElementById('newsGridBlock').style.display = 'none';
                document.getElementById('imagesGridBlock').style.display = 'none';
                document.getElementById('liveImage').style.display = 'none';
                document.getElementById('webLinksBlock').style.display = 'none';

                if(tabName === 'all') {
                    document.getElementById('tabAll').classList.add('active');
                    document.getElementById('aiInstantBox').style.display = 'block';
                    if(cacheStockData) { document.getElementById('stockCardBlock').style.display = 'block'; }
                    else if(cacheImage) { document.getElementById('liveImage').style.display = 'block'; }
                    document.getElementById('webLinksBlock').style.display = 'block';
                } 
                else if(tabName === 'finance') {
                    document.getElementById('tabFinance').classList.add('active');
                    document.getElementById('stockCardBlock').style.display = cacheStockData ? 'block' : 'none';
                } 
                else if(tabName === 'news') {
                    document.getElementById('tabNews').classList.add('active');
                    const query = document.getElementById('queryInput').value.trim();
                    const newsBlock = document.getElementById('newsGridBlock');
                    newsBlock.innerHTML = `<div class="news-card"><div class="news-title">Live: Market vectors are tracking heavy fluctuations for ${query}.</div><div class="news-source">📰 Financial Bureau · Live</div></div>`;
                    newsBlock.style.display = 'block';
                } 
                else if(tabName === 'images') {
                    document.getElementById('tabImages').classList.add('active');
                    const grid = document.getElementById('imagesGridBlock');
                    const imgUrl = cacheImage ? cacheImage : "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=500&q=80";
                    grid.innerHTML = `<img class="grid-img" src="${imgUrl}"><img class="grid-img" src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=500&q=80">`;
                    grid.style.display = 'grid';
                }
            }

            function performLiveSearch() {
                const query = document.getElementById('queryInput').value.trim();
                if(!query) return;

                document.getElementById('luckyWheelBlock').style.display = 'none';
                document.getElementById('homepageGameBlock').style.display = 'none';
                document.getElementById('resultCard').style.display = 'none';
                document.getElementById('liveClockBlock').style.display = 'none';

                cacheStockData = null; cacheImage = "";

                fetch('/search-engine?q=' + encodeURIComponent(query))
                .then(res => res.json())
                .then(data => {
                    document.getElementById('lblAiInstantMsg').innerText = data.ai_answer;
                    
                    if(data.type === "stock_finance") {
                        cacheStockData = data;
                        document.getElementById('lblStockCompany').innerText = data.company;
                        document.getElementById('lblStockTicker').innerText = data.ticker;
                        document.getElementById('lblStockPrice').innerText = data.price;
                        document.getElementById('lblStockChange').innerText = data.change + " ↑ today";
                        document.getElementById('lblStockOpen').innerText = data.open;
                        document.getElementById('lblStockHigh').innerText = data.high;
                        document.getElementById('lblStockLow').innerText = data.low;
                        document.getElementById('lblStockMcap').innerText = data.mcap;
                    } else if(data.type === "time") {
                        document.getElementById('liveClockBlock').style.display = 'block';
                        if(clockInterval) clearInterval(clockInterval);
                        clockInterval = setInterval(() => { document.getElementById('lblClockTime').innerText = new Date().toLocaleTimeString(); }, 1000);
                    } else {
                        cacheImage = data.image;
                    }

                    const container = document.getElementById('linksContainer');
                    container.innerHTML = data.links.map(item => `
                        <div class="web-link-block">
                            <a class="web-title" href="${item.url}" target="_blank">${item.title}</a>
                            <div class="web-snippet">${item.snippet}</div>
                        </div>
                    `).join('');

                    document.getElementById('resultCard').style.display = 'block';
                    switchGoogleTab('all');
                });
            }

            function clearSearch() {
                document.getElementById('queryInput').value = "";
                document.getElementById('resultCard').style.display = 'none';
                document.getElementById('luckyWheelBlock').style.display = 'flex';
                document.getElementById('homepageGameBlock').style.display = 'block';
            }

            // 🎮 स्नेक गेम रनिंग लूप लॉजिक
            function changeSnakeDir(dir) {
                if(dir === 'left' && dx === 0) { dx = -1; dy = 0; }
                else if(dir === 'right' && dx === 0) { dx = 1; dy = 0; }
                else if(dir === 'up' && dy === 0) { dx = 0; dy = -1; }
                else if(dir === 'down' && dy === 0) { dx = 0; dy = 1; }
            }

            setInterval(() => {
                let head = {x: snake[0].x + dx, y: snake[0].y + dy};
                snake.unshift(head);
                if(head.x === food.x && head.y === food.y) { food = {x: Math.floor(Math.random()*25), y: Math.floor(Math.random()*12)}; }
                else { snake.pop(); }

                if(head.x < 0 || head.x >= 28 || head.y < 0 || head.y >= 14) { snake = [{x:10, y:10}]; dx=1; dy=0; }

                ctx.fillStyle = "#000"; ctx.fillRect(0,0,280,140);
                ctx.fillStyle = "#ff2a75"; ctx.fillRect(food.x*10, food.y*10, 8, 8);
                ctx.fillStyle = "#81c995"; snake.forEach(p => ctx.fillRect(p.x*10, p.y*10, 8, 8));
            }, 150);

            document.getElementById("queryInput").addEventListener("keyup", function(e) { if(e.key === "Enter") { performLiveSearch(); } });
        </script>
    </body>
    </html>
    '''

@app.route('/search-engine', methods=['GET'])
def search_engine():
    query = request.args.get('q', '').strip()
    if not query: return jsonify({'type': 'normal', 'image': '', 'links': []})
    web_data = fetch_complete_google_matrix(query)
    return jsonify(web_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
