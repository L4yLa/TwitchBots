
# Reception twitch chatbot

* TwitchIO   : Version 1.1.0

## 1. Summary

* Play wave file when new viewers on a stream come to your chat.


## 2. Requirements

* Python 3.6 or higher
  Å® https://www.python.org/

* pipenv
  Å® $ pip install pipenv


## 3. ïKóvèÓïÒÇÃê›íË : 

1. Create OAuth password
   Å® https://twitchapps.com/tmi/

2. Register app on Twitch Developers and get ClientID
   Å® https://dev.twitch.tv/

3. Fill out the .env file with the required information

Enter the channel name of the account you got at (1,2) in BOT_NICK.
Enter the channel name of the channel you want to use the bot for in CHANNEL.

Fill out like this:

```
TMI_TOKEN=oauth:aabbccddeeffgg0011223344556677
CLIENT_ID=0123456789abcdefghijklmnopqrst
BOT_NICK=botchannelname
BOT_PREFIX=!
CHANNEL=#loginchannelname
```


## 4. Startup

* double click 'Run_Receptionbot' shortcut.


---