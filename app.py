from flask import Flask , render_template , request , jsonify
from flask_cors import CORS
import google.generativeai as genai
from pymongo import MongoClient
import datetime

app = Flask(__name__)
CORS(app)
genai.configure(api_key="AIzaSyAvyLEzkIaibw5BFF4ZCISLljZNbLKd2Cg")
model = genai.GenerativeModel("gemini-2.0-flash")

client = MongoClient("mongodb+srv://sriram65raja:1324sriram@cluster0.dejys.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["ai"] 
chat_collection = db["UserChats"]  

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
    chat_data = {
        "UserMeassage":user_meassage,
        "AI_Response": ai_res.text,
        "Time":datetime.datetime.today()
    }
    chat_collection.insert_one(chat_data)
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
