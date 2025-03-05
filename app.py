from flask import Flask , render_template , request , jsonify
from flask_cors import CORS
import google.generativeai as genai


app = Flask(__name__)
CORS(app)
genai.configure(api_key="AIzaSyAvyLEzkIaibw5BFF4ZCISLljZNbLKd2Cg")
model = genai.GenerativeModel("gemini-2.0-flash")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/use")
def use():
    return render_template("index.html")

@app.route("/apiDocs")
def Docs():
    return render_template("docs.html")

@app.route("/chat" , methods=["POST"])
def chat():
    user_meassage = request.form["meassage"]
    ai_res = model.generate_content(user_meassage)
    return render_template("index.html" , chat=str(ai_res.text))


@app.route("/api/ramAI/chat/content/<prompt>")
def api(prompt):
    if(prompt==" "):
        return jsonify("MUST PROVIDE THE PROMPT") , 404
    else:
          res = model.generate_content(prompt)
          return jsonify(res.text)
        
  

if __name__ == "__main__":
    app.run(debug=True)
