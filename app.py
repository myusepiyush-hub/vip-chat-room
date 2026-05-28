from flask import Flask, render_template, request, jsonify
import urllib.request
import json
import re
from datetime import datetime

app = Flask(__name__)

# 🌐 [गुगल क्लोन इंजिन] - थेट ओरिजिनल ब्रँड डेटा, लाईव्ह टाईम आणि रियल वेब लिंक्स
def fetch_perfect_google_data(query):
    query_clean = query.strip().lower()
    
    # 👑 पीयुष पाटील स्पेशल ओनरशिप ब्रँडिंग
    if "banavla" in query_clean or "who made you" in query_clean or "owner" in query_clean or "creator" in query_clean:
        return {
            "type": "branding",
            "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
            "links": [
                {"title": "👑 Creator Status: PIYUSH PATIL (Official Website)", "url": "https://github.com", "snippet": "नादच खुळा बॉस! या अल्ट्रा-व्हायरल VIP सर्च इंजिन नेटवर्कला जळगावच्या 'पीयुष पाटील' यांनी बनवलं आहे. ही पीयुष पाटील यांची स्वतःची कडक आणि नेक्स्ट-लेव्हल सायबर सिस्टीम आहे!"}
            ]
        }

    # 🕒 [लाईव्ह टाईम फिक्स]: जर युझरने वेळ किंवा टाईम विचारला तर विशेष डिजिटल घड्याळ इंजिन ट्रिगर करणे
    if "time" in query_clean or "tame" in query_clean or "वेळ" in query_clean or "tarikh" in query_clean or "date" in query_clean:
        now = datetime.now()
        return {
            "type": "time",
            "live_time": now.strftime("%I:%M:%S %p"),
            "live_date": now.strftime("%A, %d %B %Y"),
            "links": [{"title": "Time.is - Exact time for any time zone", "url": "https://time.is", "snippet": "Live clock synchronization with global servers. Checked via Piyush Core Time Matrix."}]
        }

    # 🚗 [रियल ब्रँड फिक्स]: स्क्रीनशॉट `1000005702.jpg` प्रमाणे थेट हुबेहूब ओरिजINAL लिंक्स
    if "bmw" in query_clean:
        return {
            "type": "normal",
            "image": "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=800&q=80",
            "links": [
                {"title": "BMW India - Explore Latest Models & Book Test Drive", "url": "https://www.bmw.in", "snippet": "Welcome to the official BMW India website. Discover premium vehicle models, exclusive offers, innovative technologies and first-class services."},
                {"title": "Instagram · bmw (4.4Cr+ followers)", "url": "https://www.instagram.com/bmw", "snippet": "BMW (@bmw) • Munich. 44M followers • 14K posts • The official #BMW account, home of Sheer Driving Pleasure."},
                {"title": "BMW Cars Price in India - CarWale", "url": "https://www.carwale.com/bmw-cars/", "snippet": "BMW cars price starts at Rs. 43.50 Lakh for the cheapest model and goes up to Rs. 2.60 Cr for the most expensive model."}
            ]
        }
    elif "google" in query_clean or "goole" in query_clean:
        return {
            "type": "normal",
            "image": "https://images.unsplash.com/photo-1573804633927-bfcbcd909acd?auto=format&fit=crop&w=800&q=80",
            "links": [
                {"title": "Google - Official Site", "url": "https://www.google.com", "snippet": "Search the world's information, including webpages, images, videos and more. Google has many special features to help you find exactly what you're looking for."},
                {"title": "Google AI Studio", "url": "https://aistudio.google.com", "snippet": "Prototype and experiment with Gemini models, Google's next-generation AI, securely inside the ultimate developer platform."}
            ]
        }
    elif "chatgpt" in query_clean:
        return {
            "type": "normal",
            "image": "https://images.unsplash.com/photo-1677442136019-21780efad99a?auto=format&fit=crop&w=800&q=80",
            "links": [
                {"title": "ChatGPT - Official OpenAI Portal", "url": "https://chatgpt.com", "snippet": "A conversational AI system that listens, learns, and challenges. Ask anything, get instant professional answers and create amazing text or codes."}
            ]
        }
    elif "capcut" in query_clean:
        return {
            "type": "normal",
            "image": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?auto=format&fit=crop&w=800&q=80",
            "links": [
                {"title": "CapCut - Free All-in-One Video Editor", "url": "https://www.capcut.com", "snippet": "CapCut is a free all-in-one video editing solution that helps you create incredible videos for TikTok, Instagram Reels and WhatsApp Status with ease."}
            ]
        }

    # ग्लोबल सर्च फॉलबॅक
    formatted_title = query.capitalize()
    return {
        "type": "normal",
        "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
        "links": [
            {"title": f"{formatted_title} India - Official Verified Website", "url": f"https://www.google.com/search?q={urllib.parse.quote(query)}", "snippet": f"Explore the official global parameters, latest live trends, and verified cloud resources for {formatted_title} on the main secure network."},
            {"title": f"Instagram · #{query_clean} Threads & Posts", "url": "https://www.instagram.com", "snippet": f"See viral trends, short reels, and official community photos tag-synced with #{query_clean} online."}
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
                --google-bg: #202124;
                --google-card-bg: #303134;
                --google-text: #e8eaed;
                --google-link: #8ab4f8;
                --google-subtext: #bdc1c6;
                --google-green: #81c995;
            }

            /* 🖥️ हुबेहूब अधिकृत गुगल डार्क मोड लुक फिक्स */
            body {
                background-color: var(--google-bg);
                color: var(--google-text); font-family: Roboto, Helvetica, Arial, sans-serif;
                margin: 0; padding: 12px; display: flex; flex-direction: column;
                align-items: center; min-height: 100vh; box-sizing: border-box;
            }

            .search-container { width: 100%; max-width: 480px; text-align: center; margin-top: 10px; position: relative; }

            /* 🎨 गुगल निऑन ब्रँडेड लोगो */
            .google-logo-text {
                font-size: 38px; font-weight: bold; margin-bottom: 20px; letter-spacing: -1px;
            }
            .g-blue { color: #4285F4; } .g-red { color: #EA4335; } 
            .g-yellow { color: #FBBC05; } .g-green { color: #34A853; }

            .search-wrapper { position: relative; width: 100%; margin-bottom: 12px; text-align: left; }

            /* 🔍 [फिक्स - Screenshot 1000005702.jpg]: हुबेहूब गुगल सर्च बार */
            .search-box {
                display: flex; align-items: center;
                background: #303134; border: 1px solid transparent;
                border-radius: 24px; padding: 4px 8px; box-sizing: border-box;
                box-shadow: 0 1px 6px rgba(32,33,36,0.28);
            }
            .search-box:focus-within { background: #303134; border: 1px solid #5f6368; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }

            .search-input { flex: 1; border: none; background: transparent; color: var(--google-text); padding: 12px 15px; font-size: 16px; outline: none; }

            .search-btn { background: #3c4043; border: none; color: #e8eaed; padding: 10px 18px; font-size: 14px; border-radius: 4px; cursor: pointer; margin-left: 5px; font-weight: 500; }

            /* 📊 गुगल ऑप्शन्स मेनू बार */
            .google-options-bar {
                display: flex; gap: 16px; justify-content: flex-start; overflow-x: auto;
                padding: 10px 4px; margin-bottom: 15px; width: 100%; font-size: 14px; color: var(--google-subtext);
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .opt-item { cursor: pointer; padding-bottom: 6px; white-space: nowrap; }
            .opt-item.active { color: #8ab4f8; border-bottom: 3px solid #8ab4f8; font-weight: bold; }

            /* 📍 लोकेशन बार पॅटर्न */
            .location-bar {
                display: flex; align-items: center; gap: 8px; color: var(--google-subtext);
                font-size: 13.5px; text-align: left; width: 100%; padding: 0 5px 12px 5px;
                border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 15px;
            }

            /* 🕒 गुगल सजेस्ट बॉक्स */
            .suggestions-dropdown {
                display: none; position: absolute; top: 105%; left: 0; width: 100%;
                background: #303134; border-radius: 0 0 24px 24px; border-top: 1px solid #5f6368;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3); z-index: 99; padding: 5px 0;
            }
            .suggestion-item { display: flex; align-items: center; padding: 12px 20px; font-size: 15px; color: var(--google-text); cursor: pointer; }
            .suggestion-item:hover { background: rgba(255, 255, 255, 0.05); }
            .suggestion-item::before { content: "🕒"; margin-right: 14px; opacity: 0.5; }

            /* 🗂️ गुगल रिझल्ट कार्ड */
            .result-card { display: none; width: 100%; text-align: left; box-sizing: border-box; }

            /* 🕒 [नवीन फिचर]: कडक गुगल लाईव्ह डिजिटल घड्याळ युआय */
            .live-clock-card {
                background: #303134; border-radius: 16px; padding: 20px; margin-bottom: 20px;
                border: 1px solid #404144; box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }
            .clock-time { font-size: 36px; font-weight: bold; color: var(--google-link); font-family: monospace; }
            .clock-date { font-size: 15px; color: var(--google-subtext); margin-top: 5px; }

            .live-image-frame { width: 100%; height: 210px; border-radius: 12px; margin-bottom: 20px; object-fit: cover; }

            /* 🌐 गुगल स्टाईल लिंक्स ब्लॉक */
            .web-link-block { margin-bottom: 24px; }
            .web-header-row { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
            .web-favicon { width: 16px; height: 16px; border-radius: 50%; background: #fff; display: inline-block; }
            .web-site-name { font-size: 12px; color: var(--google-text); }
            .web-url-text { font-size: 12px; color: var(--google-subtext); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 300px; }
            
            .web-title { font-size: 20px; color: var(--google-link); text-decoration: none; display: inline-block; margin-bottom: 4px; }
            .web-title:hover { text-decoration: underline; }
            .web-snippet { font-size: 14px; line-height: 1.5; color: var(--google-subtext); }

            .action-btn { background: #303134; border: 1px solid #5f6368; color: var(--google-text); padding: 10px 16px; font-size: 13px; border-radius: 20px; cursor: pointer; }
            .footer-brand { margin-top: 40px; font-size: 11px; color: var(--google-subtext); }
        </style>
    </head>
    <body>

        <div class="search-container">
            <!-- 🎨 गुगल ब्रँडेड ओरिजिनल लोगो -->
            <div class="google-logo-text">
                <span class="g-blue">V</span><span class="g-red">I</span><span class="g-yellow">P</span>
                <span class="g-blue">G</span><span class="g-red">o</span><span class="g-yellow">o</span><span class="g-blue">g</span><span class="g-green">l</span><span class="g-red">e</span>
            </div>

            <div class="search-wrapper">
                <div class="search-box">
                    <input type="text" id="queryInput" class="search-input" placeholder="Google वर सर्च करा..." autocomplete="off" onfocus="showDropdown()" oninput="filterDropdown()">
                    <button class="search-btn" onclick="performLiveSearch()">सर्च</button>
                </div>
                
                <div class="suggestions-dropdown" id="suggestionsBox">
                    <div class="suggestion-item" onclick="selectSuggestion('time')">time (सध्याची वेळ काय आहे?)</div>
                    <div class="suggestion-item" onclick="selectSuggestion('bmw')">bmw</div>
                    <div class="suggestion-item" onclick="selectSuggestion('tula kuni banavla')">tula kuni banavla?</div>
                    <div class="suggestion-item" onclick="selectSuggestion('google')">google</div>
                    <div class="suggestion-item" onclick="selectSuggestion('chatgpt')">chatgpt</div>
                </div>
            </div>

            <!-- 📊 Google Options Bar -->
            <div class="google-options-bar">
                <div class="opt-item">AI Mode</div>
                <div class="opt-item active">All</div>
                <div class="opt-item">Images</div>
                <div class="opt-item">Shopping</div>
                <div class="opt-item">Videos</div>
            </div>

            <!-- 📍 [फिक्स - Screenshot 1000005702.jpg]: लोकेशन बार युआय -->
            <div class="location-bar">
                <span>📍</span>
                <div><b>Jalgaon, Maharashtra 425001</b> · <span style="color:var(--google-link); cursor:pointer;">Choose area</span></div>
            </div>

            <!-- 🗂️ मुख्य रिझल्ट कार्ड -->
            <div class="result-card" id="resultCard">
                
                <!-- 🕒 [नवीन मॅजिक]: लाईव्ह डिजिटल क्लॉक ब्लॉक -->
                <div class="live-clock-card" id="liveClockBlock" style="display:none;">
                    <div class="clock-time" id="lblClockTime">00:00:00 AM</div>
                    <div class="clock-date" id="lblClockDate">Monday, 01 January 2026</div>
                </div>

                <img id="liveImage" class="live-image-frame" src="" alt="Live Image" style="display:none;">
                <div id="linksContainer"></div>
                
                <br><br>
                <button class="action-btn" onclick="clearSearch()">Clear x</button>
            </div>

            <div class="footer-brand">OWNED BY PIYUSH PATIL © 2026</div>
        </div>

        <script>
            let clockInterval = null;

            function speakVipVoice(textMessage) {
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                    let utterance = new SpeechSynthesisUtterance(textMessage);
                    utterance.lang = 'mr-IN'; utterance.rate = 1.0; utterance.pitch = 1.1;
                    window.speechSynthesis.speak(utterance);
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

            // 🕒 लाईव्ह घड्याळ अपडेटर फंक्शन
            function startLiveClock(initialTime) {
                if(clockInterval) clearInterval(clockInterval);
                let timeParts = initialTime.split(/[: ]/);
                let hours = parseInt(timeParts[0]);
                let minutes = parseInt(timeParts[1]);
                let seconds = parseInt(timeParts[2]);
                let ampm = initialTime.split(' ')[1];

                clockInterval = setInterval(() => {
                    seconds++;
                    if(seconds >= 60) { seconds = 0; minutes++; }
                    if(minutes >= 60) { minutes = 0; hours++; }
                    if(hours > 12) { hours = 1; }
                    
                    let strH = hours < 10 ? "0" + hours : hours;
                    let strM = minutes < 10 ? "0" + minutes : minutes;
                    let strS = seconds < 10 ? "0" + seconds : seconds;
                    
                    document.getElementById('lblClockTime').innerText = `${strH}:${strM}:${strS} ${ampm}`;
                }, 1000);
            }

            function performLiveSearch() {
                const query = document.getElementById('queryInput').value.trim();
                if(!query) return;

                document.getElementById('suggestionsBox').style.display = 'none';
                document.getElementById('resultCard').style.display = 'none';
                document.getElementById('liveClockBlock').style.display = 'none';
                document.getElementById('liveImage').style.display = 'none';
                if(clockInterval) clearInterval(clockInterval);

                fetch('/search-engine?q=' + encodeURIComponent(query))
                .then(res => res.json())
                .then(data => {
                    
                    // 🕒 जर टाईम विचारला असेल तर लाईव्ह घड्याळ उघडणे
                    if(data.type === "time") {
                        document.getElementById('lblClockTime').innerText = data.live_time;
                        document.getElementById('lblClockDate').innerText = data.live_date;
                        document.getElementById('liveClockBlock').style.display = 'block';
                        startLiveClock(data.live_time);
                        speakVipVoice("बॉस, सध्याचा लाईव्ह टाईम स्क्रीनवर चालू आहे!");
                    } else {
                        // नॉर्मल ब्रँड इमेज दाखवणे
                        const imgElement = document.getElementById('liveImage');
                        imgElement.src = data.image;
                        imgElement.style.display = 'block';
                    }

                    // 🌐 गुगल पॅटर्ननुसार लिंक्स लोड करणे
                    const container = document.getElementById('linksContainer');
                    container.innerHTML = data.links.map(item => `
                        <div class="web-link-block">
                            <div class="web-header-row">
                                <div class="web-favicon"></div>
                                <div class="web-site-name">Verified System</div>
                            </div>
                            <a class="web-title" href="${item.url}" target="_blank">${item.title}</a>
                            <div class="web-url-text">${item.url}</div>
                            <div class="web-snippet">${item.snippet}</div>
                        </div>
                    `).join('');

                    document.getElementById('resultCard').style.display = 'block';
                    
                    // पीयुष पाटील ब्रँडिंग अलार्म चेक
                    const qLower = query.toLowerCase();
                    if(qLower.includes("banavla") || qLower.includes("who made you")) {
                        speakVipVoice("नादच खुळा बॉस! या सिस्टीमला जळगावच्या पीयुष पाटील यांनी बनवलं आहे! ही पीयुष पाटील यांची कडक सिस्टीम आहे!");
                    } else if(data.type !== "time") {
                        speakVipVoice("बॉस, गुगल डेटा चॅनेल्स ऑनलाइन आहेत!");
                    }
                });
            }

            function clearSearch() {
                document.getElementById('queryInput').value = "";
                document.getElementById('resultCard').style.display = 'none';
                if(clockInterval) clearInterval(clockInterval);
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
    web_data = fetch_perfect_google_data(query)
    return jsonify(web_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
