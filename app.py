from flask import Flask, render_template, request, jsonify
# IMPORT BOTH FUNCTIONS HERE
from web_assist import get_response, detect_intent 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.json
        user_input = data.get("query", "")

        if not user_input:
            return jsonify({"response": "I didn't hear anything. Could you please repeat that?"})

        # 1. Detect the intent (Now imported from web_assist)
        intent = detect_intent(user_input)

        # 2. Get the string response
        bot_response = get_response(intent, user_input)

        return jsonify({"response": bot_response})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "I'm having trouble processing that right now."}), 500

if __name__ == "__main__":
    app.run(debug=True)