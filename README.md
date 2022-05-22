# ELMS-notice

ELMS-notice は ELMS の新着メッセージの到着を LINE に通知してくれる BOT です。

## 使い方

1. Line Developer で新しいチャネルを作成
2. Heroku にアクセスして新たにアプリを作成
3. Heroku に buildpacks の設定
   - heroku/python
   - https://github.com/heroku/heroku-buildpack-chromedriver.git
   - https://github.com/heroku/heroku-buildpack-google-chrome.git
4. Heroku の環境変数の設定
   - LINE_CHANNEL_ACCESS_TOKEN
   - LINE_CHANNEL_SECRET
   - LINE_USER_ID
   - ELMS_STUDENT_ID
   - ELMS_PASSWORD
5. Heroku に LINE BOT アプリを push する。
   1. `git clone https://github.com/karintou8710/elms-notice`
   2. `heroku git:remote -a <app>`
   3. `git push heroku master`
   4. `heroku ps:scale clock=1`
