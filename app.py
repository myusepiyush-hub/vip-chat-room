from flask import Flask, render_template_string, request

app = Flask(__name__)

# हे एक साधे लॉजिक आहे, इथे आपण 'AI API' कनेक्ट करू
def get_ai_response(user_input, age_group):
    if age_group == "18+":
        return f"तुम्ही परिपक्व आहात, म्हणून मी तुमच्याशी अधिक खुल्या विचारांनी बोलू शकतो. तुम्ही म्हणालात: {user_input}"
    else:
        return f"मी तुमचा एक चांगला मित्र आहे! आपण काहीतरी मजेशीर बोलूया का? तुम्ही म्हणालात: {user_input}"

@app.route('/', methods=['GET', 'POST'])
def chat():
    response = ""
    if request.method == 'POST':
        user_msg = request.form.get('msg')
        age = request.form.get('age')
        response = get_ai_response(user_msg, age)
    return render_template_string("""
        <form method="POST">
            <select name="age"><option>General</option><option>18+</option></select>
            <input type="text" name="msg" placeholder="काहीतरी बोला...">
            <button type="submit">Send</button>
        </form>
        <h3>AI: {{ response }}</h3>
    """, response=response)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
