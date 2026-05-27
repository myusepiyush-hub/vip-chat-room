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
    <title>🔮 पाटील मॅजिक कार्ड्स 🔮</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: linear-gradient(135deg, #0d0221 0%, #020005 100%);
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 15px;
        }
        .magic-box {
            width: 100%;
            max-width: 450px;
            background: rgba(255, 255, 255, 0.03);
            border: 2px solid #00f0ff;
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 0 30px rgba(0, 240, 255, 0.2);
            backdrop-filter: blur(15px);
        }
        h1 {
            color: #00f0ff;
            font-size: 1.8rem;
            margin-bottom: 20px;
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
        }
        p {
            color: #e0e0e0;
            font-size: 1.05rem;
            line-height: 1.5;
            margin-bottom: 25px;
        }
        .card-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 30px;
            justify-items: center;
        }
        .card {
            width: 90px;
            height: 130px;
            background: #ffffff;
            color: #000000;
            border-radius: 8px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 2rem;
            font-weight: bold;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            border: 2px solid #fff;
            transition: transform 0.3s;
        }
        .red-card { color: #ff0055; }
        .black-card { color: #111111; }
        
        .magic-btn {
            background: #00f0ff;
            color: #0d0221;
            border: none;
            padding: 15px 30px;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 30px;
            cursor: pointer;
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
            width: 100%;
            text-transform: uppercase;
            transition: all 0.3s ease;
        }
        .magic-btn:hover {
            box-shadow: 0 0 25px #00f0ff;
            transform: scale(1.02);
        }
        .step-indicator {
            background: #ff0055;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>

<div class="magic-box">
    <h1>🔮 पाटील माइंड रीडर 🔮</h1>

    <!-- STEP 1 -->
    <div id="step1">
        <div class="step-indicator">पायरी १/२</div>
        <p>खालील ६ पत्त्यांपैकी कोणताही <b>एक पत्ता</b> मनात घट्ट पकड आणि लक्षात ठेव... विचार बदलू नकोस!</p>
        <div class="card-container">
            <div class="card red-card">♦️K</div>
            <div class="card black-card">♠️Q</div>
            <div class="card red-card">♥️J</div>
            <div class="card black-card">♣️A</div>
            <div class="card red-card">♦️10</div>
            <div class="card black-card">♠️9</div>
        </div>
        <button class="magic-btn" onclick="goToStep2()">मी मनात पकडला, पुढे चला! ➔</button>
    </div>

    <!-- STEP 2 (LOADING) -->
    <div id="step2" style="display: none;">
        <div class="step-indicator">पायरी २/२</div>
        <p id="loadingText">तुझ्या डोक्यात चाललेला विचार मी वाचतोय... थांब भावा...</p>
        <div id="loadingAnimation" style="font-size: 3rem; margin: 30px 0; animation: rotate 2s infinite linear;">🔮</div>
        <button class="magic-btn" id="finalBtn" style="display: none;" onclick="showResult()">तुझ्या मनातला पत्ता गायब कर! 🔥</button>
    </div>

    <!-- RESULT -->
    <div id="resultScreen" style="display: none;">
        <p style="font-size: 1.2rem; color: #50fa7b; font-weight: bold;">😎 विषयच एंड भावा! 😎</p>
        <p>मी तुझ्या मनातील विचार वाचून, तू निवडलेला तो एक पत्ता पूर्णपणे <b>गायब</b> केला आहे! खाली बघ, तुझा पत्ता उडालाय:</p>
        <div class="card-container">
            <div class="card black-card">♠️K</div>
            <div class="card red-card">♦️Q</div>
            <div class="card black-card">♠️J</div>
            <div class="card red-card">♥️A</div>
            <div class="card black-card">♣️10</div>
        </div>
        <button class="magic-btn" style="background: #ff0055; color: white; box-shadow: none;" onclick="location.reload()">पुन्हा खेळ</button>
    </div>
</div>

<script>
    function goToStep2() {
        document.getElementById('step1').style.display = 'none';
        document.getElementById('step2').style.display = 'block';
        
        // २ सेकंदाचा लोड होण्याचा ड्रामा (असं वाटायला पाहिजे की एआय विचार करतोय)
        setTimeout(() => {
            document.getElementById('loadingText').innerText = "मी तुझ्या डोक्यात शिरून तो पत्ता हुडकला आहे! आता खालील बटन दाबायची तयारी कर.";
            document.getElementById('loadingAnimation').innerText = "✅";
            document.getElementById('finalBtn').style.display = 'block';
        }, 2500);
    }

    function showResult() {
        document.getElementById('step2').style.display = 'none';
        document.getElementById('resultScreen').style.display = 'block';
    }
</script>

<style>
    @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
</style>

</body>
</html>
    """)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
