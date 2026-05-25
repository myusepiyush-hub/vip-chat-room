from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Fun Zone</title>
    <style>
        body { 
            margin: 0; padding: 0; background-color: #000; font-family: 'Arial', sans-serif; 
            display: flex; justify-content: center; align-items: center; min-height: 100vh; overflow: hidden;
        }
        .background-icon { position: absolute; font-size: 300px; opacity: 0.1; z-index: 0; user-select: none; }
        .box { 
            background: rgba(20, 20, 20, 0.95); padding: 30px; border-radius: 25px; 
            border: 2px solid #ff0055; width: 90%; max-width: 400px; 
            box-shadow: 0 0 40px #ff0055; text-align: center; z-index: 1;
        }
        input { padding: 12px; width: 85%; border-radius: 8px; border: none; margin-bottom: 20px; background: #333; color: white; text-align: center;}
        .btn { padding: 12px; width: 100%; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; margin-bottom: 10px; color: white; }
        .roast { background: #ff0055; }
        .love { background: #00d4ff; color: white; }
        .task { background: #70ff00; color: #000; }
        #result { margin-top: 20px; font-size: 1.2em; color: #fff; min-height: 50px; }
        
        /* मोठे नाव स्टाईल */
        .creator-name { 
            margin-top: 30px; color: #ff0055; font-size: 24px; text-transform: uppercase; 
            text-shadow: 0 0 10px #ff0055; font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="background-icon">🖕</div>
    <div class="box">
        <h2 style="color: white;">🔥 Infinite Fun Zone 🔥</h2>
        <input type="text" id="name" placeholder="तुमचं नाव टाका...">
        <button class="btn roast" onclick="generate('roast')">Roast Me! 💀</button>
        <button class="btn love" onclick="generate('love')">Love Quote ❤️</button>
        <button class="btn task" onclick="generate('task')">Give Me Task 🎯</button>
        <div id="result"></div>
        
        <!-- मोठे नाव -->
        <h2 class="creator-name">Created by Piyush Patil</h2>
    </div>

    <script>
        function generate(type) {
            let name = document.getElementById('name').value || "दोस्ता";
            let msgs = {
                roast: ["तू आरशात बघितला की आरसा पण घाबरून फुटतो!", "तुझं डोकं आणि रिकामी जागा यात जास्त फरक नाही!", "निसर्गाची एक मोठी चूक म्हणजे तू!"],
                love: ["तू जगातील सर्वात स्पेशल व्यक्ती आहेस!", "तुझं हसणं खूप गोड आहे!", "तू आयुष्यात आहेस म्हणून बहार आहे!"],
                task: ["५ मिनिटे शांत बसून दाखव!", "कोणाला तरी कॉल करून आय मिस यू म्हण!", "१० वेळा उठ-बैठ कर!"]
            };
            let res = msgs[type][Math.floor(Math.random() * msgs[type].length)];
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
"""

आता तुझी वेबसाईट एकदम कडक आणि प्रोफेशनल दिसेल! ही आयडिया तुला आवडली का?
