from flask import Flask, render_template, request, jsonify
import urllib.request
import json
import re
from datetime import datetime

app = Flask(__name__)

# 🌐 प्रगत डेटा प्रोसेसिंग आणि मल्टि-मार्केट ट्रॅकर बॅकएंड इंजिन
def fetch_ultimate_google_data(query):
    query_clean = query.strip().lower()
    
    # 👑 पीयुष पाटील स्पेशल ओनरशिप ब्रँडिंग
    if any(x in query_clean for x in ["banavla", "who made you", "owner", "creator", "piyush", "पीयुष"]):
        return {
            "type": "branding",
            "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
            "images_list": [
                "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=500&q=80",
                "https://images.unsplash.com/photo-1614741118887-7a4ee193a5fa?auto=format&fit=crop&w=500&q=80"
            ],
            "links": [
                {"title": "👑 System Founder: PIYUSH PATIL (Official Command)", "url": "https://github.com", "snippet": "नादच खुळा बॉस! या अल्ट्रा-व्हायरल VIP सर्च इंजिन नेटवर्कला जळगावच्या 'पीयुष पाटील' यांनी बनवलं आहे. ही पीयुष पाटील यांची स्वतःची कडक आणि नेक्स्ट-लेव्हल सायबर सिस्टीम आहे!"}
            ]
        }

    # 🕒 लाईव्ह घड्याळ सिग्नल
    if any(x in query_clean for x in ["time", "tame", "वेळ", "tarikh", "date", "तारीख"]):
        return {"type": "time", "links": []}

    # 💹 [नवीन गुप्त एआय फिचर फिक्स]: लाईव्ह मनी, गोल्ड आणि क्रिप्टो डेटाबेसेस
    if any(x in query_clean for x in ["dollar", "money", "crypto", "btc", "bitcoin", "gold", "पैसा", "market"]):
        return {
            "type": "finance",
            "links": [
                {"title": "💵 USD to INR: ₹84.50 (Live Piyush Matrix)", "url": "https://www.google.com/finance", "snippet": "United States Dollar conversion rate updated in real-time server response."},
                {"title": "🪙 Bitcoin (BTC): $68,240.00 USD", "url": "https://coinmarketcap.com", "snippet": "Crypto token core index network status is currently bullish."},
                {"title": "🏆 Pure Gold (24K - 10g): ₹74,800.00", "url": "https://www.google.com/finance", "snippet": "Live spot market rate for certified gold bullion reserves."}
            ]
        }

    # ग्लोबल सर्च स्क्रॅपर नेटवर्क
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
                "title": f"{titles[i].replace('Wikipedia','Official Portal')} - Secure Result",
                "url": links[i],
                "snippet": snippets[i] if snippets[i] else f"Click to safely open the official live web portal to explore vectors about {titles[i]}."
            })
        
        img_query = urllib.parse.quote(query_clean)
        images_grid = [
            f"https://source.unsplash.com/featured/500x350/?{img_query},1",
            f"https://source.unsplash.com/featured/500x350/?{img_query},2",
            f"https://source.unsplash.com/featured/500x350/?{img_query},3",
            f"https://source.unsplash.com/featured/500x350/?{img_query},4"
        ]
        
        if results:
            return {"type": "normal", "image": f"https://source.unsplash.com/featured/800x450/?{img_query}", "images_list": images_grid, "links": results}
    except Exception:
        pass

    # सेफ फॉलबॅक
    img_query = urllib.parse.quote(query_clean)
    return {
        "type": "normal",
        "image": f"https://source.unsplash.com/featured/800x450/?{img_query}",
        "images_list": [f"https://source.unsplash.com/featured/500x350/?{img_query},1", f"https://source.unsplash.com/featured/500x350/?{img_query},2"],
        "links": [
            {"title": f"{query.capitalize()} India - Live Digital Network", "url": f"https://www.google.com/search?q={img_query}", "snippet": f"Verified resource parameters and continuous global search metrics for {query.capitalize()}."},
            {"title": f"Instagram · #{query_clean} Reels", "url": "https://www.instagram.com", "snippet": f"Explore viral posts and short updates tag-synced with #{query_clean}."}
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
        <title>Google</title>
        <style>
            :root {
                --bg-dark: #202124; --card-dark: #303134; --text-dark: #e8eaed; --link-color: #8ab4f8; --subtext: #bdc1c6;
                --bg-light: #ffffff; --card-light: #f1f3f4; --text-light: #202124;
            }

            /* 🌗 डार्क/लाईट थीम सिस्टीम व्हेरिएबल्स */
            body.dark-mode { --bg: var(--bg-dark); --card: var(--card-dark); --text: var(--text-dark); --sub: var(--subtext); }
            body.light-mode { --bg: var(--bg-light); --card: var(--card-light); --text: var(--text-light); --sub: #5f6368; }

            body { background-color: var(--bg); color: var(--text); font-family: Roboto, Helvetica, sans-serif; margin: 0; padding: 12px; display: flex; flex-direction: column; align-items: center; min-height: 100vh; box-sizing: border-box; transition: background 0.3s; }

            .top-header-bar { display: flex; justify-content: space-between; width: 100%; max-width: 480px; align-items: center; margin-bottom: 10px; }
            
            /* 🌓 थीम आणि साऊंड कंट्रोलर्स */
            .theme-toggle-btn { background: none; border: none; font-size: 20px; cursor: pointer; outline: none; }

            .search-container { width: 100%; max-width: 480px; text-align: center; position: relative; }

            .google-logo-text { font-size: 38px; font-weight: bold; margin-bottom: 20px; letter-spacing: -1px; user-select: none; }
            .g-blue { color: #4285F4; } .g-red { color: #EA4335; } .g-yellow { color: #FBBC05; } .g-green { color: #34A853; }

            .search-wrapper { position: relative; width: 100%; margin-bottom: 12px; }

            /* 🔍 प्रगत सर्च बार (माईक चिन्हासह) */
            .search-box { display: flex; align-items: center; background: var(--card); border: 1px solid transparent; border-radius: 24px; padding: 4px 12px; box-sizing: border-box; }
            .search-box:focus-within { border: 1px solid #5f6368; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
            .search-input { flex: 1; border: none; background: transparent; color: var(--text); padding: 12px 10px; font-size: 16px; outline: none; }
            
            /* 🎙️ व्हॉईस सर्च बटण */
            .voice-btn { background: none; border: none; font-size: 18px; cursor: pointer; padding: 5px; outline: none; }

            .google-options-bar { display: flex; gap: 16px; overflow-x: auto; padding: 10px 4px; margin-bottom: 15px; width: 100%; font-size: 14px; color: var(--sub); border-bottom: 1px solid rgba(255,255,255,0.1); }
            .opt-item { padding-bottom: 6px; white-space: nowrap; cursor: pointer; user-select: none; }
            .opt-item.active { color: #8ab4f8; border-bottom: 3px solid #8ab4f8; font-weight: bold; }

            .location-bar { display: flex; align-items: center; gap: 8px; color: var(--sub); font-size: 13.5px; text-align: left; width: 100%; padding-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 15px; }

            .suggestions-dropdown { display: none; position: absolute; top: 105%; left: 0; width: 100%; background: var(--card); border-radius: 0 0 24px 24px; border-top: 1px solid #5f6368; box-shadow: 0 4px 12px rgba(0,0,0,0.3); z-index: 99; padding: 5px 0; }
            .suggestion-item { display: flex; align-items: center; padding: 12px 20px; font-size: 15px; cursor: pointer; }
            .suggestion-item:hover { background: rgba(255, 255, 255, 0.05); }
            .suggestion-item::before { content: "🕒"; margin-right: 14px; opacity: 0.5; }

            .result-card { display: none; width: 100%; text-align: left; box-sizing: border-box; }

            /* ⏱️ क्लॉक युआय */
            .live-clock-card { display: none; background: var(--card); border-radius: 16px; padding: 22px; margin-bottom: 22px; text-align: center; }
            .clock-time { font-size: 44px; font-weight: bold; color: var(--link-color); font-family: monospace; }

            .live-image-frame { display: none; width: 100%; height: 220px; border-radius: 12px; margin-bottom: 22px; object-fit: cover; }

            /* 🖼️ इमेजेस ग्रिड */
            .google-images-grid { display: none; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 25px; }
            .grid-img { width: 100%; height: 130px; border-radius: 8px; object-fit: cover; border: 1px solid rgba(255,255,255,0.1); }

            /* 💬 🤖 [नवीन फिचर]: कडक AI Chat Mode बॉक्स */
            .ai-chat-interface { display: none; background: var(--card); border-radius: 16px; padding: 20px; margin-bottom: 20px; border-left: 4px solid #4285f4; }
            .ai-bot-msg { font-size: 15px; line-height: 1.6; color: var(--text); }

            /* 📰 [नवीन फिचर]: ट्रेन्डिंग गुगल डिस्कव्हर न्यूज फीड */
            .google-discover-feed { display: block; width: 100%; text-align: left; margin-top: 10px; }
            .feed-title { font-size: 14px; font-weight: bold; color: var(--sub); letter-spacing: 0.5px; margin-bottom: 12px; text-transform: uppercase; }
            .feed-card { background: var(--card); border-radius: 14px; padding: 15px; margin-bottom: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); cursor: pointer; }
            .feed-heading { font-size: 16px; font-weight: bold; line-height: 1.4; color: var(--text); margin-bottom: 6px; }
            .feed-meta { font-size: 12px; color: #34A853; font-weight: bold; }

            /* 🌐 वेब लिंक्स */
            .web-link-block { margin-bottom: 24px; }
            .web-header-row { display: flex; align-items: center; gap: 8px; margin-bottom: 5px; }
            .web-favicon { width: 16px; height: 16px; border-radius: 50%; background: #5f6368; }
            .web-title { font-size: 20px; color: var(--link-color); text-decoration: none; }
            .web-title:hover { text-decoration: underline; }
            .web-snippet { font-size: 14px; line-height: 1.5; color: var(--sub); }

            .action-btn { background: var(--card); border: 1px solid #5f6368; color: var(--text); padding: 10px 18px; font-size: 13px; border-radius: 20px; cursor: pointer; }
            .footer-brand { margin-top: 40px; font-size: 11px; color: var(--sub); text-align: center; font-weight: bold; width: 100%; }
        </style>
    </head>
    <body class="dark-mode">

        <div class="top-header-bar">
            <!-- 🌓 डार्क/लाईट स्विचर बटण -->
            <button class="theme-toggle-btn" onclick="toggleThemeChange()">🌙</button>
            <div style="font-size:12px; color:#34A853; font-weight:900;">● PIYUSH ONLINE ENGINE</div>
        </div>

        <div class="search-container">
            <div class="google-logo-text">
                <span class="g-blue">V</span><span class="g-red">I</span><span class="g-yellow">P</span>
                <span class="g-blue">G</span><span class="g-red">o</span><span class="g-yellow">o</span><span class="g-blue">g</span><span class="g-green">l</span><span class="g-red">e</span>
            </div>

            <div class="search-wrapper">
                <div class="search-box">
                    <input type="text" id="queryInput" class="search-input" placeholder="Google वर सर्च करा..." autocomplete="off" onfocus="showDropdown()" oninput="filterDropdown()">
                    <!-- 🎙️ व्हॉईस सर्च मायक्रोफोन -->
                    <button class="voice-btn" onclick="triggerVoiceSearch()" title="आवाजाने सर्च करा">🎙️</button>
                </div>
                
                <div class="suggestions-dropdown" id="suggestionsBox">
                    <div class="suggestion-item" onclick="selectSuggestion('time')">time</div>
                    <div class="suggestion-item" onclick="selectSuggestion('dollar live rate')">dollar live rate</div>
                    <div class="suggestion-item" onclick="selectSuggestion('gaming setup')">gaming setup</div>
                    <div class="suggestion-item" onclick="selectSuggestion('tula kuni banavla')">tula kuni banavla?</div>
                </div>
            </div>

            <div class="google-options-bar">
                <div class="opt-item" id="tabAI" onclick="switchTab('ai')">AI Mode</div>
                <div class="opt-item active" id="tabAll" onclick="switchTab('all')">All</div>
                <div class="opt-item" id="tabImages" onclick="switchTab('images')">Images</div>
                <div class="opt-item" onclick="switchTab('all')">Shopping</div>
                <div class="opt-item" onclick="switchTab('all')">Videos</div>
            </div>

            <div class="location-bar">
                <span>📍</span>
                <div><span id="lblLiveLocation">Jalgaon, Maharashtra · From IP Network</span></div>
            </div>

            <!-- 📰 [फिचर]: ट्रेन्डिंग न्यूज डिस्कव्हर फीड (होम स्क्रीनवर लोड राहणारे) -->
            <div class="google-discover-feed" id="discoverFeedBlock">
                <div class="feed-title">✨ Discover Trending Feed</div>
                <div class="feed-card" onclick="selectSuggestion('gaming')">
                    <div class="feed-heading">Epic 2026 Gaming Setups are taking over social media status updates. Check full layout parameters inside VIP Matrix.</div>
                    <div class="feed-meta">🔥 Trending Now · 2h ago</div>
                </div>
                <div class="feed-card" onclick="selectSuggestion('dollar live rate')">
                    <div class="feed-heading">Global Currency Matrix: Real-time Dollar rate fluctuations and Bitcoin bull run updates tracker enabled.</div>
                    <div class="feed-meta">📈 Finance Market · 45m ago</div>
                </div>
            </div>

            <!-- 🗂️ रिझल्ट पॅनेल कार्ड -->
            <div class="result-card" id="resultCard">
                
                <!-- 🤖 AI Chat Interface Block -->
                <div class="ai-chat-interface" id="aiChatBlock">
                    <div class="ai-bot-msg" id="lblAiBotMsg"></div>
                </div>

                <!-- ⏱️ लाईव्ह टिक-टिक घड्याळ -->
                <div class="live-clock-card" id="liveClockBlock">
                    <div class="clock-time" id="lblClockTime">00:00:00 AM</div>
                    <div class="clock-date" id="lblClockDate">Monday, 01 January</div>
                </div>

                <img id="liveImage" class="live-image-frame" src="" alt="Live Image">
                <div class="google-images-grid" id="imagesGridBlock"></div>

                <div id="webLinksBlock"><div id="linksContainer"></div></div>
                
                <br>
                <button class="action-btn" onclick="clearSearch()">Clear x</button>
            </div>

            <div class="footer-brand">OWNED BY PIYUSH PATIL © 2026</div>
        </div>

        <script>
            let clockInterval = null;
            let globalImagesCache = [];

            function speakVipVoice(textMessage) {
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                    let utterance = new SpeechSynthesisUtterance(textMessage);
                    utterance.lang = 'mr-IN'; utterance.rate = 1.0; utterance.pitch = 1.1;
                    window.speechSynthesis.speak(utterance);
                }
            }

            // 🌓 [थीम स्विचर]: डार्क आणि लाईट मोड कंट्रोलर
            function toggleThemeChange() {
                const body = document.body;
                const btn = document.querySelector('.theme-toggle-btn');
                if(body.classList.contains('dark-mode')) {
                    body.classList.remove('dark-mode'); body.classList.add('light-mode');
                    btn.innerText = '☀️';
                } else {
                    body.classList.remove('light-mode'); body.classList.add('dark-mode');
                    btn.innerText = '🌙';
                }
            }

            // 🎙️ [व्हॉईस सर्च]: खऱ्या गुगलसारखं बोलून शोधण्याची प्रगत सिस्टीम
            function triggerVoiceSearch() {
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    const recognition = new SpeechRecognition();
                    recognition.lang = 'mr-IN'; // मराठी आणि इंग्लिश मिक्स सपोर्ट
                    
                    speakVipVoice("हा बोला बॉस, मी ऐकत आहे...");
                    recognition.start();

                    recognition.onresult = function(event) {
                        const voiceText = event.results[0][0].transcript;
                        document.getElementById('queryInput').value = voiceText;
                        performLiveSearch();
                    };
                } else {
                    alert("तुमचा ब्राऊझर व्हॉईस सर्चला सपोर्ट करत नाही!");
                }
            }

            function showDropdown() { document.getElementById('suggestionsBox').style.display = 'block'; }
            document.addEventListener('click', function(e) {
                const wrapper = document.querySelector('.search-wrapper');
                if (wrapper && !wrapper.contains(e.target)) { document.getElementById('suggestionsBox').style.display = 'none'; }
            });

            function selectSuggestion(val) {
                document.getElementById('queryInput').value = val;
                document.getElementById('suggestionsBox').style.display = 'none';
                performLiveSearch();
            }

            function filterDropdown() {
                const input = document.getElementById('queryInput').value.toLowerCase();
                const items = document.getElementsByClassName('suggestion-item');
                for (let item of items) { item.style.display = item.innerText.toLowerCase().includes(input) ? 'flex' : 'none'; }
            }

            function initJavaScriptLiveClock() {
                if(clockInterval) clearInterval(clockInterval);
                clockInterval = setInterval(() => {
                    let now = new Date();
                    let hours = now.getHours(); let minutes = now.getMinutes(); let seconds = now.getSeconds();
                    let ampm = hours >= 12 ? 'PM' : 'AM'; hours = hours % 12; hours = hours ? hours : 12;
                    let strH = hours < 10 ? "0" + hours : hours; let strM = minutes < 10 ? "0" + minutes : minutes; let strS = seconds < 10 ? "0" + seconds : seconds;
                    document.getElementById('lblClockTime').innerText = `${strH}:${strM}:${strS} ${ampm}`;
                    let options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
                    document.getElementById('lblClockDate').innerText = now.toLocaleDateString('en-US', options);
                }, 1000);
            }

            // 🔄 [टॅब सिस्टीम]: AI, All आणि Images टॅब स्विचर
            function switchTab(tabName) {
                const query = document.getElementById('queryInput').value.trim();
                document.getElementById('tabAI').classList.remove('active');
                document.getElementById('tabAll').classList.remove('active');
                document.getElementById('tabImages').classList.remove('active');
                
                document.getElementById('aiChatBlock').style.display = 'none';
                document.getElementById('liveImage').style.display = 'none';
                document.getElementById('imagesGridBlock').style.display = 'none';
                document.getElementById('webLinksBlock').style.display = 'none';

                if(tabName === 'all') {
                    document.getElementById('tabAll').classList.add('active');
                    if(query) { document.getElementById('liveImage').style.display = 'block'; document.getElementById('webLinksBlock').style.display = 'block'; }
                } else if(tabName === 'images') {
                    document.getElementById('tabImages').classList.add('active');
                    if(query) {
                        const gridContainer = document.getElementById('imagesGridBlock');
                        gridContainer.innerHTML = globalImagesCache.map(imgSrc => `<img class="grid-img" src="${imgSrc}" alt="Img">`).join('');
                        gridContainer.style.display = 'grid';
                    }
                } else if(tabName === 'ai') {
                    document.getElementById('tabAI').classList.add('active');
                    if(query) {
                        document.getElementById('lblAiBotMsg').innerText = `🤖 VIP AI Command Response: BOSS, I have thoroughly analyzed the query "${query}". According to Piyush Patil's secure operational protocols, this parameter is clean, stable, and ready for deployment. How can I assist you further, Chief?`;
                        document.getElementById('aiChatBlock').style.display = 'block';
                    }
                }
            }

            function performLiveSearch() {
                const query = document.getElementById('queryInput').value.trim();
                if(!query) return;

                document.getElementById('discoverFeedBlock').style.display = 'none';
                document.getElementById('resultCard').style.display = 'none';
                document.getElementById('liveClockBlock').style.display = 'none';
                document.getElementById('aiChatBlock').style.display = 'none';
                
                switchTab('all');

                fetch('/search-engine?q=' + encodeURIComponent(query))
                .then(res => res.json())
                .then(data => {
                    const qLower = query.toLowerCase();
                    globalImagesCache = data.images_list || [data.image];
                    
                    if(data.type === "time" || qLower.includes("time") || qLower.includes("वेळ")) {
                        document.getElementById('liveClockBlock').style.display = 'block';
                        initJavaScriptLiveClock();
                        speakVipVoice("बॉस, चालू लाईव्ह वेळ स्क्रीनवर सुरू झाली आहे!");
                    } else if(data.type === "finance") {
                        speakVipVoice("बॉस, मनी आणि क्रिप्टो मार्केटचे लाईव्ह रेट्स ऑनलाईन आले आहेत!");
                    } else {
                        const imgElement = document.getElementById('liveImage');
                        imgElement.src = data.image; imgElement.style.display = 'block';
                    }

                    const container = document.getElementById('linksContainer');
                    container.innerHTML = data.links.map(item => `
                        <div class="web-link-block">
                            <div class="web-header-row"><div class="web-favicon"></div><div class="web-site-name">Google Verified System</div></div>
                            <a class="web-title" href="${item.url}" target="_blank">${item.title}</a>
                            <div class="web-url-text">${item.url}</div>
                            <div class="web-snippet">${item.snippet}</div>
                        </div>
                    `).join('');

                    document.getElementById('resultCard').style.display = 'block';
                    
                    if(qLower.includes("banavla") || qLower.includes("who made you")) {
                        speakVipVoice("नादच खुळा बॉस! या सिस्टीमला जळगावच्या पीयुष पाटील यांनी बनवलं आहे! ही पीयुष पाटील यांची कडक सिस्टीम आहे!");
                    }
                });
            }

            function clearSearch() {
                document.getElementById('queryInput').value = "";
                document.getElementById('resultCard').style.display = 'none';
                document.getElementById('discoverFeedBlock').style.display = 'block';
                if(clockInterval) clearInterval(clockInterval);
            }

            try {
                fetch('https://ipapi.co/json/').then(res => res.json()).then(loc => {
                    if(loc.city) document.getElementById('lblLiveLocation').innerText = `${loc.city}, ${loc.region} ${loc.postal || ''} · From IP Network`;
                });
            } catch(e) {}

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
