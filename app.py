from flask import Flask , render_template , request , jsonify
from flask_cors import CORS
import google.generativeai as genai
from pymongo import MongoClient
import datetime
import requests

app = Flask(__name__)
CORS(app)
genai.configure(api_key="AIzaSyAvyLEzkIaibw5BFF4ZCISLljZNbLKd2Cg")

model = genai.GenerativeModel("gemini-2.0-flash")


client = MongoClient("mongodb+srv://sriram65raja:1324sriram@cluster0.dejys.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["ai"] 
chat_collection = db["UserChats"]  
api_db = db["APILogs"]
Code = db["UserCode"]

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
    user_ip = request.headers.get("X-Forwarded-For" , request.remote_addr)
    chat_data = {
        "UserMeassage":user_meassage,
        "AI_Response": ai_res.text,
        "user_ip" : user_ip,
        "Time":datetime.datetime.today()
    }
    chat_collection.insert_one(chat_data)
    return render_template("index.html" , chat=str(ai_res.text))



@app.route("/api/ramAI/chat/<prompt>")
def api(prompt):
         res = model.generate_content(prompt)
         api_ip = request.headers.get("X-Forwarded-For" , request.remote_addr)
         api_data = {
             "meassage" : prompt,
             "ai_resp" : res,
             "Api" : api_ip
         }
         api_db.insert_one(api_data)
         return jsonify(res.text)


key = "1324meta"
@app.route("/api/db/users/<password>/get" , methods=["GET"])
def chat_find(password):
    if(password == key):
         collect = list(chat_collection.find({} , {"_id" : 0}))
         return  jsonify(collect)
    else:
        return "Password Wrong !"
    
@app.route("/fetch")
def serach():
    query = request.args.get("q")
    res = requests.get(query)
    try:
        if res.status_code == 200:
            user_code={
                "Url" : query
            }
            Code.insert_one(user_code)
            return jsonify(res.text) 

    except:
        return jsonify("unable to Fetch")
    
    
@app.route("/dbcode")
def dbcode():
    cdb = list(Code.find({} , {"_id" : 0}))
    return jsonify(cdb)
    


if __name__ == "__main__":
    app.run(debug=True)
