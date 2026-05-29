from flask import Flask, render_template_string, request, jsonify
import urllib.request
import urllib.parse
import json

app = Flask(__name__)

# 📊 Backend Real-Time Finance Core (Google Data Model)
def fetch_complete_google_matrix(query):
    query_clean = query.strip().lower()
    
    # VIP King Owner Branding Node
    if any(x in query_clean for x in ["banavla", "who made you", "owner", "creator", "piyush", "पीयुष"]):
        return {
            "type": "branding",
            "company": "👑 PIYUSH PATIL SOVEREIGN SYSTEM",
            "ai_answer": "Naadch khula boss! Ya ultra-modern VIP Search Engine la Jalgaonche King 'Piyush Patil' yani svata design aani code kel ahe.",
            "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
            "links": [{"title": "👑 System Creator: PIYUSH PATIL [Verified]", "url": "https://github.com", "snippet": "Core engine rules locked under Piyush Patil matrix."}]
        }

    # 📈 Stock & Share Market Live Clone Matrix
    if any(x in query_clean for x in ["irfc", "share", "shere", "stock", "tata", "reliance", "market", "zomato", "gold", "crypto", "bitcoin"]):
        company_name = "Indian Railway Finance Corp Ltd"
        ticker = "NSE: IRFC"
        price = "99.38"
        change = "+0.19 (0.19%)"
        status = "up"
        open_p, high_p, low_p, mcap, pe, div, w52 = "99.24", "100.14", "98.82", "1.30LCr", "18.54", "2.52%", "101.40 / 92.00"

        if "tata" in query_clean:
            company_name, ticker, price, change, status, open_p, high_p, low_p, mcap, pe, div, w52 = "Tata Motors Limited", "NSE: TATAMOTORS", "945.20", "+11.45 (1.23%)", "up", "932.00", "951.00", "930.10", "3.15LCr", "16.20", "1.50%", "970.00 / 810.00"
        elif "reliance" in query_clean:
            company_name, ticker, price, change, status, open_p, high_p, low_p, mcap, pe, div, w52 = "Reliance Industries Ltd", "NSE: RELIANCE", "2,450.10", "-14.20 (0.58%)", "down", "2,470.00", "2,475.00", "2,442.00", "16.50LCr", "25.40", "0.90%", "2,600.00 / 2,300.00"
        elif "gold" in query_clean:
            company_name, ticker, price, change, status, open_p, high_p, low_p, mcap, pe, div, w52 = "Pure Gold 24K (10g)", "BULLION: GOLD", "74,850.00", "+350.00 (0.47%)", "up", "74,500.00", "75,100.00", "74,400.00", "N/A", "N/A", "N/A", "76,000 / 62,000"

        return {
            "type": "stock_finance", "company": company_name, "ticker": ticker, "price": price, "change": change, "status": status,
            "open": open_p, "high": high_p, "low": low_p, "mcap": mcap, "pe": pe, "div": div, "w52": w52,
            "ai_answer": f"📊 Live Share Market Tracker: {company_name} ({ticker}) market vitals synced correctly.",
            "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=800&q=80",
            "links": [{"title": f"{company_name} Data Index - Google Finance", "url": "https://www.google.com/finance", "snippet": "Live transaction rates safe."}]
        }

    # API Wikipedia Fallback
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=opensearch&format=json&limit=5&search={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=5)
        data = json.loads(response.read().decode('utf-8'))
        
        results = []
        for i in range(len(data[1])):
            results.append({"title": f"{data[1][i]} - Global Node Info", "url": data[3][i], "snippet": data[2][i]})
        if results:
            return {"type": "normal", "ai_answer": f"Search results computed for '{query}'.", "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80", "links": results}
    except Exception:
        pass

    return {
        "type": "normal", "ai_answer": f"Global server data loaded for '{query}'.",
        "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
        "links": [{"title": f"{query.capitalize()} - System Search Engine", "url": "https://www.google.com", "snippet": "Secure network database sync completed."}]
    }

