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
    <title>🔮 Piyush Mind Reader 🔮</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: linear-gradient(135deg, #1a0933 0%, #0a0314 100%);
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
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid #bd93f9;
            border-radius: 16px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 0 25px rgba(189, 147, 249, 0.3);
            backdrop-filter: blur(10px);
        }
        h1 {
            color: #50fa7b;
            font-size: 1.8rem;
            margin-bottom: 15px;
            text-shadow: 0 0 10px rgba(80, 250, 123, 0.4);
        }
        .steps {
            text-align: left;
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-size: 1rem;
            line-height: 1.6;
            border-left: 4px solid #ff79c6;
        }
        .steps li {
            margin-bottom: 8px;
            list-style-type: none;
        }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 8px;
            max-height: 200px;
            overflow-y: auto;
            background: rgba(0, 0, 0, 0.5);
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .grid-item {
            font-size: 0.85rem;
            color: #f8f8f2;
            padding: 4px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        .magic-btn {
            background: #ff79c6;
            color: #1a0933;
            border: none;
            padding: 14px 30px;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 30px;
            cursor: pointer;
            box-shadow: 0 0 15px rgba(255, 121, 198, 0.4);
            transition: all 0.3s ease;
            width: 100%;
            text-transform: uppercase;
        }
        .magic-btn:hover {
            background: #ff92df;
            box-shadow: 0 0 25px rgba(255, 121, 198, 0.7);
            transform: scale(1.02);
        }
        .result-screen {
            display: none;
            animation: fadeIn 0.5s ease-in-out forwards;
        }
        .final-symbol {
            font-size: 5rem;
            color: #ffb86c;
            margin: 20px 0;
            text-shadow: 0 0 20px rgba(255, 184, 108, 0.6);
            animation: pulse 1.5s infinite;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>

<div class="magic-box" id="mainBox">
    <div id="gameScreen">
        <h1>🔮 पाटील माइंड रीडर 🔮</h1>
        <p style="color: #8be9fd; font-size: 0.9rem; margin-bottom: 15px;">मी तुझ्या मनातलं १००% अचूक ओळखू शकतो!</p>
        
        <div class="steps">
            <strong>या ४ पायऱ्या पाळ भावा:</strong><br><br>
            <li>1️⃣ मनात १० ते ९९ च्या दरम्यान कोणताही <b>एक नंबर</b> पकड.</li>
            <li>2️⃣ आता त्या दोन्ही अंकांची बेरीज कर (उदा. २३ असेल तर २+३ = ५).</li>
            <li>3️⃣ मूळ नंबरमधून ती बेरीज वजा कर (उदा. २३ - ५ = १८).</li>
            <li>4️⃣ आता खालील तक्त्यामध्ये तुझ्या आलेल्या उत्तराच्या समोरचा <b>चिन्ह (Symbol)</b> नीट मनात लक्षात ठेव.</li>
        </div>

        <div class="grid-container" id="symbolGrid"></div>

        <button class="magic-btn" id="readMindBtn">माझं मन वाच!</button>
    </div>

    <div class="result-screen" id="resultScreen">
        <h1>🔮 तुझ्या मनात हेच होतं! 🔮</h1>
        <p style="color: #f8f8f2;">मी तुझ्या डोक्यात चाललेलं चिन्ह हुडकून काढलं आहे:</p>
        <div class="final-symbol" id="targetSymbol">👑</div>
        <p style="color: #50fa7b; font-weight: bold;">विषयच एंड भावा! आहे का नाही जादू? 😎</p>
        <button class="magic-btn" style="margin-top: 20px; background: #8be9fd;" onclick="location.reload()">पुन्हा खेळा</button>
    </div>
</div>

<script>
    // गेम सुरू झाल्यावर प्रत्येक वेळी एक नवीन जादूचा सिम्बॉल निवडला जाईल
    const symbols = ["👑", "🔥", "🚀", "💀", "💎", "👻", "🃏", "🦁", "⚡", "🦖", "🛸"];
    const magicSymbol = symbols[Math.floor(Math.random() * symbols.length)];
    const grid = document.getElementById('symbolGrid');

    // तक्ता तयार करणे (९ च्या पाढ्यातील नंबर्सना मॅजिक सिम्बॉल देणे)
    for (let i = 1; i <= 99; i++) {
        let currentSymbol = "";
        if (i % 9 === 0) {
            currentSymbol = magicSymbol; // ९ च्या पाढ्यात येणाऱ्या सर्व नंबरला सेम सिम्बॉल मिळतो
        } else {
            // बाकीच्या नंबर्सना उरलेले सिम्बॉल्स रँडम मिळतात
            let remainingSymbols = symbols.filter(s => s !== magicSymbol);
            currentSymbol = remainingSymbols[Math.floor(Math.random() * remainingSymbols.length)];
        }
        
        let item = document.createElement('div');
        item.className = 'grid-item';
        item.innerText = `${i} : ${currentSymbol}`;
        grid.appendChild(item);
    }

    // बटन क्लिक वर रिझल्ट दाखवणे
    document.getElementById('readMindBtn').addEventListener('click', function() {
        document.getElementById('gameScreen').style.display = 'none';
        document.getElementById('targetSymbol').innerText = magicSymbol;
        document.getElementById('resultScreen').style.display = 'block';
    });
</script>

</body>
</html>
    """)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
