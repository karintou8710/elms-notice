from linebot import LineBotApi
from linebot.models import (
    TextSendMessage,
)

import settings

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def main():
    user_id = settings.LINE_USER_ID
    messages = TextSendMessage(text=f"ボボボーボ・ボーボボ")
    line_bot_api.push_message(user_id, messages=messages)


if __name__ == "__main__":
    main()