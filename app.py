from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import subprocess

app = Flask(__name__)


MONGO_URI = "mongodb+srv://siddhunioh7:admin@clusters0.pwmqglw.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.get_database("sid")
collection = db.get_collection("trending_topics")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run-script", methods=["POST"])
def run_script():
    subprocess.run(["python", "selenium_script.py"])
    return jsonify({"message": "Script executed successfully"})

@app.route("/get-trends")
def get_trends():
    data = collection.find_one(sort=[("datetime", -1)])  
    if not data:
        return jsonify({"message": "No trends available yet."})
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
