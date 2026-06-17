from flask import Flask, request
import requests
import os
from supabase import create_client

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}/sendMessage"


def send_message(chat_id, text):
    requests.post(API_URL, json={
        "chat_id": chat_id,
        "text": text
    })


def add_member(group_id, user_id, username):

    group_id = str(group_id)

    existing = supabase.table("members") \
        .select("user_id") \
        .eq("group_id", group_id) \
        .eq("user_id", user_id) \
        .execute()

    if existing.data:
        return

    supabase.table("members").insert({
        "group_id": group_id,
        "user_id": user_id,
        "username": username
    }).execute()


def get_members(group_id):
    res = supabase.table("members") \
        .select("username") \
        .eq("group_id", str(group_id)) \
        .execute()

    return [row["username"] for row in res.data]


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    message = data.get("message", {})
    text = message.get("text", "")
    username = message.get("from", {}).get("username")
    user_id = message.get("from", {}).get("id")
    chat_id = message.get("chat", {}).get("id")

    if not chat_id:
        return "ok"

    group_id = str(chat_id)

    if username and user_id:
        add_member(group_id, user_id, f"@{username}")


    if text == "@all":
        members = get_members(group_id)

        if not members:
            send_message(group_id, "لیست اعضا خالیه 😐")
        else:
            send_message(group_id, "👥 اعضای گروه:\n" + " ".join(members))

    return "ok"


@app.route("/")
def home():
    return "Bot is running with Supabase..."
