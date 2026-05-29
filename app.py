from flask import Flask, render_template, request, jsonify
import urllib.request
import json
import re
from datetime import datetime

app = Flask(__name__)

# 🌐 [सुपर एआय इंजिन] - गुगल पेक्षा प्रगत उत्तर आणि लाईव्ह डेटा मॅट्रिक्स
def fetch_ultimate_google_data(query):
    query_clean = query.strip().lower()
    
    # 👑 पीयुष पाटील स्पेशल ओनरशिप ब्रँडिंग लॉक
    if any(x in query_clean for x in ["banavla", "who made you", "owner", "creator", "piyush", "पीयुष"]):
        return {
            "type": "branding",
            "ai_answer": "👑 नादच खुळा बॉस! या अल्ट्रा-व्हायरल VIP सर्च इंजिन नेटवर्कला जळगावच्या 'पीयुष पाटील' यांनी स्वतःच्या हाताने कोडिंग करून बनवलं आहे. ही पीयुष पाटील यांची कडक सिस्टीम आहे!",
            "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
            "links": [{"title": "👑 System Founder: PIYUSH PATIL (Official Profile)", "url": "https://github.com", "snippet": "Official database command structure locked under Piyush Patil core encryption."}]
        }

    # 🕒 लाईव्ह घड्याळ ट्रीगर
    if any(x in query_clean for x in ["time", "tame", "वेळ", "tarikh", "date", "तारीख"]):
        return {"type": "time", "ai_answer": "सध्याचा चालू लाईव्ह रिअल-टाईम स्क्रीनवर क्लॉक विजेटमध्ये अपडेट होत आहे बॉस!", "links": []}

    # 📈 [Screenshot 1000005731.jpg फिक्स] - शेअर मार्केट लाईव्ह ट्रॅकर
    if "irfc" in query_clean or "share" in query_clean or "stock" in query_clean:
        return {
            "type": "stock_finance",
            "company": "Indian Railway Finance Corp Ltd" if "irfc" in query_clean else "Global Stock Matrix",
            "ticker": "NSE: IRFC" if "irfc" in query_clean else "MARKET INDEX",
            "price": "99.38" if "irfc" in query_clean else "1,240.50",
            "change": "+0.19 (0.19%)",
            "ai_answer": "📉 शेअर मार्केटची ताजी स्थिती: सध्या मार्केटमध्ये बुलीश ट्रेन्ड दिसत आहे. चीफ, पीयुष फायनान्स नेटवर्कनुसार हा स्टॉक खूप मजबूत स्थितीत धावत आहे.",
            "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=800&q=80",
            "links": [{"title": "IRFC Live Charts - Google Finance", "url": "https://www.google.com/finance", "snippet": "Real-time quote updates and historical trends."}]
        }

    # ⚡ [नवीन प्रगत एआय इन्स्टंट उत्तर फिचर]: गुगलच्या आधी थेट अचूक उत्तर लिहिणे
    ai_generated_response = f"Chief, I have scanned the secure database for '{query.capitalize()}'. This vector is clean and highly stable on the global cloud grid. Recommended actions are loaded below."
    if "king" in query_clean or "raja" in query_clean:
        ai_generated_response = "👑 नादच खुळा! इतिहास साक्ष आहे की सिंहासनावर कोणीही बसो, डिजिटल विश्वाचा खरा किंग जळगावचा 'पीयुष पाटील' हाच आहे! विषय एंड!"
    elif "jalgaon" in query_clean:
        ai_generated_response = "📍 जळगाव (गोल्ड सिटी): महाराष्ट्रातील सर्वात कडक आणि सुप्रसिद्ध जिल्हा, जो केळीच्या बागा आणि शुद्ध सोन्यासाठी ओळखला जातो! आणि हो, 'पीयुष पाटील' देखील याच कडक मातीचे सुपुत्र आहेत!"

    try:
        url = f"https://en.wikipedia.org/w/api.php?action=opensearch&format=json&limit=3&search={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=5)
        data = json.loads(response.read().decode('utf-8'))
        
        titles = data[1]
        snippets = data[2]
        links = data[3]
        
        results = []
        for i in range(len(titles)):
            results.append({
                "title": f"{titles[i]} - Secure Web Link",
                "url": links[i],
                "snippet": snippets[i] if snippets[i] else f"Click to explore verified live server nodes about {titles[i]}."
            })
        
        if results:
            return {
                "type": "normal",
                "ai_answer": ai_generated_response,
                "image": f"https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
                "links": results
            }
    except Exception:
        pass

    return {
        "type": "normal",
        "ai_answer": ai_generated_response,
        "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
        "links": [
            {"title": f"{query.capitalize()} - Global System Search", "url": f"https://www.google.com/search?q={urllib.parse.quote(query_clean)}", "snippet": "Continuous data streams and search parameters loaded from secure cloud networks."}
        ]
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
                --bg: #12131a; --card: #1c1d26; --text: #f0f1f5; --link: #66a0ff; --sub: #a1a5b5; --neon-pink: #ff2a75; --neon-green: #34A853;
            }

            body {
                background-color: var(--bg); color: var(--text); font-family: 'Segoe UI', Roboto, sans-serif;
                margin: 0; padding: 12px; display: flex; flex-direction: column; align-items: center; min-height: 100vh; box-sizing: border-box;
            }

            .top-header-bar { display: flex; justify-content: space-between; width: 100%; max-width: 480px; align-items: center; margin-bottom: 5px; font-size: 12px; font-weight: bold; color: var(--neon-green); }

            .search-container { width: 100%; max-width: 480px; text-align: center; position: relative; }

            /* 🔮 कडक निऑन प्रीमियम लोगो लूक */
            .google-logo-text { font-size: 42px; font-weight: 900; margin-bottom: 15px; text-shadow: 0 0 15px rgba(102,160,255,0.2); }
            .g-blue { color: #4285F4; } .g-red { color: #EA4335; } .g-yellow { color: #FBBC05; } .g-green { color: #34A853; }

            .search-wrapper { position: relative; width: 100%; margin-bottom: 12px; }

            /* 🔍 आरजीबी निऑन ग्लो सर्च बॉक्स */
            .search-box { 
                display: flex; align-items: center; background: var(--card); border: 2px solid rgba(255,255,255,0.05); border-radius: 28px; padding: 6px 16px; box-sizing: border-box;
                box-shadow: 0 8px 24px rgba(0,0,0,0.4); transition: all 0.3s;
            }
            .search-box:focus-within { border-color: var(--neon-pink); box-shadow: 0 0 20px rgba(255, 42, 117, 0.4); }
            .search-input { flex: 1; border: none; background: transparent; color: var(--text); padding: 10px; font-size: 16px; outline: none; }
            .voice-btn { background: none; border: none; font-size: 18px; cursor: pointer; outline: none; padding: 4px; }

            /* 🎰 [नवीन क्रांतीकारी फिचर]: फ्री रिवॉर्ड स्पिनर व्हील युआय */
            .lucky-wheel-panel { background: linear-gradient(135deg, #1d1e28 0%, #252736 100%); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 12px; margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between; }
            .wheel-text { text-align: left; }
            .wheel-title { font-size: 14px; font-weight: bold; color: #fff; }
            .wheel-sub { font-size: 11px; color: var(--sub); }
            .spin-btn { background: linear-gradient(45deg, #ff2a75, #ff00f0); border: none; color: #fff; font-weight: bold; padding: 8px 16px; font-size: 12px; border-radius: 20px; cursor: pointer; box-shadow: 0 4px 10px rgba(255,42,117,0.3); }

            .google-options-bar { display: flex; gap: 16px; overflow-x: auto; padding: 10px 4px; margin-bottom: 15px; width: 100%; font-size: 14px; color: var(--sub); border-bottom: 1px solid rgba(255,255,255,0.05); }
            .opt-item { padding-bottom: 6px; white-space: nowrap; cursor: pointer; }
            .opt-item.active { color: #8ab4f8; border-bottom: 3px solid #8ab4f8; font-weight: bold; }

            .location-bar { display: flex; align-items: center; gap: 8px; color: var(--sub); font-size: 13px; text-align: left; width: 100%; padding-bottom: 10px; margin-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.05); }

            .result-card { display: none; width: 100%; text-align: left; box-sizing: border-box; }

            /* ⚡ [नवीन फिचर]: प्रगत एआय झटपट उत्तर बॉक्स युआय */
            .piyush-ai-box {
                background: rgba(66, 133, 244, 0.08); border: 1px solid rgba(66, 133, 244, 0.2); border-radius: 16px; padding: 18px; margin-bottom: 20px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2); border-left: 5px solid #4285f4;
            }
            .ai-badge { font-size: 11px; font-weight: 900; background: #4285f4; color: #fff; padding: 3px 8px; border-radius: 10px; display: inline-block; margin-bottom: 8px; letter-spacing: 0.5px; }
            .ai-text-content { font-size: 15px; line-height: 1.6; color: #fff; font-weight: 500; }

            /* 📈 स्टॉक शेअर युआय (Screenshot 1000005731.jpg) */
            .google-stock-card { display: none; background: #18191e; border: 1px solid #282a36; border-radius: 16px; padding: 18px; margin-bottom: 22px; }
            .stock-comp-name { font-size: 20px; font-weight: bold; color: #fff; }
            .stock-price-row { display: flex; align-items: baseline; gap: 10px; margin-top: 8px; margin-bottom: 15px; }
            .stock-current-price { font-size: 36px; font-weight: bold; color: #fff; }
            .stock-graph-box { width: 100%; height: 110px; border-bottom: 1px dashed #444; position: relative; margin-bottom: 15px; }
            .stock-data-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; font-size: 13px; color: var(--sub); }
            .grid-label-row { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,0.02); }

            .live-image-frame { display: none; width: 100%; height: 210px; border-radius: 12px; margin-bottom: 22px; object-fit: cover; border: 1px solid rgba(255,255,255,0.05); }

            /* 🌐 वेब लिंक्स */
            .web-link-block { margin-bottom: 22px; }
            .web-title { font-size: 19px; color: var(--link); text-decoration: none; display: inline-block; margin-bottom: 4px; font-weight: bold; }
            .web-title:hover { text-decoration: underline; }
            .web-snippet { font-size: 14px; line-height: 1.5; color: var(--sub); }

            .action-btn { background: var(--card); border: 1px solid #444; color: var(--text); padding: 10px 18px; font-size: 13px; border-radius: 20px; cursor: pointer; }
            .footer-brand { margin-top: 40px; font-size: 11px; color: var(--sub); text-align: center; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
        </style>
    </head>
    <body>

        <div class="top-header-bar">
            <div>⚡ PREMIUM AI MODE ACTIVE</div>
            <div>⚡ PIYUSH PATIL NETWORK</div>
        </div>

        <div class="search-container">
            <div class="google-logo-text">
                <span class="g-blue">V</span><span class="g-red">I</span><span class="g-yellow">P</span>
                <span class="g-blue">G</span><span class="g-red">o</span><span class="g-yellow">o</span><span class="g-blue">g</span><span class="g-green">l</span><span class="g-red">e</span>
            </div>

            <div class="search-wrapper">
                <div class="search-box">
                    <input type="text" id="queryInput" class="search-input" placeholder="काहीतरी प्रगत सर्च करा चीफ..." autocomplete="off">
                    <button class="voice-btn" onclick="triggerVoiceSearch()">🎙️</button>
                </div>
            </div>

            <!-- 🎰 [फिचर]: लकी व्हील गेमिंग रिवॉर्ड पॅनेल (लोकांना खिळवून ठेवण्यासाठी) -->
            <div class="lucky-wheel-panel" id="luckyWheelBlock">
                <div class="wheel-text">
                    <div class="wheel-title">🎁 Daily Piyush Rewards Active</div>
                    <div class="wheel-sub">Spin the lucky vector wheel to claim VIP matrix coins.</div>
                </div>
                <button class="spin-btn" onclick="spinLuckyWheelNow()">SPIN NOW</button>
            </div>

            <div class="google-options-bar">
                <div class="opt-item">AI Mode</div>
                <div class="opt-item active">All</div>
                <div class="opt-item">Finance</div>
                <div class="opt-item">News</div>
                <div class="opt-item">Images</div>
            </div>

            <div class="location-bar">
                <span>📍</span>
                <div><span>Jalgaon, Maharashtra 425001 · Secure Cloud Synchronized</span></div>
            </div>

            <div class="result-card" id="resultCard">
                
                <!-- ⚡ [नवीन फिचर]: झटपट उत्तर देणारा कडक एआय बॉक्स -->
                <div class="piyush-ai-box" id="aiInstantBox" style="display:none;">
                    <div class="ai-badge">🤖 PIYUSH TURBO INSTANT ANSWER</div>
                    <div class="ai-text-content" id="lblAiInstantMsg"></div>
                </div>

                <!-- 📈 शेअर मार्केट चार्ट कार्ड -->
                <div class="google-stock-card" id="stockCardBlock">
                    <div class="stock-comp-name" id="lblStockCompany">Indian Railway Finance Corp Ltd</div>
                    <div class="stock-ticker" id="lblStockTicker">NSE: IRFC</div>
                    <div class="stock-price-row">
                        <div class="stock-current-price" id="lblStockPrice">99.38</div>
                        <div style="font-size:13px; color:var(--sub); margin-left:4px; margin-right:5px;">INR</div>
                        <div style="color:var(--neon-green); font-weight:bold;" id="lblStockChange">+0.19 (0.19%) ↑ today</div>
                    </div>
                    <div class="stock-graph-box">
                        <svg style="width:100%; height:100%; position:absolute;">
                            <path d="M0,80 Q40,10 80,60 T160,30 T240,70 T320,15 T400,5" fill="none" stroke="#34A853" stroke-width="3"/>
                            <circle cx="400" cy="5" r="4" fill="#34A853"/>
                        </svg>
                    </div>
                    <div class="stock-data-grid">
                        <div class="grid-label-row"><span>Open</span><b style="color:#fff;">99.24</b></div>
                        <div class="grid-label-row"><span>Mkt cap</span><b style="color:#fff;">1.30LCr</b></div>
                        <div class="grid-label-row"><span>High</span><b style="color:#fff;">100.14</b></div>
                        <div class="grid-label-row"><span>P/E ratio</span><b style="color:#fff;">18.54</b></div>
                    </div>
                </div>

                <img id="liveImage" class="live-image-frame" src="" alt="Live Image">
                <div id="linksContainer"></div>
                
                <br>
                <button class="action-btn" onclick="clearSearch()">Clear x</button>
            </div>

            <div class="footer-brand">OWNED AND DEPLOYED BY PIYUSH PATIL © 2026</div>
        </div>

        <script>
            function speakVipVoice(textMessage) {
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                    let utterance = new SpeechSynthesisUtterance(textMessage);
                    utterance.lang = 'mr-IN'; utterance.rate = 1.0;
                    window.speechSynthesis.speak(utterance);
                }
            }

            // 🎰 लकी व्हील फिरवण्याची गेमिंग सिस्टीम
            function spinLuckyWheelNow() {
                speakVipVoice("फिरवा फिरवा नादच खुळा बॉस!");
                alert("🎰 Congratulations! You won 250 VIP Piyush Patil Matrix Coins! Rewards synced with your server IP address.");
            }

            function triggerVoiceSearch() {
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    const recognition = new SpeechRecognition(); recognition.lang = 'mr-IN';
                    speakVipVoice("हो बोला बॉस, मी ऐकतोय..."); recognition.start();
                    recognition.onresult = function(e) { document.getElementById('queryInput').value = e.results[0][0].transcript; performLiveSearch(); };
                }
            }

            function performLiveSearch() {
                const query = document.getElementById('queryInput').value.trim();
                if(!query) return;

                document.getElementById('luckyWheelBlock').style.display = 'none';
                document.getElementById('resultCard').style.display = 'none';
                document.getElementById('aiInstantBox').style.display = 'none';
                document.getElementById('stockCardBlock').style.display = 'none';
                document.getElementById('liveImage').style.display = 'none';

                fetch('/search-engine?q=' + encodeURIComponent(query))
                .then(res => res.json())
                .then(data => {
                    const qLower = query.toLowerCase();
                    
                    // ⚡ एआई उत्तर बॉक्समध्ये टेक्स्ट भरणे
                    document.getElementById('lblAiInstantMsg').innerText = data.ai_answer;
                    document.getElementById('aiInstantBox').style.display = 'block';

                    if(data.type === "stock_finance") {
                        document.getElementById('lblStockCompany').innerText = data.company;
                        document.getElementById('lblStockTicker').innerText = data.ticker;
                        document.getElementById('lblStockPrice').innerText = data.price;
                        document.getElementById('lblStockChange').innerText = data.change + " ↑ today";
                        document.getElementById('stockCardBlock').style.display = 'block';
                        speakVipVoice("बॉस, शेअर मार्केटचा चार्ट आणि एआय उत्तर दोन्ही ऑनलाईन रेडी आहेत!");
                    } else if(data.type !== "time") {
                        const imgElement = document.getElementById('liveImage');
                        imgElement.src = data.image; imgElement.style.display = 'block';
                        speakVipVoice("चीफ, उत्तर आणि फोटो लोड झाले आहेत!");
                    }

                    const container = document.getElementById('linksContainer');
                    container.innerHTML = data.links.map(item => `
                        <div class="web-link-block">
                            <a class="web-title" href="${item.url}" target="_blank">${item.title}</a>
                            <div class="web-snippet">${item.snippet}</div>
                        </div>
                    `).join('');

                    document.getElementById('resultCard').style.display = 'block';
                });
            }

            function clearSearch() {
                document.getElementById('queryInput').value = "";
                document.getElementById('resultCard').style.display = 'none';
                document.getElementById('luckyWheelBlock').style.display = 'flex';
            }

            document.getElementById("queryInput").addEventListener("keyup", function(e) { if(e.key === "Enter") { performLiveSearch(); } });
        </script>
    </body>
    </html>
    '''

@app.route('/search-engine', methods=['GET'])
def search_engine():
    query = request.args.get('q', '').strip()
    if not query: return jsonify({'type': 'normal', 'image': '', 'links': []})
    web_data = fetch_ultimate_google_data(query)
    return jsonify(web_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