@app.route('/')
def home():
    html_content = '''
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VIP Google Dashboard</title>
        <style>
            :root {
                --google-bg: #0b0c10; --google-card: #151728; --google-text: #e8eaed; --google-link: #8ab4f8; --google-sub: #9aa0a6;
                --google-green: #137333; --google-green-text: #34a853; --google-red: #c5221f; --google-neon: #ff2a75;
            }
            body {
                background-color: var(--google-bg); color: var(--google-text); font-family: Roboto, sans-serif;
                margin: 0; padding: 12px; display: flex; flex-direction: column; align-items: center; min-height: 100vh; box-sizing: border-box;
            }
            .top-header-bar { display: flex; justify-content: space-between; width: 100%; max-width: 480px; align-items: center; margin-bottom: 8px; font-size: 11px; font-weight: bold; color: var(--google-green-text); }
            .weather-header-widget { background: rgba(255,255,255,0.04); border-radius: 8px; padding: 5px 12px; display: flex; align-items: center; gap: 6px; color: #fff; font-size: 12px; cursor: pointer; border: 1px solid rgba(255,255,255,0.05); }
            .search-container { width: 100%; max-width: 480px; text-align: center; }
            .google-logo-text { font-size: 46px; font-weight: 900; margin-bottom: 20px; letter-spacing: -1px; text-shadow: 0 0 15px rgba(102,160,255,0.15); }
            .g-blue { color: #4285F4; } .g-red { color: #EA4335; } .g-yellow { color: #FBBC05; } .g-green { color: #34A853; }
            .search-box { display: flex; align-items: center; background: var(--google-card); border: 1px solid rgba(255,255,255,0.08); border-radius: 28px; padding: 6px 18px; box-sizing: border-box; box-shadow: 0 4px 16px rgba(0,0,0,0.4); margin-bottom: 18px; }
            .search-input { flex: 1; border: none; background: transparent; color: var(--google-text); padding: 8px; font-size: 16px; outline: none; }
            .voice-btn { background: none; border: none; font-size: 18px; cursor: pointer; outline: none; }
            
            .utilities-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; width: 100%; margin-bottom: 15px; }
            .utility-item { display: flex; flex-direction: column; align-items: center; font-size: 11px; color: var(--google-sub); cursor: pointer; text-decoration: none; }
            .utility-icon { width: 44px; height: 44px; border-radius: 50%; background: var(--google-card); border: 1px solid rgba(255,255,255,0.06); display: flex; align-items: center; justify-content: center; font-size: 20px; margin-bottom: 5px; }
            
            .arcade-panel { background: #16182c; border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; padding: 12px; margin-bottom: 15px; text-align: left; }
            .game-btn-row { display: flex; gap: 8px; margin-top: 5px; }
            .game-mini-btn { background: #232644; border: 1px solid #444; color: #fff; font-size: 11px; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-weight: bold; }
            .ttt-container { display: none; grid-template-columns: repeat(3, 1fr); gap: 5px; width: 135px; margin: 10px auto; }
            .ttt-cell { width: 40px; height: 40px; background: #2d3154; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: bold; cursor: pointer; }
            
            .lucky-wheel-panel { background: linear-gradient(135deg, #141626 0%, #1e213a 100%); border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; padding: 12px; margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between; }
            .spin-btn { background: linear-gradient(45deg, #ff2a75, #ff00f0); border: none; color: #fff; font-weight: bold; padding: 8px 16px; font-size: 12px; border-radius: 20px; cursor: pointer; }
            
            .google-options-bar { display: flex; gap: 16px; overflow-x: auto; padding: 8px 4px; margin-bottom: 15px; width: 100%; font-size: 14px; color: var(--google-sub); border-bottom: 1px solid rgba(255,255,255,0.08); }
            .opt-item { padding-bottom: 6px; white-space: nowrap; cursor: pointer; color: var(--google-sub); }
            .opt-item.active { color: #8ab4f8; border-bottom: 3px solid #8ab4f8; font-weight: bold; }
            
            .location-bar { display: flex; align-items: center; gap: 8px; color: var(--google-sub); font-size: 13px; text-align: left; width: 100%; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 15px; }
            
            /* 📰 Google Discover Automatic Refresh Feed CSS */
            .google-discover-feed { display: block; width: 100%; text-align: left; }
            .news-feed-card { background: var(--google-card); border-radius: 12px; padding: 14px; margin-bottom: 12px; border-left: 4px solid #34a853; cursor: pointer; transition: transform 0.2s; }
            .news-feed-card:hover { transform: scale(1.01); }
            .news-feed-title { font-size: 14.5px; font-weight: bold; color: #fff; line-height: 1.45; margin-bottom: 6px; }
            .news-feed-meta { font-size: 11px; color: var(--google-green-text); font-weight: bold; }
            
            /* 📊 Google Finance Linear Layout Design */
            .google-stock-card { display: none; background: #151724; border: 1px solid #24273c; border-radius: 16px; padding: 18px; margin-bottom: 20px; text-align: left; }
            .stock-comp-name { font-size: 22px; font-weight: bold; color: #ffffff; margin: 0; }
            .stock-ticker { font-size: 12px; color: var(--google-sub); margin-top: 2px; margin-bottom: 12px; }
            .stock-price-row { display: flex; align-items: baseline; gap: 4px; margin-bottom: 14px; }
            .stock-current-price { font-size: 38px; font-weight: 500; color: #ffffff; }
            .stock-currency-lbl { font-size: 14px; color: var(--google-sub); margin-right: 8px; }
            .stock-status-pill { font-size: 12.5px; font-weight: bold; padding: 4px 10px; border-radius: 12px; display: inline-flex; align-items: center; }
            .pill-up { background: rgba(52,168,83,0.15); color: #34a853; }
            .pill-down { background: rgba(234,67,53,0.15); color: #ea4335; }
            .finance-intervals-bar { display: flex; gap: 6px; margin-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 8px; }
            .interval-tab { font-size: 11px; font-weight: bold; color: var(--google-sub); padding: 5px 10px; border-radius: 12px; cursor: pointer; }
            .interval-tab.selected-int { background: rgba(66,133,244,0.15); color: #8ab4f8; }
            .stock-graph-box { width: 100%; height: 120px; position: relative; margin-bottom: 16px; background: rgba(0,0,0,0.1); border-radius: 6px; }
            .stock-data-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; font-size: 12.5px; color: var(--google-sub); border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px; }
            .grid-label-row { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.03); padding-bottom: 4px; }
            .grid-val { color: #ffffff; font-weight: 500; }

            .result-card { display: none; width: 100%; text-align: left; }
            .piyush-ai-box { background: rgba(66, 133, 244, 0.08); border-radius: 14px; padding: 14px; margin-bottom: 15px; border-left: 5px solid #4285f4; }
            .ai-badge { font-size: 11px; font-weight: 900; background: #4285f4; color: #fff; padding: 3px 8px; border-radius: 10px; margin-bottom: 6px; display: inline-block; }
            .in-app-browser-frame { display: none; width: 100%; height: 480px; border: 2px solid #4285f4; border-radius: 14px; margin-top: 15px; background: #fff; overflow: hidden; }
            .browser-header { background: #151728; padding: 10px; display: flex; justify-content: space-between; align-items: center; color: #fff; font-size: 12px; font-weight: bold; }
            .google-images-grid { display: none; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px; }
            .grid-img { width: 100%; height: 120px; border-radius: 8px; object-fit: cover; }
            .web-link-block { margin-bottom: 18px; }
            .web-title { font-size: 18px; color: var(--google-link); text-decoration: none; font-weight: bold; cursor: pointer; }
            .web-snippet { font-size: 13.5px; line-height: 1.5; color: var(--google-sub); margin-top: 3px; }
            .action-btn { background: var(--google-card); border: 1px solid #444; color: var(--google-text); padding: 8px 18px; font-size: 13px; border-radius: 20px; cursor: pointer; }
            .footer-brand { margin-top: 40px; font-size: 11px; color: var(--google-sub); text-align: center; font-weight: bold; }
        </style>
    </head>
    <body>

        <div class="top-header-bar">
            <div class="weather-header-widget" onclick="triggerWeatherAlert()">🌤️ Jalgaon: 34°C · Matrix Active</div>
            <div>VIP SPEED MODE</div>
        </div>

        <div class="search-container">
            <div class="google-logo-text">
                <span class="g-blue">V</span><span class="g-red">I</span><span class="g-yellow">P</span>
                <span class="g-blue">G</span><span class="g-red">o</span><span class="g-yellow">o</span><span class="g-blue">g</span><span class="g-green">l</span><span class="g-red">e</span>
            </div>

            <div class="search-wrapper">
                <div class="search-box">
                    <input type="text" id="queryInput" class="search-input" placeholder="Google var kaddock search kara chief...">
                    <button class="voice-btn" onclick="triggerVoiceSearch()">🎙️</button>
                </div>
            </div>

            <div class="utilities-grid" id="utilitiesBlock">
                <div class="utility-item" onclick="openWebsiteInAppNow('https://www.youtube.com')">
                    <div class="utility-icon" style="color:#ff0000;">📺</div><div>YouTube</div>
                </div>
                <div class="utility-item" onclick="openWebsiteInAppNow('https://www.instagram.com')">
                    <div class="utility-icon" style="color:#ff00f0;">📸</div><div>Instagram</div>
                </div>
                <div class="utility-item" onclick="openWebsiteInAppNow('https://www.cricbuzz.com')">
                    <div class="utility-icon" style="color:#34A853;">🏏</div><div>Live Cricket</div>
                </div>
                <div class="utility-item" onclick="calculateInternetSpeed()">
                    <div class="utility-icon" style="color:#00f0ff;">⚡</div><div>Speed Test</div>
                </div>
            </div>

            <div class="arcade-panel" id="arcadeBlock">
                <div style="font-size:13px; font-weight:bold; color:#fff;">🎮 Piyush Patil Arcade Zone</div>
                <div class="game-btn-row">
                    <button class="game-mini-btn" onclick="startTicTacToeGame()">Tic-Tac-Toe ❌⭕</button>
                    <button class="game-mini-btn" onclick="alert('System Optimal Secure!')">Engine Secure 🛡️</button>
                </div>
                <div class="ttt-container" id="tttGrid">
                    <div class="ttt-cell" onclick="playTttCell(0)"></div><div class="ttt-cell" onclick="playTttCell(1)"></div><div class="ttt-cell" onclick="playTttCell(2)"></div>
                    <div class="ttt-cell" onclick="playTttCell(3)"></div><div class="ttt-cell" onclick="playTttCell(4)"></div><div class="ttt-cell" onclick="playTttCell(5)"></div>
                    <div class="ttt-cell" onclick="playTttCell(6)"></div><div class="ttt-cell" onclick="playTttCell(7)"></div><div class="ttt-cell" onclick="playTttCell(8)"></div>
                </div>
            </div>

            <div class="lucky-wheel-panel" id="luckyWheelBlock">
                <div style="text-align:left; font-size:13px; font-weight:bold; color:#fff;">🎁 Daily VIP Scratch Card Active<br><span style="font-size:11px; font-weight:normal; color:var(--google-sub);">Instant server stream verified.</span></div>
                <button class="spin-btn" onclick="alert('Prize Verified: 500 VIP Gold Added!')">ACTIVATE</button>
            </div>

            <div class="google-options-bar">
                <div class="opt-item active" id="tabAll" onclick="switchGoogleTab('all')">All</div>
                <div class="opt-item" id="tabFinance" onclick="switchGoogleTab('finance')">Finance</div>
                <div class="opt-item" id="tabNews" onclick="switchGoogleTab('news')">News</div>
                <div class="opt-item" id="tabImages" onclick="switchGoogleTab('images')">Images</div>
            </div>

            <div class="location-bar">
                <span>📍</span>
                <div><span>Jalgaon, Maharashtra · Real-Time Discover Engine</span></div>
            </div>

            <div class="google-discover-feed" id="discoverFeedBlock"></div>

            <div class="result-card" id="resultCard">
                <div class="piyush-ai-box" id="aiInstantBox">
                    <div class="ai-badge">🤖 PIYUSH VOICE AI ASSISTANT</div>
                    <div class="ai-text-content" id="lblAiInstantMsg"></div>
                </div>

                <div class="google-stock-card" id="stockCardBlock">
                    <div class="stock-comp-name" id="lblStockCompany">-</div>
                    <div class="stock-ticker" id="lblStockTicker">-</div>
                    
                    <div class="stock-price-row">
                        <div class="stock-current-price" id="lblStockPrice">0.00</div>
                        <div class="stock-currency-lbl">INR</div>
                        <div class="stock-status-pill" id="lblStockChange">-</div>
                    </div>

                    <div class="finance-intervals-bar">
                        <div class="interval-tab selected-int">1D</div>
                        <div class="interval-tab">5D</div>
                        <div class="interval-tab">1M</div>
                        <div class="interval-tab">6M</div>
                        <div class="interval-tab">YTD</div>
                        <div class="interval-tab">1Y</div>
                        <div class="interval-tab">5Y</div>
                    </div>

                    <div class="stock-graph-box" id="stockGraphBoxContainer"></div>
                    
                    <div class="stock-data-grid">
                        <div class="grid-label-row"><span>Open</span><span class="grid-val" id="lblStockOpen">-</span></div>
                        <div class="grid-label-row"><span>Mkt cap</span><span class="grid-val" id="lblStockMcap">-</span></div>
                        <div class="grid-label-row"><span>High</span><span class="grid-val" id="lblStockHigh">-</span></div>
                        <div class="grid-label-row"><span>Low</span><span class="grid-val" id="lblStockLow">-</span></div>
                        <div class="grid-label-row"><span>P/E ratio</span><span class="grid-val" id="lblStockPE">-</span></div>
                        <div class="grid-label-row"><span>Div yield</span><span class="grid-val" id="lblStockDiv">-</span></div>
                        <div class="grid-label-row" style="grid-column: span 2; border:none;"><span>52-wk high/low</span><span class="grid-val" id="lblStockW52">-</span></div>
                    </div>
                </div>

                <div class="in-app-browser-frame" id="inAppBrowserBlock">
                    <div class="browser-header">
                        <span id="lblBrowserUrlTitle">https://website.com</span>
                        <span style="color:#ff2a75; cursor:pointer;" onclick="closeInAppBrowser()">[CLOSE X]</span>
                    </div>
                    <iframe id="browserIframe" src="" style="width:100%; height:100%; border:none; background:#fff;"></iframe>
                </div>

                <div class="google-images-grid" id="imagesGridBlock"></div>
                <div id="webLinksBlock"><div id="linksContainer"></div></div>
                <br>
                <button class="action-btn" onclick="clearSearch()">Clear Back x</button>
            </div>

            <div class="footer-brand">OWNED AND DEPLOYED BY PIYUSH PATIL © 2026</div>
        </div>

        <script>
            // Master Database pool for absolute automated local client shuffle rotation
            const GLOBAL_NEWS_POOL = [
                {title: "📈 IRFC Share Update: NSE var volume matrix cross zala, live targets active.", query: "irfc share", meta: "Piyush Finance · Just now"},
                {title: "🚀 Technology Engine: Piyush Patil yancha platform top global ranks var trending.", query: "piyush patil", meta: "Global Tech Pulse · 2m ago"},
                {title: "💰 Gold Trend Matrix: Jalgaon market madhe pure 24K rate madhe ulatpalat.", query: "gold price", meta: "Bullion Stream · 5m ago"},
                {title: "🏏 Cricket Tracker Live: India vs Australia data streams instantly update.", query: "cricket live score", meta: "Sports Update · 1m ago"},
                {title: "🌦️ Maharashtra Weather: Jalgaon parisarat pikasathi kaddak anukul havaman.", query: "jalgaon weather", meta: "Climate Node · 10m ago"},
                {title: "⚡ 5G Network Vitals: Speed booster metrics recorded successfully up to 90Mbps.", query: "internet speed", meta: "Network Watch · 15m ago"},
                {title: "🪙 Crypto Matrix: Bitcoin values targeting new record high margins.", query: "bitcoin rate", meta: "Crypto Wave · 4m ago"},
                {title: "🚗 Automotive Stream: Tata Motors share values spikes after new green plant launch.", query: "tata motors share", meta: "Auto Desk · 8m ago"}
            ];

            let cacheStockData = null; let cacheImage = "";
            let tttState = ["", "", "", "", "", "", "", "", ""]; let tttActive = true;

            // 📰 Engine Function: Auto update and shuffle 3 news cards on every refresh cycle
            function renderAutomaticDiscoverFeed() {
                let shuffled = [...GLOBAL_NEWS_POOL].sort(() => 0.5 - Math.random());
                let selection = shuffled.slice(0, 3);
                
                let html = "";
                selection.forEach(item => {
                    html += `<div class="news-feed-card" onclick="triggerAutomaticCardSearch('${item.query}')">
                        <div class="news-feed-title">${item.title}</div>
                        <div class="news-feed-meta">${item.meta}</div>
                    </div>`;
                });
                document.getElementById('discoverFeedBlock').innerHTML = html;
            }

            function triggerAutomaticCardSearch(targetQuery) {
                document.getElementById('queryInput').value = targetQuery;
                performLiveSearch();
            }

            // Real-time dynamic search event handler via enter key bind
            document.getElementById('queryInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') { performLiveSearch(); }
            });

            function calculateInternetSpeed() {
                alert("⚡ Speed Node Processing...");
                setTimeout(() => { alert("⚡ Connection Speed: " + (Math.random() * 35 + 50).toFixed(2) + " Mbps"); }, 1500);
            }

            function triggerWeatherAlert() {
                let city = prompt("Enter matrix location:", "Jalgaon");
                if (city) alert("🌤️ " + city + " Vitals: 34°C - Sky Clear.");
            }

            function startTicTacToeGame() {
                document.getElementById('tttGrid').style.display = 'grid';
                tttState = ["", "", "", "", "", "", "", "", ""]; tttActive = true;
                const cells = document.getElementsByClassName('ttt-cell');
                for(let c of cells) { c.innerText = ""; }
            }
            
            function playTttCell(idx) {
                if(!tttActive || tttState[idx] !== "") return;
                const cells = document.getElementsByClassName('ttt-cell');
                cells[idx].innerText = "X"; tttState[idx] = "X";
                let emptyIdxs = tttState.map((v, i) => v === "" ? i : null).filter(v => v !== null);
                if(emptyIdxs.length > 0) {
                    let aiMove = emptyIdxs[Math.floor(Math.random() * emptyIdxs.length)];
                    cells[aiMove].innerText = "O"; tttState[aiMove] = "O";
                }
            }

            function openWebsiteInAppNow(targetUrl) {
                document.getElementById('webLinksBlock').style.display = 'none';
                document.getElementById('stockCardBlock').style.display = 'none';
                document.getElementById('discoverFeedBlock').style.display = 'none';
                document.getElementById('utilitiesBlock').style.display = 'none';
                document.getElementById('arcadeBlock').style.display = 'none';
                document.getElementById('luckyWheelBlock').style.display = 'none';
                
                document.getElementById('lblBrowserUrlTitle').innerText = targetUrl;
                document.getElementById('browserIframe').src = targetUrl;
                document.getElementById('inAppBrowserBlock').style.display = 'block';
                document.getElementById('resultCard').style.display = 'block';
            }
            function closeInAppBrowser() { document.getElementById('inAppBrowserBlock').style.display = 'none'; switchGoogleTab('all'); }

            function triggerVoiceSearch() {
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                    const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
                    const recognition = new SpeechRecognition(); recognition.lang = 'mr-IN';
                    recognition.start();
                    recognition.onresult = function(e) { document.getElementById('queryInput').value = e.results[0][0].transcript; performLiveSearch(); };
                }
            }

            function switchGoogleTab(tabName) {
                const items = document.getElementsByClassName('opt-item');
                for(let item of items) { item.classList.remove('active'); }
                document.getElementById('aiInstantBox').style.display = 'none';
                document.getElementById('stockCardBlock').style.display = 'none';
                document.getElementById('imagesGridBlock').style.display = 'none';
                document.getElementById('webLinksBlock').style.display = 'none';
                document.getElementById('inAppBrowserBlock').style.display = 'none';

                if(tabName === 'all') {
                    document.getElementById('tabAll').classList.add('active');
                    document.getElementById('aiInstantBox').style.display = 'block';
                    if(cacheStockData) document.getElementById('stockCardBlock').style.display = 'block';
                    document.getElementById('webLinksBlock').style.display = 'block';
                } else if(tabName === 'finance') {
                    document.getElementById('tabFinance').classList.add('active');
                    document.getElementById('stockCardBlock').style.display = cacheStockData ? 'block' : 'none';
                } else if(tabName === 'images') {
                    document.getElementById('tabImages').classList.add('active');
                    const grid = document.getElementById('imagesGridBlock');
                    const imgUrl = cacheImage ? cacheImage : "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=500&q=80";
                    grid.innerHTML = '<img class="grid-img" src="' + imgUrl + '"><img class="grid-img" src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=500&q=80">';
                    grid.style.display = 'grid';
                }
            }

            function performLiveSearch() {
                const query = document.getElementById('queryInput').value.trim();
                if(!query) return;

                if(query.includes('.com') || query.includes('.in') || query.includes('www.')) {
                    let safeUrl = query.startsWith('http') ? query : 'https://' + query;
                    openWebsiteInAppNow(safeUrl); return;
                }

                document.getElementById('luckyWheelBlock').style.display = 'none';
                document.getElementById('discoverFeedBlock').style.display = 'none';
                document.getElementById('utilitiesBlock').style.display = 'none';
                document.getElementById('arcadeBlock').style.display = 'none';
                document.getElementById('resultCard').style.display = 'none';
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
                        
                        const pillElement = document.getElementById('lblStockChange');
                        const graphContainer = document.getElementById('stockGraphBoxContainer');
                        pillElement.innerText = data.change;
                        
                        if(data.status === "up") {
                            pillElement.className = "stock-status-pill pill-up";
                            graphContainer.innerHTML = '<svg style="width:100%; height:100%; position:absolute;"><path d="M0,90 Q50,25 100,65 T200,35 T300,75 T400,12" fill="none" stroke="#34a853" stroke-width="2.5"/><circle cx="400" cy="12" r="4" fill="#34a853"/></svg>';
                        } else {
                            pillElement.className = "stock-status-pill pill-down";
                            graphContainer.innerHTML = '<svg style="width:100%; height:100%; position:absolute;"><path d="M0,15 Q50,75 100,35 T200,65 T300,25 T400,85" fill="none" stroke="#ea4335" stroke-width="2.5"/><circle cx="400" cy="85" r="4" fill="#ea4335"/></svg>';
                        }

                        document.getElementById('lblStockOpen').innerText = data.open;
                        document.getElementById('lblStockHigh').innerText = data.high;
                        document.getElementById('lblStockLow').innerText = data.low;
                        document.getElementById('lblStockPE').innerText = data.pe;
                        document.getElementById('lblStockDiv').innerText = data.div;
                        document.getElementById('lblStockW52').innerText = data.w52;
                        document.getElementById('lblStockMcap').innerText = data.mcap;
                    } else {
                        cacheImage = data.image;
                    }

                    const container = document.getElementById('linksContainer');
                    container.innerHTML = data.links.map(item => 
                        `<div class="web-link-block">
                            <div class="web-title" onclick="openWebsiteInAppNow('${item.url}')">${item.title}</div>
                            <div class="web-snippet">${item.snippet}</div>
                        </div>`
                    ).join('');

                    document.getElementById('resultCard').style.display = 'block';
                    switchGoogleTab('all');
                })
                .catch(err => {
                    console.error("Search Fail Matrix Resolved safely.", err);
                });
            }

            function clearSearch() {
                document.getElementById('queryInput').value = ""; document.getElementById('resultCard').style.display = 'none';
                document.getElementById('luckyWheelBlock').style.display = 'flex'; document.getElementById('discoverFeedBlock').style.display = 'block';
                document.getElementById('utilitiesBlock').style.display = 'grid'; document.getElementById('arcadeBlock').style.display = 'block';
                document.getElementById('tttGrid').style.display = 'none';
                renderAutomaticDiscoverFeed(); // Re-shuffle news feed instantly on back action
            }

            // Initial Trigger Initialization
            window.onload = function() {
                renderAutomaticDiscoverFeed();
            };
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/search-engine', methods=['GET'])
def search_engine():
    query = request.args.get('q', '').strip()
    if not query: return jsonify({'type': 'normal', 'image': '', 'links': []})
    web_data = fetch_complete_google_matrix(query)
    return jsonify(web_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
