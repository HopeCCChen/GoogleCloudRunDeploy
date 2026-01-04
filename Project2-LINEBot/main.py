import os
import sys
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 初始化 Flask 應用程式
app = Flask(__name__)

# 從環境變數中讀取 LINE Bot 的設定
# 在 Cloud Run 部署時，我們會在環境變數中設定這些值，避免將金鑰直接寫在程式碼裡
CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN', '你的_CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET', '你的_CHANNEL_SECRET')

if CHANNEL_ACCESS_TOKEN is None or CHANNEL_SECRET is None:
    print("錯誤: 請設定 CHANNEL_ACCESS_TOKEN 與 CHANNEL_SECRET 環境變數")
    sys.exit(1)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # 取得 X-Line-Signature 標頭值 (用於驗證訊息是否真的來自 LINE)
    signature = request.headers['X-Line-Signature']

    # 取得 Request Body
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 處理 Webhook Body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 如果簽章驗證失敗，回傳 400 錯誤
        abort(400)

    return 'OK'

# 處理訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 取得使用者傳送的文字
    user_text = event.message.text
    
    # 這裡實作簡單的 Echo (回聲) 功能，你可以在這裡修改邏輯
    # 例如：串接 Gemini API、查詢資料庫等
    reply_text = f"你剛才說了：{user_text}"

    # 回覆訊息給使用者
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    # Cloud Run 會將 Port 寫入環境變數 PORT，預設為 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)