from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Roast & Dare Hub</title>
    <style>
        body { background: #000; color: #fff; text-align: center; font-family: 'Arial', sans-serif; padding: 30px; }
        .container { background: #1a1a1a; padding: 20px; border-radius: 15px; border: 2px solid #ff4d4d; display: inline-block; width: 90%; max-width: 400px; }
        input { padding: 10px; width: 80%; border-radius: 5px; border: none; margin-bottom: 10px; }
        button { padding: 12px 20px; background: #ff4d4d; color: white; border: none; cursor: pointer; border-radius: 5px; font-weight: bold; }
        #result { margin-top: 20px; font-size: 1.2em; color: #ffeb3b; padding: 10px; min-height: 50px; }
    </style>
</head>
<body>
    <h1>💀 Roast & Dare 💀</h1>
    <div class="container">
        <input type="text" id="name" placeholder="तुमचं नाव टाका...">
        <br>
        <button onclick="getRandom()">सांगा माझं काय होईल?</button>
        <div id="result"></div>
    </div>

    <script>
        function getRandom() {
            let name = document.getElementById('name').value;
            if(!name) { alert("नाव टाका!"); return; }
            
            let actions = [
                "रोस्ट: तू आरशात बघितला की आरसा पण विचार करतो, 'हे काय बघायला लागलो मी!'",
                "रोस्ट: तू कॉमेडी शोमध्ये जाण्याची गरज नाही, तुझा चेहराच पुरेसा आहे!",
                "डेअर: पुढील १० मिनिटे कोणाशीही बोलू नकोस, करून दाखव!",
                "डेअर: तुझ्या क्रशला 'आय लव्ह यू' चा मेसेज कर आणि स्क्रीनशॉट पाठव!",
                "डेअर: एक गाणे गाऊन त्याचा व्हिडिओ स्टोरीला ठेव!",
                "रोस्ट: तुझ्याकडे बघून असं वाटतं की देवाने तुला बनवताना ओव्हरटाइम केला होता!"
            ];
            
            let randomAction = actions[Math.floor(Math.random() * actions.length)];
            document.getElementById('result').innerText = name + ", " + randomAction;
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
