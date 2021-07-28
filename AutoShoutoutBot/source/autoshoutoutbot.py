import os
import re
import threading
import asyncio
import simpleaudio
import requests
from string import Template
from os.path import join, dirname
from dotenv import load_dotenv
from twitchio.ext import commands

SOUND = True	# 音声ファイル再生を使用する

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

bot = commands.Bot(
	irc_token = os.environ['TMI_TOKEN'],
	client_id = os.environ['CLIENT_ID'],
	nick      = os.environ['BOT_NICK'],
	prefix    = os.environ['BOT_PREFIX'],
	initial_channels = [os.environ['CHANNEL']],
)

class ChatbotStorage:
	def __init__(self):
		self.fQuit = bool
		self.ready = bool
		self.channel = None
		self.threads = [None, None, None, None, None]
		self.so_args = ["", "", "", "", ""]
		self.raidmsg = ""
		self.aduser = None
		self.addone = []
	
	def getUIDfromName(self, name):
		if name == "":
			return None
		r = requests.get('https://api.twitch.tv/helix/users?login=' + name, headers=self.header)
		if r.status_code == requests.codes.ok:
			if len(r.json()['data']) > 0:
				return r.json()['data'][0]['id']
		return None

	def getChannelInfo(self, cid):
		if cid == None:
			return None
		r = requests.get('https://api.twitch.tv/helix/channels?broadcaster_id=' + cid, headers=self.header)
		if r.status_code == requests.codes.ok:
			if len(r.json()['data']) > 0:
				return r.json()['data'][0]

	def sendShoutout(self, uid, uname=""):
		ci = dat.getChannelInfo(dat.getUIDfromName(uid))
		if ci == None:
			eventloop.create_task(dat.channel.send("[shoutout] 不明なユーザー名です"))
		else:
			if ci['broadcaster_name'] != uid:
				name = ci['broadcaster_name'] + "(" + uid + ")"
			else:
				name = uid
			eventloop.create_task(dat.channel.send(dat.raidmsg.format(NAME=name, CATEGORY=ci['game_name'], TITLE=ci['title'], ID=uid)))
	
	def isAdtarget(self, uid):
		if not uid in self.addone:
			if uid in self.aduser:
				return True
		return False
	
	def AdDone(self, uid):
		if not uid in self.addone:
			self.addone.append(uid)


dat = ChatbotStorage()
gBeep = simpleaudio.WaveObject.from_wave_file("beep.wav") # 通知音:New-viewer notification sound
channelname = os.environ['CHANNEL'].replace('#', '')
botname = os.environ['BOT_NICK']

def is_admin(ctx):
	if ctx.author.name == channelname:
		return True
	if ctx.author.is_mod:
		return True
	return False

@bot.event
async def event_ready():
	print(f"Bot {botname} is ready.")
	dat.ready = True

@bot.event
async def event_raw_data(data):
	if dat.ready:
		
		# Raid Detection
		if not "PRIVMSG" in data:
			if "USERNOTICE" in data and "msg-id=raid" in data:
				mname = re.search('msg-param-displayName\=(.+?);', data)
				mvcnt = re.search('msg-param-viewerCount\=([0-9]+?);', data)
				mid   = re.search('msg-param-login\=(.+?);', data)
				if mname.group(1) == mid.group(1):
					print("[RAID] " + mname.group(1) + " raiding with " + mvcnt.group(1) + " viewers!!")
				else:
					print("[RAID] " + mname.group(1) + "(" + mid.group(1) + ") raiding with " + mvcnt.group(1) + " viewers!!")
				
				if dat.channel != None:
					dlytime = 0.0
					for idx in range(5):
						if dat.threads[idx] == None or dat.threads[idx].is_alive() == False:
							rn = int(mvcnt.group(1))
							dlytime = 45.0 * (rn / (30.0 + abs(rn)))
							dat.so_args[idx] = mid.group(1)
							dat.threads[idx] = threading.Timer(dlytime, dat.sendShoutout, args=(dat.so_args[idx],))
							dat.threads[idx].start()
							break
					if dlytime > 30.0:
						dat.sendShoutout(mid.group(1), mname.group(1))
				
				simpleaudio.stop_all()
				gBeep.play()


