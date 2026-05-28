from flask import Flask, render_template, request, jsonify
import urllib.request
import json
import re

app = Flask(__name__)

# 🌐 थेट इंटरनेटवरून खऱ्या गुगल लिंक्स आणि 'पीयुष पाटील' यांचे ब्रँडिंग साठवणारे प्रगत इंजिन
def fetch_real_web_results(query):
    query_clean = query.strip().lower()
    
    # 👑 [स्पेशल ब्रँडिंग फिक्स]: जर कोणी विचारलं की तुला कोणी बनवलंय, तर थेट पीयुष पाटील नाव येणार!
    if "kuni banavla" in query_clean or "who made you" in query_clean or "who created you" in query_clean or "owner" in query_clean or "creator" in query_clean or "banavla" in query_clean:
        return [
            {
                "title": "👑 Developer Status: PIYUSH PATIL (Official)",
                "link": "https://github.com",
                "snippet": "नादच खुळा बॉस! या अल्ट्रा-व्हायरल VIP सर्च इंजिन नेटवर्कला जळगावच्या 'पीयुष पाटील' यांनी बनवलं आहे. ही पीयुष पाटील यांची स्वतःची कडक आणि नेक्स्ट-लेव्हल सायबर सिस्टीम आहे!"
            }
        ]
    
    # स्पेलिंग आणि महत्त्वाचे की-वर्ड्स ऑटो-करेक्ट फिक्स
    if "goole" in query_clean or "google" in query_clean:
        return [
            {"title": "Google - Official Search Engine", "link": "https://www.google.com", "snippet": "Search the world's information, including webpages, images, videos and more. Google has many special features to help you find exactly what you're looking for."},
            {"title": "Google AI Studio", "link": "https://aistudio.google.com", "snippet": "Prototype and experiment with Gemini models, Google's next-generation AI, securely inside the ultimate developer platform."}
        ]
    elif "chatgpt" in query_clean or "openai" in query_clean:
        return [
            {"title": "ChatGPT - Official OpenAI Portal", "link": "https://chatgpt.com", "snippet": "A conversational AI system that listens, learns, and challenges. Ask anything, get instant professional answers and create amazing text or codes."}
        ]
    elif "capcut" in query_clean:
        return [
            {"title": "CapCut - Free All-in-One Video Editor", "link": "https://www.capcut.com", "snippet": "CapCut is a free all-in-one video editing solution that helps you create incredible videos for TikTok, Instagram Reels and WhatsApp Status with ease."}
        ]

    # इतर सर्व सामान्य सर्च क्वेरीसाठी डायनॅमिक वेब रिझल्ट्स
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
                "title": titles[i],
                "link": links[i],
                "snippet": snippets[i] if snippets[i] else f"Click the official blue link to explore live encrypted database parameters about {titles[i]}."
            })
        if results: return results
    except Exception:
        pass

    return [
        {"title": f"{query.capitalize()} - Live Search Hub", "link": f"https://www.google.com/search?q={urllib.parse.quote(query)}", "snippet": f"बॉस, इंटरनेटवरून '{query}' बद्दल थेट अधिकृत वेब लिंक्स फेच केल्या आहेत. अधिक माहितीसाठी वरील मुख्य निळ्या लिंकवर क्लिक करा."}
    ]

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VIP Cyber Search - Piyush Patil Edition</title>
        <style>
            :root {
                --insta-gradient: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
                --cyber-blue: #00f0ff;
                --cyber-pink: #ff2a75;
                --cyber-green: #00ff66;
                --glass-card: rgba(255, 255, 255, 0.05);
            }

            body {
                background: radial-gradient(circle at center, #0c0f26 0%, #020308 100%);
                color: #fff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0; padding: 15px; display: flex; flex-direction: column;
                align-items: center; justify-content: center; min-height: 100vh;
                box-sizing: border-box; overflow-x: hidden;
            }

            .search-container {
                width: 100%; max-width: 450px; text-align: center; z-index: 10;
                position: relative;
            }

            h1 {
                font-family: 'Grand Hotel', 'Brush Script MT', cursive, sans-serif;
                font-size: 56px; margin: 0 0 5px 0;
                background: linear-gradient(45deg, #ff2a75, #ff00f0, #00f0ff);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                text-shadow: 0 0 35px rgba(255, 42, 117, 0.4);
            }

            .tagline { font-size: 12px; color: rgba(255, 255, 255, 0.5); margin-bottom: 35px; letter-spacing: 3px; text-transform: uppercase; font-weight: bold; }

            .search-wrapper { position: relative; width: 100%; margin-bottom: 30px; text-align: left; }

            .search-box {
                display: flex; align-items: center;
                background: rgba(0, 0, 0, 0.8); border: 2px solid rgba(255, 255, 255, 0.12);
                border-radius: 25px; padding: 5px; box-sizing: border-box;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
                transition: all 0.3s ease;
            }
            .search-box:focus-within {
                border-color: var(--cyber-pink);
                box-shadow: 0 0 25px rgba(255, 42, 117, 0.5);
            }

            .search-input {
                flex: 1; border: none; background: transparent; color: #fff;
                padding: 16px 22px; font-size: 16px; outline: none; font-weight: 500;
            }

            .search-btn {
                background: var(--insta-gradient); border: none; color: white;
                padding: 14px 28px; font-size: 15px; font-weight: 800; border-radius: 20px;
                cursor: pointer; transition: 0.2s; margin-right: 4px;
            }

            /* 🕒 ड्रॉपडाऊन पॅनेल (Screenshot 1000005700.jpg स्टाईल) */
            .suggestions-dropdown {
                display: none; position: absolute; top: 105%; left: 0; width: 100%;
                background: #181922; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);
                box-shadow: 0 15px 40px rgba(0,0,0,0.8); z-index: 99; overflow: hidden;
                box-sizing: border-box; padding: 10px 0;
            }
            
            .suggestion-item {
                display: flex; align-items: center; padding: 14px 20px;
                font-size: 15px; color: rgba(255,255,255,0.85); cursor: pointer;
                transition: background 0.2s ease; font-weight: 500;
            }
            .suggestion-item:hover { background: rgba(255, 255, 255, 0.06); color: #fff; }
            .suggestion-item::before { content: "🕒"; margin-right: 15px; font-size: 13px; opacity: 0.5; }

            /* 🗂️ रिझल्ट कार्ड */
            .result-card {
                display: none; width: 100%; background: var(--glass-card);
                border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 30px;
                padding: 25px; text-align: left; box-sizing: border-box;
                backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);
                box-shadow: 0 25px 50px rgba(0,0,0,0.6);
                animation: slideUp 0.4s ease;
            }
            @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

            .result-header { color: var(--cyber-blue); font-size: 13px; font-weight: 800; letter-spacing: 1.5px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
            
            .live-image-frame {
                width: 100%; height: 210px; border-radius: 20px; 
                margin-bottom: 22px; object-fit: cover;
                border: 2px solid rgba(0, 240, 255, 0.25);
                box-shadow: 0 10px 25px rgba(0, 240, 255, 0.2);
            }

            .web-link-block { margin-bottom: 22px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 12px; }
            .web-link-block:last-child { border-bottom: none; margin-bottom: 10px; }
            
            .web-title {
                font-size: 19px; font-weight: 700; color: #4285f4;
                text-decoration: none; display: inline-block; margin-bottom: 5px;
            }
            .web-title:hover { text-decoration: underline; color: #66a0ff; }
            
            .web-url { font-size: 12px; color: var(--cyber-green); margin-bottom: 6px; word-break: break-all; font-weight: bold; }
            .web-snippet { font-size: 14.5px; line-height: 1.5; color: rgba(255, 255, 255, 0.85); }

            .action-btn {
                background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255,255,255,0.2); color: #fff;
                padding: 12px 22px; font-size: 14px; font-weight: 700; border-radius: 14px; cursor: pointer;
            }
            .action-btn:hover { background: #fff; color: #000; }

            .footer-brand { margin-top: 45px; font-size: 11px; color: rgba(255,255,255,0.25); font-weight: 800; text-align: center; width: 100%; }
        </style>
    </head>
    <body>

        <div class="search-container">
            <h1>VIP Search</h1>
            <div class="tagline">Quantum Live Search Engine</div>

            <div class="search-wrapper">
                <div class="search-box">
                    <input type="text" id="queryInput" class="search-input" placeholder="काहीपण सर्च करा बॉस..." autocomplete="off" onfocus="showDropdown()" oninput="filterDropdown()">
                    <button class="search-btn" onclick="performLiveSearch()">SEARCH</button>
                </div>
                
                <div class="suggestions-dropdown" id="suggestionsBox">
                    <div class="suggestion-item" onclick="selectSuggestion('tula kuni banavla')">tula kuni banavla? (Who made you?)</div>
                    <div class="suggestion-item" onclick="selectSuggestion('google')">google</div>
                    <div class="suggestion-item" onclick="selectSuggestion('chatgpt')">chatgpt</div>
                    <div class="suggestion-item" onclick="selectSuggestion('south indian look saree pose')">south indian look saree pose</div>
                    <div class="suggestion-item" onclick="selectSuggestion('capcut')">capcut</div>
                    <div class="suggestion-item" onclick="selectSuggestion('olx')">olx</div>
                    <div class="suggestion-item" onclick="selectSuggestion('esp32')">esp32</div>
                </div>
            </div>

            <div class="result-card" id="resultCard">
                <div class="result-header">
                    <span>📡 GOOGLE LIVE CHANNELS</span>
                    <span style="color:var(--cyber-green); font-weight:900;">● SECURE VERIFIED</span>
                </div>
                
                <img id="liveImage" class="live-image-frame" src="" alt="Live Image">
                <div id="linksContainer"></div>
                
                <br>
                <button class="action-btn" onclick="clearSearch()">Clear</button>
            </div>

            <div class="footer-brand">OWNED AND DEVELOPED BY PIYUSH PATIL © 2026</div>
        </div>

        <script>
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
                for (let item of items) {
                    item.style.display = item.innerText.toLowerCase().includes(input) ? 'flex' : 'none';
                }
            }

            function performLiveSearch() {
                const query = document.getElementById('queryInput').value.trim();
                if(!query) return;

                document.getElementById('suggestionsBox').style.display = 'none';
                document.getElementById('resultCard').style.display = 'none';

                fetch('/search-engine?q=' + encodeURIComponent(query))
                .then(res => res.json())
                .then(data => {
                    const imgElement = document.getElementById('liveImage');
                    const qLower = query.toLowerCase();
                    
                    // 👑 [पीयुष पाटील स्पेशल इमेज]: जर युझर क्रिएटर बद्दल शोधत असेल तर किंग/डॅशिंग इमेज दाखवणे
                    if(qLower.includes("banavla") || qLower.includes("who made you") || qLower.includes("creator")) {
                        imgElement.src = "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=800&q=80"; // Premium King Profile Template
                    } else if(qLower.includes("google") || qLower.includes("goole")) {
                        imgElement.src = "https://images.unsplash.com/photo-1573804633927-bfcbcd909acd?auto=format&fit=crop&w=800&q=80";
                    } else if(qLower.includes("chatgpt")) {
                        imgElement.src = "https://images.unsplash.com/photo-1677442136019-21780efad99a?auto=format&fit=crop&w=800&q=80";
                    } else {
                        imgElement.src = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=60";
                    }
                    imgElement.style.display = 'block';
                    
                    const container = document.getElementById('linksContainer');
                    container.innerHTML = data.results.map(item => `
                        <div class="web-link-block">
                            <a class="web-title" href="${item.link}" target="_blank">${item.title}</a>
                            <div class="web-url">${item.link}</div>
                            <div class="web-snippet">${item.snippet}</div>
                        </div>
                    `).join('');

                    document.getElementById('resultCard').style.display = 'block';
                    
                    // 👑 [व्हॉईस अनाउन्समेंट ब्रँडिंग]: पीयुष पाटील नावाचा कडक मराठी उच्चार
                    if(qLower.includes("banavla") || qLower.includes("who made you") || qLower.includes("creator")) {
                        speakVipVoice("नादच खुळा बॉस! या अल्ट्रा-व्हायरल VIP सर्च इंजिन नेटवर्कला जळगावच्या पीयुष पाटील यांनी बनवलं आहे! ही पीयुष पाटील यांची कडक सिस्टीम आहे!");
                    } else {
                        speakVipVoice("बॉस, अधिकृत लाईव्ह गुगल वेब लिंक्स सापडल्या आहेत!");
                    }
                });
            }

            function clearSearch() {
                document.getElementById('queryInput').value = "";
                document.getElementById('resultCard').style.display = 'none';
            }

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
    if not query: return jsonify({'results': []})
    web_data = fetch_real_web_results(query)
    return jsonify({'results': web_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
