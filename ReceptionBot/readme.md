
# Reception twitch chatbot

* TwitchIO   : Version 1.1.0

## 1. �T�v

* �z�M�ɗ����l�̏���̃`���b�g��wave�t�@�C�����Đ����Ēʒm���܂��B


## 2. �O���

* Python 3.6 �ȍ~
  �� https://www.python.org/

* pipenv
  �� $ pip install pipenv


## 3. �K�v���̐ݒ�

1. OAuth�p�X���[�h�̍쐬
   �� https://twitchapps.com/tmi/

2. Twitch Developers�ŃA�v���P�[�V������o�^���ăN���C�A���gID���擾
   �� https://dev.twitch.tv/

3. .env�t�@�C���ɕK�v�����L��

BOT_NICK �ɂ�(1,2)�Ŏ擾�����A�J�E���g�̃`�����l��������͂��Ă��������B
CHANNEL �ɂ�bot���g�p�������`�����l��������͂��Ă��������B

�ȉ��̂悤�ɂȂ�܂��F

--.env-->
```
TMI_TOKEN=oauth:aabbccddeeffgg0011223344556677
CLIENT_ID=0123456789abcdefghijklmnopqrst
BOT_NICK=botchannelname
BOT_PREFIX=!
CHANNEL=#loginchannelname
```
<--.env--


## 4. �N��

* startbot.bat�����s���Ă��������B
* run startbot.bat


---