from flask import Flask, render_template_string
import random

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>piyush patil Infinite</title>
    <style>
        body { background: #050505; font-family: 'Arial', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; color: #fff; }
        .box { background: rgba(20, 20, 20, 0.95); padding: 30px; border-radius: 25px; border: 2px solid #ff0055; width: 90%; max-width: 450px; box-shadow: 0 0 40px #ff0055; text-align: center; }
        .btn { padding: 15px; width: 100%; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; margin-bottom: 12px; color: white; }
        .roast { background: #ff0055; }
        .love { background: #00d4ff; }
        .task { background: #70ff00; color: #000; }
        #result { margin-top: 25px; font-size: 1.3em; color: #ffeb3b; padding: 15px; border-top: 2px dashed #444; }
    </style>
</head>
<body>
    <div class="box">
        <h1>🔥 Infinite Fun Zone 🔥</h1>
        <input type="text" id="name" placeholder="तुमचं नाव टाका..." style="padding:10px; width:80%; border-radius:5px;">
        <button class="btn roast" onclick="generate('roast')">Roast Me! 💀</button>
        <button class="btn love" onclick="generate('love')">Love Quote ❤️</button>
        <button class="btn task" onclick="generate('task')">Give Me Task 🎯</button>
        <div id="result"></div>
    </div>

    <script>
        const parts = {
            roast: ["तू", "तुझा चेहरा", "तुझं डोकं", "तुझी अक्कल"],
            roast_end: ["आरशात बघून पण लाजते!", "कॉमेडी शोला पण लाजवेल!", "वाळलेल्या कांद्यापेक्षा खराब आहे!", "निसर्गाची मोठी चूक आहे!"],
            love: ["तुझं हास्य", "तुझा स्वभाव", "तुझं मन", "तुझी मैत्री"],
            love_end: ["सगळ्यात सुंदर आहे!", "कोणाचंही हृदय जिंकू शकतं!", "सोन्यासारखं चमकतंय!", "देवदूतासारखं भारी आहे!"],
            task: ["पुढच्या ५ मिनिटांत", "आज दिवसभरात", "लगेच आताच"],
            task_end: ["एक सेल्फी काढून स्टेटस ठेव!", "कोणीतरी फनी गाणं गा!", "एखाद्याला 'आय लव्ह यू' मेसेज कर!", "१० वेळा गोल फिरून दाखव!"]
        };

        function generate(type) {
            let name = document.getElementById('name').value || "दोस्ता";
            let p1 = parts[type][Math.floor(Math.random() * parts[type].length)];
            let p2 = parts[type + "_end"][Math.floor(Math.random() * parts[type + "_end"].length)];
            document.getElementById('result').innerText = name + ", " + p1 + " " + p2;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
