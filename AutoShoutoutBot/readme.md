
# AutoShoutout twitch chatbot

* TwitchIO   : Version 1.1.0

## 1. 概要

* Raidを検知してシャウトアウトを自動でコメントするbotです
* 指定したユーザーの初コメントで自動的にシャウトアウトできます。


## 2. 必要情報の設定

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



## 3. 実行ファイルと必要ファイル

1. 本体 (autoshoutoutbot.exe)
   shoutout ディレクトリにある autoshoutoutbot.exe が本体です。
   
2. 本体と同じディレクトリに beep.wav と 手順3で用意した .env を配置してください。

3. beep.wav をSEディレクトリの中から好みに応じて好きな方を配置してください。

   SE\bell\beep.wav：ドアベルSE<br>
   SE\silent\beep.wav：無音

4. 本体と同じディレクトリにある raidmessage.txt を編集することで、
   シャウトアウトのメッセージが変更できます。詳細は同ファイルを確認してください。

5. 本体と同じディレクトリにある adlist.txt を編集することで、
   コメント時に自動シャウトアウトするユーザーを指定できます（英字のユーザーIDを入力してください）。
   複数人登録したいときは改行して追加してください。
   ```
   例：
   l4yla_coop
   l4yla_bot
   ```


## 4. 起動

* autoshoutoutbot.exe をダブルクリックしてください。


---
