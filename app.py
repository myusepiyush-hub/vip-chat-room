from flask import Flask, render_template_string, request

app = Flask(__name__)

# साधा काउंटर आणि मेसेज लिस्ट (हे रिस्टार्ट केल्यावर रिसेट होईल)
stats = {"visitors": 0}
messages = []

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Fun Zone Live</title>
    <style>
        body { background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 20px; }
        .box { background: #1a1a1a; padding: 20px; border-radius: 20px; border: 1px solid #ff0055; width: 90%; max-width: 400px; margin: auto; }
        input { padding: 10px; width: 80%; border-radius: 5px; border: none; margin-bottom: 10px; }
        button { padding: 10px 20px; background: #ff0055; color: white; border: none; border-radius: 5px; cursor: pointer; }
        #live-chat { margin-top: 20px; background: #222; padding: 10px; border-radius: 10px; height: 150px; overflow-y: scroll; text-align: left; }
    </style>
</head>
<body>
    <div class="box">
        <h2>🔥 Infinite Fun Zone 🔥</h2>
        <p>Total Visitors: {{ visitors }}</p>
        
        <input type="text" id="msg" placeholder="Live मेसेज लिहा...">
        <button onclick="send()">Send</button>

        <div id="live-chat">
            {% for m in messages %}
                <p><b>User:</b> {{ m }}</p>
            {% endfor %}
        </div>
        <p style="font-size: 0.7em; margin-top: 15px;">Created by Piyush Patil</p>
    </div>

    <script>
        function send() {
            let m = document.getElementById('msg').value;
            window.location.href = "/send?m=" + m;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    stats["visitors"] += 1
    return render_template_string(HTML_PAGE, visitors=stats["visitors"], messages=messages)

@app.route('/send')
def send():
    msg = request.args.get('m')
    if msg: messages.append(msg)
    return "<script>window.location.href='/';</script>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
