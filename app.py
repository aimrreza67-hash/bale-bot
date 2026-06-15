from flask import Flask, request

app = Flask(__name__)

db = {}

@app.route("/")
def home():
    return "Bot is running"


def add_member(db, group_id, username):
    if group_id not in db:
        db[group_id] = {"members": []}

    if username not in db[group_id]["members"]:
        db[group_id]["members"].append(username)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    message = data.get("message", {})
    text = message.get("text", "")
    username = message.get("from", {}).get("username")
    group_id = message.get("chat", {}).get("id")

    print("TEXT:", text)
    print("USERNAME:", username)
    print("GROUP:", group_id)

    if group_id not in db:
        db[group_id] = {"members": []}

    if username:
        user = f"@{username}"
        if user not in db[group_id]["members"]:
            db[group_id]["members"].append(user)

    if text == "@all":
        members = db[group_id]["members"]
        print("ALL MEMBERS:", members)
        return " ".join(members)

    return "ok"
