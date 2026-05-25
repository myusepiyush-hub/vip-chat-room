from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Ultimate Fun Zone</title>
    <style>
        body { background: #0a0a0a; color: #fff; text-align: center; font-family: 'Arial', sans-serif; padding: 20px; }
        .box { background: #1a1a1a; padding: 30px; border-radius: 20px; border: 2px solid #ff0055; display: inline-block; width: 90%; max-width: 400px; box-shadow: 0 0 20px #ff0055; }
        input { padding: 12px; width: 85%; border-radius: 10px; border: none; margin-bottom: 20px; background: #333; color: white; }
        .btn-group { display: flex; flex-direction: column; gap: 10px; }
        button { padding: 12px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; color: white; transition: 0.3s; }
        button:hover { transform: scale(1.05); }
        .roast { background: #ff0055; }
        .love { background: #00d4ff; }
        .task { background: #70ff00; color: #000; }
        #result { margin-top: 25px; font-size: 1.2em; min-height: 80px; color: #ffeb3b; padding: 15px; border-top: 1px solid #444; }
    </style>
</head>
<body>
    <h1>🔥 Fun Zone 🔥</h1>
    <div class="box">
        <input type="text" id="name" placeholder="तुमचं नाव टाका...">
        <div class="btn-group">
            <button class="roast" onclick="show('roast')">Roast Me! 💀</button>
            <button class="love" onclick="show('love')">Love Quote ❤️</button>
            <button class="task" onclick="show('task')">Give Me Task 🎯</button>
        </div>
        <div id="result">येथे रिझल्ट दिसेल...</div>
    </div>

    <script>
        function show(type) {
            let name = document.getElementById('name').value || "दोस्ता";
            let data = {
                roast: [
                    "तुला बघून वाटतं निसर्गाने काहीतरी भलतंच बनवलंय!", 
                    "तू आरशात बघितला की आरसा पण घाबरून फुटून जातो!",
                    "तुझं डोकं आणि रिकामी जागा यात जास्त फरक नाहीये.",
                    "तू कॉमेडी शोमध्ये जाण्याची गरज नाही, तुझा चेहराच पुरेसा आहे!",
                    "देवाने तुला बनवताना ओव्हरटाइम केला होता आणि शेवटी कंटाळून सोडून दिलं!",
                    "तुझ्यापेक्षा चांगला मेंदू तर एका वाळलेल्या कांद्याला असेल!"
                ],
                love: [
                    "प्रेम म्हणजे एका दुखाचा सुखावणारा अनुभव आहे!", 
                    "तू कितीही रागवलास तरी तुझं मन सोन्यासारखं आहे!",
                    "तुला बघितलं की चेहऱ्यावर आपोआप हसू येतं!",
                    "आयुष्यात तू आहेस म्हणून सगळं काही सुंदर वाटतं.",
                    "तुझा स्वभाव एखाद्या सुंदर गाण्यासारखा आहे, जे कधीच संपू नये!",
                    "तू जगातील सर्वात स्पेशल व्यक्ती आहेस, हे लक्षात ठेव!"
                ],
                task: [
                    "पुढच्या ५ मिनिटात एक सेल्फी काढून स्टेटस ठेव!", 
                    "कोणाला तरी कॉल करून 'आय मिस यू' म्हण!",
                    "एखादं फनी गाणं गाऊन व्हिडिओ बनवून टाक!",
                    "पुढचे १० मिनिटे कोणाशीही न बोलता शांत बसून दाखव!",
                    "तुझ्या क्रशचा फोटो बघून ३ वेळा 'आय लव्ह यू' म्हण!",
                    "एका कागदावर 'मी बेस्ट आहे' असं लिहून आरशासमोर धर!"
                ]
            };
            let arr = data[type];
            let res = arr[Math.floor(Math.random() * arr.length)];
            document.getElementById('result').innerText = name + ", " + res;
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
