from linebot import LineBotApi
from linebot.models import (
    TextSendMessage,
)
import settings
import scraping


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def main():
    '''
    Parameters
    ----------
    user_id : string
        LINEのユーザーID
    elms_id : string
        ELMSの学生ID
    elms_password : string
        ELMSのパスワード
    num_of_post : int
        1時間以内に投稿された数
    error_message : string
        スクレイピング時に発生したエラーメッセージ 
    '''
    user_id = settings.LINE_USER_ID 
    elms_id = settings.ELMS_STUDENT_ID
    elms_password = settings.ELMS_PASSWORD
    num_of_post = 0
    
    try:
        # 実際のスクレイプを行う処理
        elms = scraping.ScrapeElms(elms_id, elms_password)
        elms.login()
        elms.choose_dropdown_list(2) #グループに関するお知らせのドロップダウンを選択
        elms.get_time_list() #時間一覧を取得
        num_of_post = elms.count_message() # 1時間以内に投稿された数を返す
        elms.close_browser()

    except Exception as e: #スクレイプ中に起きたエラーは全てここで受ける
        error_message = "エラーが発生したようです．\n内容は以下です．\n---------{}\n---------".format(str(e))
        print(error_message)
        line_bot_api.push_message(user_id, messages=TextSendMessage(text=error_message))
        return

    ## LINEにpushする処理
    # メッセージを作る処理を追加する
    # error_messageが空でない場合はerrorメッセージをLINE側に送ってほしいです．
    # (空で初期化しているので送るテキストに連結して貰うだけでもいいかもです)

    
    if num_of_post > 0:
        print("メッセージが届いたよ!")
        messages = TextSendMessage(text=f"ELMSに{num_of_post}件のメッセージが届いたよ!https://www.hokudai.ac.jp/gakusei/instruction-info/elms/")
        line_bot_api.push_message(user_id, messages=messages)
    else:
        print("新着メッセージがないよ！")
