import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from services.service import process_input
from flask import Flask, request

app = Flask(__name__)
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

@app.route("/slack/events", methods=["POST"])
def handle_slack_event():
    slack_event = request.json
    print(slack_event)

    if "challenge" in slack_event:
        return slack_event["challenge"]

    if "event" in slack_event:
        event = slack_event["event"]


        if "bot_id" not in event:
            text = event["text"]
            response = process_input(text)
            try:
                client.chat_postMessage(channel=event["channel"], text=response)
            except SlackApiError as e:
                print("Error posting message: {}".format(e))

    return "ok"

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)), host="0.0.0.0")
