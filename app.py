from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: #0f0f0f; color: #ff00ff; font-family: 'Courier New', monospace; text-align: center; padding: 50px; }
        .engine { border: 3px solid #ff00ff; padding: 30px; border-radius: 25px; max-width: 500px; margin: auto; }
        .glitch-text { font-size: 24px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="engine">
        <h1>🧠 Neural Psychic Engine</h1>
        <form method="POST">
            <p>मनात १ ते १० मधील आकडा धर...</p>
            <button type="submit">मी तयार आहे, माझं मन वाचा!</button>
        </form>
        {% if result %}
            <h2 class="glitch-text">...स्कॅनिंग पूर्ण...</h2>
            <h1 style="color: #fff;">तुझ्या मनातलं उत्तर: {{ result }}</h1>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        # इथे आपण 'Random Logic' वापरतोय जेणेकरून उत्तर प्रत्येक वेळी वेगळं येईल!
        x = random.randint(5, 10)
        y = random.randint(2, 5)
        result = (x * y) + random.randint(1, 9) 
    return render_template_string(HTML, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