# Shoutoutするcommand
@bot.command(name='shoutout', aliases=['so'])
async def shoutout_command(ctx, *arg):
	if not is_admin(ctx):
		return
	dat.sendShoutout(arg[0])

# botを終了するcommand
@bot.command(name='quit', aliases=['q'])
async def quit_command(ctx):
	if not is_admin(ctx):
		return
	dat.fQuit = True
	# bot.close() # will be impliment on TwitchIO 2.0
	exit()

# 通知音を鳴らすcommand
@bot.command(name='beep', aliases=['call', 'help'])
async def beep_command(ctx):
	if not is_admin(ctx):
		return
	simpleaudio.stop_all()
	gBeep.play()

#
#  messages
# 
@bot.event
async def event_message(message):
	if dat.fQuit:
		# bot.close() # will be impliment on TwitchIO 2.0
		exit()
	if dat.channel == None:
		dat.channel = message.channel
	
	if dat.isAdtarget(message.author.name):
		dat.sendShoutout(message.author.name)
		dat.AdDone(message.author.name)
	
	# If you override event_message you will need to handle_commands for commands to work.
	await bot.handle_commands(message)

def interpreter():
	while(not dat.fQuit):
		cmd = input()
		if cmd.lower() in {"quit", "q"}:
			if not dat.fQuit:
				dat.fQuit = True
				print("Quit Bot")
			break
		if cmd.lower() in {"user"}:
			u = input("user?>")
			ts = os.environ['TMI_TOKEN'].replace("oauth:", "Bearer ")
			h = {
				'client-id': os.environ['CLIENT_ID'],
				'Authorization': ts,
			}
			print(h)
			r = requests.get('https://api.twitch.tv/helix/users?login=' + u, headers=h)
			print(r.text)
		elif cmd != "":
			print("[CONSOLE]", cmd, "is invalid command.")
	print("interpreter end.")

if __name__ == "__main__":
	# init
	dat.ready = False
	dat.fQuit = False
	dat.channel = None

	rmsg = ""
	if os.path.isfile('raidmessage.txt'):
		with open('raidmessage.txt', 'r') as fd:
			rmsg = fd.readline()
	
	if rmsg == "":
		dat.raidmsg = '§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§  - - - - - Please check this awesome streamer!! - - - - - - この素晴らしい配信者もチェックしてください！ - -  {NAME} : https://twitch.tv/{ID} 最近の配信 Recent stream : {CATEGORY} - {TITLE}  §=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§'
	else:
		dat.raidmsg = rmsg
	
	print("Raid Message:" + dat.raidmsg)

	if os.path.isfile('adlist.txt'):
		with open('adlist.txt', 'r') as fd:
			dat.aduser = fd.read().splitlines()
	else: 
		dat.aduser = ['',]
	
	print("Shoutout User:", end='')
	print(dat.aduser)


	# Get CID for Twitch API
	th = {'Authorization': 'OAuth ' + os.environ['TMI_TOKEN'].replace('oauth:', '') }
	#	print('[TEMP HEADER]', th)
	r = requests.get('https://id.twitch.tv/oauth2/validate', headers=th)
	#	print('[GET CID]', r.json()['client_id'])
	dat.header = {
		'Authorization': 'Bearer '+ os.environ['TMI_TOKEN'].replace('oauth:', ''),
		'Client-ID': r.json()['client_id'],
	}
	#	print('[HEADER]', dat.header)
	
	print("--- Twitch API TEST ---")
	print('[USERNAME]', channelname)
	uid = dat.getUIDfromName(channelname)
	print('[GET USER CID]', uid)
	cinfo = dat.getChannelInfo(uid)
	print('[GET CATEGORY]', cinfo['game_name'])
	print('[GET TITLE]', cinfo['title'])
	print("--- Twitch API TEST END ---")

	t = threading.Thread(target=bot.run)
	eventloop = asyncio.get_event_loop()

	# run
	t.start()
	interpreter()
	t.join()
