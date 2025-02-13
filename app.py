from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 從環境變數中獲取 Channel Secret 和 Channel Access Token
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
line_handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 設定 /callback 路徑來接收 LINE Webhook
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        # 驗證來自 LINE 的訊息
        line_handler.handle(body, signature)
    except Exception as e:
        print(f"Error: {e}")
        abort(400)

    return 'OK'

# 當收到訊息事件時回應
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    # 回應用戶發送的訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f'你說: {user_message}')
    )

# Vercel 要求的入口點
def vercel_main(req, res):
    with app.wsgi_app:
        return app.full_dispatch_request()
