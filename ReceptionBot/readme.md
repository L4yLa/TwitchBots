
# Reception twitch chatbot

* TwitchIO   : Version 1.1.0

## 1. 概要

* 配信に来た人の初回のチャットをwaveファイルを再生して通知します。


## 2. 前提環境

* Python 3.6 以降
  → https://www.python.org/

* pipenv
  → $ pip install pipenv


## 3. 必要情報の設定

1. OAuthパスワードの作成
   → https://twitchapps.com/tmi/

2. Twitch Developersでアプリケーションを登録してクライアントIDを取得
   → https://dev.twitch.tv/

3. .envファイルに必要情報を記入

BOT_NICK には(1,2)で取得したアカウントのチャンネル名を入力してください。
CHANNEL にはbotを使用したいチャンネル名を入力してください。

以下のようになります：

--.env-->
```
TMI_TOKEN=oauth:aabbccddeeffgg0011223344556677
CLIENT_ID=0123456789abcdefghijklmnopqrst
BOT_NICK=botchannelname
BOT_PREFIX=!
CHANNEL=#loginchannelname
```
<--.env--


## 4. 起動

* startbot.batを実行してください。
* run startbot.bat


---