from linebot import LineBotApi
from linebot.models import (
    TextSendMessage,
)
import settings
import scraping


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def main():
    user_id = settings.LINE_USER_ID 
    elms_id = settings.ELMS_STUDENT_ID
    elms_password = settings.ELMS_PASSWORD
    

    ## scraping.pyのScrapeElmsクラスのインスタンスを作成してスクレイプを行う処理
    elms = scraping.ScrapeElms(elms_id, elms_password)
    elms.login()
    elms.choose_dropdown_list(2) #グループに関するお知らせのドロップダウンを選択
    times_list = elms.get_time_list() #時間一覧を取得
    print("\n############ 時間一覧 ############\n times_list", times_list)
    num_of_post = elms.count_messege() # 1時間以内に投稿された数

    elms.close_browser()

    ## LINEにpushする処理
    #メッセージを作る処理を追加する 
    messages = TextSendMessage(text=f"ボボボーボ・ボーボボ")
    line_bot_api.push_message(user_id, messages=messages)


if __name__ == "__main__":
    main()