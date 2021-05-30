
# AutoShoutout twitch chatbot

* TwitchIO   : Version 1.1.0

## 1. 概要

* 配信に来た人の初回のチャットをwaveファイルを再生して通知します。
* (withShoutoutだけ) Raidを検知してシャウトアウトを自動でコメントします。
* (withShoutoutだけ) !soコマンドでシャウトアウトメッセージをコメントします。


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

```
TMI_TOKEN=oauth:aabbccddeeffgg0011223344556677
CLIENT_ID=0123456789abcdefghijklmnopqrst
BOT_NICK=botchannelname
BOT_PREFIX=!
CHANNEL=#loginchannelname
```


## 4. 実行ファイルと必要ファイル

1. 本体 (doorbellbot.exe)
   DoorbellBot と DoorbellBot_withShoutout のどちらかのディレクトリにある doorbellbot.exe が本体です。
   それぞれ以下のように使い分けてください。

   DoorbellBot：botを起動してから初回チャットの人がいたときに音を鳴らします。
   DoorbellBot_withShoutout：上記に加えて自動so/soコマンド機能が追加されています。
   
2. 本体と同じディレクトリに beep.wav と 手順3で用意した .env を配置してください。
   beep.wav は初回チャット時のSEになります。
   raidbeep.wav はRAID検知時のSEになります。
   
3. 本体と同じディレクトリにある raidmessage.txt を編集することで、
   シャウトアウトのメッセージが変更できます。詳細は同ファイルを確認してください。


## 5. 起動

* doorbellbot.exe をダブルクリックしてください。


---