
# AutoShoutout twitch chatbot

* TwitchIO   : Version 1.1.0

## 1. �T�v

* �z�M�ɗ����l�̏���̃`���b�g��wave�t�@�C�����Đ����Ēʒm���܂��B
* (withShoutout����) Raid�����m���ăV���E�g�A�E�g�������ŃR�����g���܂��B
* (withShoutout����) !so�R�}���h�ŃV���E�g�A�E�g���b�Z�[�W���R�����g���܂��B


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

```
TMI_TOKEN=oauth:aabbccddeeffgg0011223344556677
CLIENT_ID=0123456789abcdefghijklmnopqrst
BOT_NICK=botchannelname
BOT_PREFIX=!
CHANNEL=#loginchannelname
```


## 4. ���s�t�@�C���ƕK�v�t�@�C��

1. �{�� (doorbellbot.exe)
   DoorbellBot �� DoorbellBot_withShoutout �̂ǂ��炩�̃f�B���N�g���ɂ��� doorbellbot.exe ���{�̂ł��B
   ���ꂼ��ȉ��̂悤�Ɏg�������Ă��������B

   DoorbellBot�Fbot���N�����Ă��珉��`���b�g�̐l�������Ƃ��ɉ���炵�܂��B
   DoorbellBot_withShoutout�F��L�ɉ����Ď���so/so�R�}���h�@�\���ǉ�����Ă��܂��B
   
2. �{�̂Ɠ����f�B���N�g���� beep.wav �� �菇3�ŗp�ӂ��� .env ��z�u���Ă��������B
   beep.wav �͏���`���b�g����SE�ɂȂ�܂��B
   raidbeep.wav ��RAID���m����SE�ɂȂ�܂��B
   
3. �{�̂Ɠ����f�B���N�g���ɂ��� raidmessage.txt ��ҏW���邱�ƂŁA
   �V���E�g�A�E�g�̃��b�Z�[�W���ύX�ł��܂��B�ڍׂ͓��t�@�C�����m�F���Ă��������B


## 5. �N��

* doorbellbot.exe ���_�u���N���b�N���Ă��������B


---