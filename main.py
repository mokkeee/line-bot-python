from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
from argparse import ArgumentParser

app = Flask(__name__)

# 環境変数取得
# LINE Developersで設定されているチャネルアクセストークンとチャネルシークレットを設定
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route("/callback", methods=['POST'])
def callback():
    """
    Webhookからのリクエストの正当性をチェックし、ハンドラに応答処理を移譲する
    """

    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        Handler.handle(body, signature)
    # 署名検証で失敗した場合、例外を出す。
    except InvalidSignatureError:
        app.logger.warn("Invalid Signature.")
        abort(400)
    # handleの処理を終えればOK
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    LINEへのテキストメッセージに対して応答を返す

    Parameters
    ----------
    event: MessageEvent
      LINEに送信されたメッセージイベント
    """

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="応答です。 " + event.message.text))


if __name__ == "__main__":
    # app.run()
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int,
                            default=int(os.environ.get('PORT', 8000)), help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    arg_parser.add_argument('--host', default='0.0.0.0', help='host')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, host=options.host, port=options.port)
