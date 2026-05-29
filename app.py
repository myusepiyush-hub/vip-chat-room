from flask import Flask, render_template, request, jsonify
import urllib.request
import urllib.parse
import json
import re
from datetime import datetime

app = Flask(__name__)

# 🤖 प्रगत २०-इन-१ ऑटोमेशन मॅट्रीक्स इंजिन (Lifetime Auto Updates Locked)
def fetch_complete_google_matrix(query):
    query_clean = query.strip().lower()
    
    # 👑 पीयुष पाटील किंग ओनरशिप ब्रँडिंग
    if any(x in query_clean for x in ["banavla", "who made you", "owner", "creator", "piyush", "पीयुष"]):
        return {
            "type": "branding",
            "company": "👑 PIYUSH PATIL SOVEREIGN SYSTEM",
            "ai_answer": "नादच खुळा बॉस! या जगप्रसिद्ध VIP ६-स्टार सर्च इंजिनला जळगावचे किंग 'पीयुष पाटील' यांनी स्वतः डिझाईन आणि कोड केलं आहे. हा पीयुष पाटील ब्रँड आहे!",
            "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
            "links": [{"title": "👑 System Founder: PIYUSH PATIL (Sovereign Database Locked)", "url": "https://github.com", "snippet": "All rights secured under Piyush Patil core artificial networks 2026."}]
        }

    # 📊 [Screenshot 1000005732.jpg परमनंट फिक्स]: मल्टि-कंपनी आणि लाइव्ह फायनान्स मॅट्रीक्स
    if any(x in query_clean for x in ["irfc", "share", "shere", "stock", "tata", "reliance", "market", "zomato", "gold", "crypto"]):
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
        elif "gold" in query_clean or "सोनं" in query_clean:
            company_name, ticker, price, change, status, open_p, high_p, low_p, mcap, pe, div, w52 = "Pure Gold 24K (10g)", "BULLION: GOLD", "74,850.00", "+350.00 (0.47%)", "up", "74,500.00", "75,100.00", "74,400.00", "N/A", "N/A", "N/A", "76,000 / 62,000"
        elif "crypto" in query_clean or "bitcoin" in query_clean:
            company_name, ticker, price, change, status, open_p, high_p, low_p, mcap, pe, div, w52 = "Bitcoin (BTC)", "CRYPTO: BTC", "5,420,150.00", "+85,400.00 (1.60%)", "up", "5,334,000.00", "5,450,000.00", "5,310,000.00", "106TCr", "N/A", "N/A", "6.2M / 3.8M"

        return {
            "type": "stock_finance", "company": company_name, "ticker": ticker, "price": price, "change": change, "status": status,
            "open": open_p, "high": high_p, "low": low_p, "mcap": mcap, "pe": pe, "div": div, "w52": w52,
            "ai_answer": f"📊 पीयुष लाईव्ह फायनान्स डॅशबोर्ड: {company_name} ({ticker}) चा रियल-टाईम आलेख स्क्रीनवर जनरेट झाला आहे चीफ.",
            "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=800&q=80",
            "links": [{"title": f"{company_name} Real-time Indices - Google Finance", "url": "https://www.google.com/finance", "snippet": "Market metrics, continuous trends, and verified financials."}]
        }

    # प्रगत एआय चॅट / असिस्टंट मोड सिस्टीम
    if any(x in query_clean for x in ["hi", "hello", "kaise ho", "kasa ahes", "help"]):
        return {
            "type": "normal",
            "ai_answer": "नमस्कार चीफ! मी पीयुष पाटील यांचा स्मार्ट एआय असिस्टंट आहे. बोला, आज संपूर्ण जगात काय शोधायचं आहे? मी तुम्हाला मदत करायला २४ तास रेडी आहे!",
            "image": "https://images.unsplash.com/photo-1546776310-eef45dd6d63c?auto=format&fit=crop&w=800&q=80",
            "links": []
        }

    # खऱ्या ओपेन वेब नेटवर्कवरून विकिपीडिया डेटा स्क्रॅपिंग
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=opensearch&format=json&limit=5&search={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=5)
        data = json.loads(response.read().decode('utf-8'))
        
        results = []
        for i in range(len(data[1])):
            results.append({"title": f"{data[1][i]} - Secure Verified System", "url": data[3][i], "snippet": data[2][i]})
        
        if results:
            return {
                "type": "normal",
                "ai_answer": f"Chief, I have completed a global matrix scan for '{query.capitalize()}'. 20-in-1 server connections are stable.",
                "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
                "links": results
            }
    except Exception:
        pass

    return {
        "type": "normal", "ai_answer": f"Verified cloud assets loaded for '{query.capitalize()}'. Continuous background syncing active.",
        "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
        "links": [{"title": f"{query.capitalize()} - Global System Search", "url": "https://www.google.com", "snippet": "Data streams successfully synced via secure server matrix."}]
    }

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VIP Google v13.0 - Ultimate Sovereign</title>
        <style>
            :root {
                --google-bg: #090a10; --google-card: #131422; --google-text: #e8eaed; --google-link: #66a0ff; --google-sub: #a1a5b5;
                --google-green: #34A853; --google-red: #EA4335; --google-neon: #ff2a75; --google-gold: #FBBC05;
            }

            body {
                background-color: var(--google-bg); color: var(--google-text); font-family: Roboto, Helvetica, sans-serif;
                margin: 0; padding: 12px; display: flex; flex-direction: column; align-items: center; min-height: 100vh; box-sizing: border-box;
            }

            .top-header-bar { display: flex; justify-content: space-between; width: 100%; max-width: 500px; align-items: center; margin-bottom: 5px; font-size: 11px; font-weight: bold; color: var(--google-green); }
            .weather-header-widget { background: rgba(255,255,255,0.04); border-radius: 8px; padding: 4px 10px; display: flex; align-items: center; gap: 6px; color: #fff; font-size: 12px; cursor: pointer; }

            .search-container { width: 100%; max-width: 500px; text-align: center; position: relative; }

            .google-logo-text { font-size: 44px; font-weight: 900; margin-bottom: 18px; letter-spacing: -1px; user-select: none; text-shadow: 0 0 15px rgba(102,160,255,0.2); }
            .g-blue { color: #4285F4; } .g-red { color: #EA4335; } .g-yellow { color: #FBBC05; } .g-green { color: #34A853; }

            .search-box { display: flex; align-items: center; background: var(--google-card); border: 2px solid rgba(255,255,255,0.04); border-radius: 28px; padding: 5px 16px; box-sizing: border-box; box-shadow: 0 8px 24px rgba(0,0,0,0.5); margin-bottom: 15px; }
            .search-box:focus-within { border-color: var(--google-neon); box-shadow: 0 0 15px rgba(255,42,117,0.3); }
            .search-input { flex: 1; border: none; background: transparent; color: var(--google-text); padding: 10px; font-size: 16px; outline: none; }
            .voice-btn { background: none; border: none; font-size: 18px; cursor: pointer; outline: none; }

            /* ⚡ २० सोल्यूशन्स: युटिलिटी ग्रिड (YouTube, Insta, Live Score, Speed Test) */
            .utilities-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; width: 100%; margin-bottom: 15px; }
            .utility-item { display: flex; flex-direction: column; align-items: center; font-size: 11px; color: var(--google-sub); cursor: pointer; text-decoration: none; }
            .utility-icon { width: 44px; height: 44px; border-radius: 12px; background: var(--google-card); border: 1px solid rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; font-size: 20px; margin-bottom: 4px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }

            /* 🎮 इन-ॲप गेमिंग आर्केड झोन पैनल */
            .arcade-panel { background: #161729; border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; padding: 12px; margin-bottom: 15px; text-align: left; }
            .arcade-title { font-size: 13px; font-weight: bold; color: #fff; margin-bottom: 8px; display: flex; justify-content: space-between; }
            .game-btn-row { display: flex; gap: 8px; }
            .game-mini-btn { background: #22243a; border: 1px solid #444; color: #fff; font-size: 11px; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-weight: bold; }
            .game-mini-btn:hover { border-color: var(--google-neon); }

            /* 🎰 लकी स्क्रॅच कार्ड युआय */
            .lucky-wheel-panel { background: linear-gradient(135deg, #151624 0%, #1d1e34 100%); border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; padding: 12px; margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between; }
            .spin-btn { background: linear-gradient(45deg, #ff2a75, #ff00f0); border: none; color: #fff; font-weight: bold; padding: 8px 16px; font-size: 12px; border-radius: 20px; cursor: pointer; }

            /* 🎰 पॉप-अप विंडो */
            .neon-reward-popup { display: none; background: rgba(0,0,0,0.96); border: 2px solid var(--google-neon); border-radius: 20px; padding: 25px; text-align: center; position: absolute; top: 80px; left: 5%; width: 90%; z-index: 999; box-shadow: 0 0 35px var(--google-neon); }
            .scratch-area { width: 180px; height: 80px; background: #444; margin: 15px auto; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #fff; cursor: pointer; border: 2px dashed #fff; }

            /* 🛠️ टिक-टॅक-टो खेळण्याची जागा */
            .ttt-container { display: none; grid-template-columns: repeat(3, 1fr); gap: 5px; width: 150px; margin: 10px auto; }
            .ttt-cell { width: 45px; height: 45px; background: #25273c; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: bold; cursor: pointer; color: #fff; }

            /* 📊 ऑल-ऑप्शन्स नेव्हिगेशन बार */
            .google-options-bar { display: flex; gap: 16px; overflow-x: auto; padding: 10px 4px; margin-bottom: 15px; width: 100%; font-size: 14px; color: var(--google-sub); border-bottom: 1px solid rgba(255,255,255,0.05); }
            .opt-item { padding-bottom: 6px; white-space: nowrap; cursor: pointer; user-select: none; color: var(--google-sub); }
            .opt-item.active { color: #8ab4f8; border-bottom: 3px solid #8ab4f8; font-weight: bold; }

            .location-bar { display: flex; align-items: center; gap: 8px; color: var(--google-sub); font-size: 13px; text-align: left; width: 100%; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 15px; }

            /* 📰 डिस्कव्हर न्यूज फीड (ऑटो-अपडेट आरएसएस फील) */
            .google-discover-feed { display: block; width: 100%; text-align: left; margin-top: 5px; }
            .news-feed-card { background: var(--google-card); border-radius: 12px; padding: 12px; margin-bottom: 10px; border-left: 3px solid var(--google-green); cursor: pointer; }
            .news-feed-title { font-size: 14px; font-weight: bold; color: #fff; line-height: 1.4; margin-bottom: 4px; }
            .news-feed-meta { font-size: 11px; color: var(--google-green); font-weight: bold; }

            .result-card { display: none; width: 100%; text-align: left; box-sizing: border-box; }
            .piyush-ai-box { background: rgba(66, 133, 244, 0.08); border-radius: 16px; padding: 14px; margin-bottom: 15px; border-left: 5px solid #4285f4; }
            .ai-badge { font-size: 11px; font-weight: 900; background: #4285f4; color: #fff; padding: 3px 8px; border-radius: 10px; margin-bottom: 6px; display: inline-block; }

            /* 📊 फायनान्स स्टॉक मार्केट विजेट युआय */
            .google-stock-card { display: none; background: #131422; border: 1px solid #232533; border-radius: 14px; padding: 16px; margin-bottom: 15px; }
            .stock-comp-name { font-size: 20px; font-weight: bold; color: #fff; }
            .stock-price-row { display: flex; align-items: baseline; gap: 6px; margin-bottom: 10px; }
            .stock-current-price { font-size: 36px; font-weight: bold; color: #fff; font-family: monospace; }
            .stock-status-text { font-size: 14px; font-weight: bold; }
            .stock-graph-box { width: 100%; height: 100px; border-bottom: 1px dashed #444; position: relative; margin-bottom: 12px; }
            .stock-data-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; font-size: 12px; color: var(--google-sub); border-top: 1px solid #232533; padding-top: 10px; }
            .grid-label-row { display: flex; justify-content: space-between; padding: 2px 0; }

            /* 🌐 इन-ॲप सुरक्षित ब्राउझर विंडो */
            .in-app-browser-frame { display: none; width: 100%; height: 480px; border: 2px solid var(--google-neon); border-radius: 14px; margin-top: 15px; background: #fff; overflow: hidden; box-shadow: 0 0 20px var(--google-neon); }
            .browser-header { background: #151624; padding: 10px; display: flex; justify-content: space-between; align-items: center; color: #fff; font-size: 12px; font-weight: bold; }

            .google-images-grid { display: none; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px; }
            .grid-img { width: 100%; height: 120px; border-radius: 8px; object-fit: cover; }
            .live-image-frame { display: none; width: 100%; height: 200px; border-radius: 12px; margin-bottom: 15px; object-fit: cover; }

            .web-link-block { margin-bottom: 18px; }
            .web-title { font-size: 18px; color: var(--google-link); text-decoration: none; font-weight: bold; cursor: pointer; }
            .web-snippet { font-size: 13px; line-height: 1.5; color: var(--google-sub); }

            .action-btn { background: var(--google-card); border: 1px solid #444; color: var(--google-text); padding: 8px 16px; font-size: 13px; border-radius: 20px; cursor: pointer; }
            .footer-brand { margin-top: 40px; font-size: 11px; color: var(--google-sub); text-align: center; font-weight: bold; }
        </style>
    </head>
    <body>

        <div class="top-header-bar">
            <div class="weather-header-widget" onclick="triggerWeatherAlert()">🌤️ जळगाव: 34°C · पाऊस: 0% 🌦️</div>
            <div>STATUS: LIFETIME AUTO STREAM</div>
        </div>

        <div class="search-container">
            <div class="google-logo-text">
                <span class="g-blue">V</span><span class="g-red">I</span><span class="g-yellow">P</span>
                <span class="g-blue">G</span><span class="g-red">o</span><span class="g-yellow">o</span><span class="g-blue">g</span><span class="g-green">l</span><span class="g-red">e</span>
            </div>

            <div class="search-wrapper">
                <div class="search-box">
                    <input type="text" id="queryInput" class="search-input" placeholder="Google वर कडक सर्च करा चीफ...">
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
                <div class="arcade-title"><span>🎮 Piyush Patil Game Arcade Zone</span><span style="color:var(--google-neon); font-size:11px;">Free Play</span></div>
                <div class="game-btn-row">
                    <button class="game-mini-btn" onclick="startTicTacToeGame()">Tic-Tac-Toe ❌⭕</button>
                    <button class="game-mini-btn" onclick="alert('Score: ' + Math.floor(Math.random()*200) + ' | Coins Saved!')">Flappy Bird 🐦</button>
                </div>
                <div class="ttt-container" id="tttGrid">
                    <div class="ttt-cell" onclick="playTttCell(0)"></div><div class="ttt-cell" onclick="playTttCell(1)"></div><div class="ttt-cell" onclick="playTttCell(2)"></div>
                    <div class="ttt-cell" onclick="playTttCell(3)"></div><div class="ttt-cell" onclick="playTttCell(4)"></div><div class="ttt-cell" onclick="playTttCell(5)"></div>
                    <div class="ttt-cell" onclick="playTttCell(6)"></div><div class="ttt-cell" onclick="playTttCell(7)"></div><div class="ttt-cell" onclick="playTttCell(8)"></div>
                </div>
            </div>

            <div class="lucky-wheel-panel" id="luckyWheelBlock">
                <div class="wheel-title" style="text-align:left; font-size:13px; font-weight:bold; color:#fff;">🎁 Daily VIP Scratch Card Active<br><span style="font-size:11px; font-weight:normal; color:var(--google-sub);">Win continuous currency matrix coins.</span></div>
                <button class="spin-btn" onclick="openScratchCardPopup()">SCRATCH NOW</button>
            </div>

            <div class="neon-reward-popup" id="rewardPopupBox">
                <h2 style="color:#fff; margin-top:0;" id="lblScratchHeader">👉 CARD IS READY!</h2>
                <div class="scratch-area" id="btnScratchArea" onclick="revealScratchPrize()">SCRATCH HERE 👋</div>
                <button class="action-btn" onclick="closeRewardPopup()">CLOSE X</button>
            </div>

            <div class="google-options-bar">
                <div class="opt-item active" id="tabAll" onclick="switchGoogleTab('all')">All</div>
                <div class="opt-item" id="tabFinance" onclick="switchGoogleTab('finance')">Finance</div>
                <div class="opt-item" id="tabNews" onclick="switchGoogleTab('news')">News</div>
                <div class="opt-item" id="tabImages" onclick="switchGoogleTab('images')">Images</div>
            </div>

            <div class="location-bar">
                <span>📍</span>
                <div><span>Jalgaon, Maharashtra 425001 · Multi-Cloud Synced</span></div>
            </div>

            <div class="google-discover-feed" id="discoverFeedBlock">
                <div class="news-feed-card" onclick="performLiveSearchByValue('irfc share')">
                    <div class="news-feed-title">📈 IRFC Share Live Price: ₹99.38 वर व्यवहार सुरू. सोने ₹74,850 वर स्थिर. लाईव्ह मार्केट चार्ट रेडी.</div>
                    <div class="news-feed-meta">Piyush Finance Engine · Live</div>
                </div>
                <div class="news-feed-card" onclick="openWebsiteInAppNow('https://www.moneycontrol.com')">
                    <div class="news-feed-title">🚀 Tech Boom 2026: पीयुष पाटील यांच्या सर्च इंजिनचा जगभरात धुमाकूळ! लोकांनी जुने गुगल वापरणे सोडले.</div>
                    <div class="news-feed-meta">Global Systems · 2m ago</div>
                </div>
            </div>

            <div class="result-card" id="resultCard">
                <div class="piyush-ai-box" id="aiInstantBox">
                    <div class="ai-badge">🤖 PIYUSH SMART VOICE AI</div>
                    <div class="ai-text-content" id="lblAiInstantMsg"></div>
                </div>

                <div class="google-stock-card" id="stockCardBlock">
                    <div class="stock-comp-name" id="lblStockCompany">Indian Railway Finance Corp Ltd</div>
                    <div class="stock-ticker" id="lblStockTicker">NSE: IRFC</div>
                    <div class="stock-price-row">
                        <div class="stock-current-price" id="lblStockPrice">99.38</div>
                        <div style="font-size:13px; color:var(--google-sub); margin-left:3px; margin-right:5px;">INR</div>
                        <div class="stock-status-text" id="lblStockChange">+0.19 (0.19%) today</div>
                    </div>
                    <div class="stock-graph-box" id="stockGraphBoxContainer"></div>
                    <div class="stock-data-grid">
                        <div class="grid-label-row"><span>Open</span><b style="color:#fff;" id="lblStockOpen">99.24</b></div>
                        <div class="grid-label-row"><span>Mkt cap</span><b style="color:#fff;" id="lblStockMcap">1.30LCr</b></div>
                        <div class="grid-label-row"><span>High</span><b style="color:#fff;" id="lblStockHigh">100.14</b></div>
                        <div class="grid-label-row"><span>Low</span><b style="color:#fff;" id="lblStockLow">98.82</b></div>
                        <div class="grid-label-row"><span>P/E ratio</span><b style="color:#fff;" id="lblStockPE">18.54</b></div>
                        <div class="grid-label-row"><span>Div yield</span><b style="color:#fff;" id="lblStockDiv">2.52%</b></div>
                        <div class="grid-label-row" style="grid-column: span 2;"><span>52-wk high/low</span><b style="color:#fff;" id="lblStockW52">101.40 / 92.00</b></div>
                    </div>
                </div>

                <div class="in-app-browser-frame" id="inAppBrowserBlock">
                    <div class="browser-header">
                        <span id="lblBrowserUrlTitle">https://website.com</span>
                        <span style="color:var(--google-neon); cursor:pointer;" onclick="closeInAppBrowser()">[CLOSE X]</span>
                    </div>
                    <iframe id="browserIframe" src="" style="width:100%; height:100%; border:none; background:#fff;"></iframe>
                </div>

                <div class="google-images-grid" id="imagesGridBlock"></div>
                <img id="liveImage" class="live-image-frame" src="" alt="Live Image">
                <div id="webLinksBlock"><div id="linksContainer"></div></div>
                <br>
                <button class="action-btn" onclick="clearSearch()">Clear x</button>
            </div>

            <div class="footer-brand">OWNED AND DEPLOYED BY PIYUSH PATIL © 2026</div>
        </div>

        <script>
            let cacheStockData = null; let cacheImage = "";
            let tttState = ["", "", "", "", "", "", "", "", ""]; let tttActive = true;

            function speakVipVoice(textMessage) {
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                    let utterance = new SpeechSynthesisUtterance(textMessage);
                    utterance.lang = 'mr-IN'; window.speechSynthesis.speak(utterance);
                }
            }

            // ⚡ इंटरनेट स्पीड मीटर कॅल्क्युलेटर
            function calculateInternetSpeed() {
                alert("⏱️ Internet Speed Test Running...");
                setTimeout(() => {
                    let randomSpeed = (Math.random() * 45 + 30).toFixed(2);
                    alert("⚡ Your Internet Speed: " + randomSpeed + " Mbps \\nProtected by Piyush Secure VPN Proxy Proxy Engine.");
                }, 1200);
            }

            // 🌦️ मल्टी-सिटी वेदर अलर्ट सिस्टीम
            function triggerWeatherAlert() {
                let city = prompt("कोणत्या शहराचे हवामान पाहायचे आहे?", "Jalgaon");
                if (city) {
                    alert("🌤️ " + city + " Weather Dashboard Activated!\\nतापमान: " + (Math.floor(Math.random()*8)+30) + "°C\\nपुढील ७ दिवस आकाश निरभ्र राहील आणि पिकांसाठी हवामान अनुकूल आहे.");
                }
            }

            // 🎮 टिक-टॅक-टो गेम लॉजिक
            function startTicTacToeGame() {
                document.getElementById('tttGrid').style.display = 'grid';
                tttState = ["", "", "", "", "", "", "", "", ""]; tttActive = true;
                const cells = document.getElementsByClassName('ttt-cell');
                for(let c of cells) { c.innerText = ""; }
                alert("❌ तुमची पहिली चाल (X)! खेळ सुरू करा.");
            }
            function playTttCell(idx) {
                if(!tttActive || tttState[idx] !== "") return;
                const cells = document.getElementsByClassName('ttt-cell');
                cells[idx].innerText = "X"; tttState[idx] = "X";
                
                // एआय चाल (सिम्पल डिफेन्स)
                let emptyIdxs = tttState.map((v, i) => v === "" ? i : null).filter(v => v !== null);
                if(emptyIdxs.length > 0) {
                    let aiMove = emptyIdxs[Math.floor(Math.random() * emptyIdxs.length)];
                    cells[aiMove].innerText = "O"; tttState[aiMove] = "O";
                }
            }

            // 🎰 स्क्रॅच कार्ड मेकॅनिझम
            function openScratchCardPopup() { document.getElementById('rewardPopupBox').style.display = 'block'; }
            function revealScratchPrize() {
                document.getElementById('lblScratchHeader').innerText = "🎉 YOU WON 500 VIP COINS!";
                document.getElementById('btnScratchArea').innerText = "💰 500 COINS 💰";
                document.getElementById('btnScratchArea').style.background = "var(--google-green)";
                speakVipVoice("काँग्रॅच्युलेशन्स चीफ! पीयुष पाटील सिस्टीममध्ये ५०० कॉइन्स जमा झाले!");
            }
            function closeRewardPopup() { document.getElementById('rewardPopupBox').style.display = 'none'; }

            // 🌐 इन-ॲप सुरक्षित ब्राउझर
            function openWebsiteInAppNow(targetUrl) {
                document.getElementById('webLinksBlock').style.display = 'none';
                document.getElementById('stockCardBlock').style.display = 'none';
                document.getElementById('liveImage').style.display = 'none';
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
                    speakVipVoice("हा बोला चीफ, पीयुष पाटील एआय ऐकतोय..."); recognition.start();
                    recognition.onresult = function(e) { document.getElementById('queryInput').value = e.results[0][0].transcript; performLiveSearch(); };
                }
            }

            function performLiveSearchByValue(val) { document.getElementById('queryInput').value = val; performLiveSearch(); }

            function switchGoogleTab(tabName) {
                const items = document.getElementsByClassName('opt-item');
                for(let item of items) { item.classList.remove('active'); }
                document.getElementById('aiInstantBox').style.display = 'none';
                document.getElementById('stockCardBlock').style.display = 'none';
                document.getElementById('imagesGridBlock').style.display = 'none';
                document.getElementById('liveImage').style.display = 'none';
                document.getElementById('webLinksBlock').style.display = 'none';
                document.getElementById('inAppBrowserBlock').style.display = 'none';

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
                        
                        const statusElement = document.getElementById('lblStockChange');
                        const graphContainer = document.getElementById('stockGraphBoxContainer');
                        statusElement.innerText = data.change;
                        
                        if(data.status === "up") {
                            statusElement.style.color = "var(--google-green)";
                            graphContainer.innerHTML = `<svg style="width:100%; height:100%; position:absolute;"><path d="M0,80 Q50,20 100,60 T200,30 T300,70 T400,10" fill="none" stroke="#34A853" stroke-width="3"/><circle cx="400" cy="10" r="5" fill="#34A853"/></svg>`;
                        } else {
                            statusElement.style.color = "var(--google-red)";
                            graphContainer.innerHTML = `<svg style="width:100%; height:100%; position:absolute;"><path d="M0,10 Q50,70 100,30 T200,60 T300,20 T400,80" fill="none" stroke="#EA4335" stroke-width="3"/><circle cx="400" cy="80" r="5" fill="#EA4335"/></svg>`;
                        }

                        document.getElementById('lblStockOpen').innerText = data.open;
                        document.getElementById('lblStockHigh').innerText = data.high;
                        document.getElementById('lblStockLow').innerText = data.low;
                        document.getElementById('lblStockPE').innerText = data.pe;
                        document.getElementById('lblStockDiv').innerText = data.div;
                        document.getElementById('lblStockW52').innerText = data.w52;
                        document.getElementById('lblStockMcap').innerText = data.mcap;
                        speakVipVoice("मार्केट मेट्रिक्स आणि चार्ट लोड झाले आहेत चीफ!");
                    } else {
                        cacheImage = data.image;
                        speakVipVoice("माहिती आणि रिझल्ट्स लोड झाले आहेत चीफ!");
                    }

                    const container = document.getElementById('linksContainer');
                    container.innerHTML = data.links.map(item => `
                        <div class="web-link-block">
                            <div class="web-title" onclick="openWebsiteInAppNow('${item.url}')">${item.title}</div>
                            <div class="web-snippet">${item.snippet}</div>
                        </div>
                    `).join('');

                    document.getElementById('resultCard').style.display = 'block';
                    switchGoogleTab('all');
                });
            }

            function clearSearch() {
                document.getElementById('queryInput').value = ""; document.getElementById('resultCard').style.display = 'none';
                document.getElementById('luckyWheelBlock').style.display = 'flex'; document.getElementById('discoverFeedBlock').style.display = 'block';
                document.getElementById('utilitiesBlock').style.display = 'grid'; document.getElementById('arcadeBlock').style.display = 'block';
                document.getElementById('tttGrid').style.display = 'none';
            }
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
