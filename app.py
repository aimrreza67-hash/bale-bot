from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)


BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}/sendMessage"

DB_FILE = "db.json"



def load_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)


db = load_db()



def add_member(group_id, username):
    group_id = str(group_id)

    if group_id not in db:
        db[group_id] = {"members": []}

    if username not in db[group_id]["members"]:
        db[group_id]["members"].append(username)
        save_db(db)



def send_message(chat_id, text):
    if not BOT_TOKEN:
        print("BOT_TOKEN not set!")
        return

    requests.post(API_URL, json={
        "chat_id": chat_id,
        "text": text
    })


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    message = data.get("message", {})
    text = message.get("text", "")
    username = message.get("from", {}).get("username")
    chat_id = message.get("chat", {}).get("id")

    if not chat_id:
        return "ok"

    group_id = str(chat_id)

   
    if username:
        add_member(group_id, f"@{username}")

 
    if text == "@all":
        members = db.get(group_id, {}).get("members", [])

        if not members:
            send_message(group_id, "لیست اعضا خالیه 😐")
        else:
            send_message(group_id, "👥 اعضای گروه:\n" + " ".join(members))

    return "ok"



@app.route("/")
def home():
    return "Bot is running"
