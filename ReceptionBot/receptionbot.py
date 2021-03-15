import os
import re
import threading
import simpleaudio
import keyboard
import requests
from os.path import join, dirname
from dotenv import load_dotenv
from twitchio.ext import commands
from obswebsocket import obsws
from obswebsocket import requests as obsrequests

from chatbotstorage import ChatbotStorage

DEBUG = False	# チャットデバッグモード
SOUND = False	# 音声ファイル再生を使用する
USE_TAPI = True	# Twitch APIを使用する
SO_SELF = True	# シャウトアウトメッセージをこのbotで生成する

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

bot = commands.Bot(
	irc_token = os.environ['TMI_TOKEN'],
	client_id = os.environ['CLIENT_ID'],
	nick      = os.environ['BOT_NICK'],
	prefix    = os.environ['BOT_PREFIX'],
	initial_channels = [os.environ['CHANNEL']],
	webhook_server   = False
)

dat = ChatbotStorage() # bot内管理データ:bot internal manage data
gBeep = simpleaudio.WaveObject.from_wave_file("beep.wav") # 通知音:New-viewer notification sound
channelname = os.environ['CHANNEL'].replace('#', '')
botname = os.environ['BOT_NICK']

# OBS Websocket
OBSHost='localhost'
OBSPort=4444
OBSPass="password"

def is_admin(ctx):
	if ctx.author.name == channelname:
		return True
	if ctx.author.is_mod:
		return True
	return False

@bot.event
async def event_ready():
	print(f"Bot {botname} is ready.")
	bot.get_channel(channelname)
	dat.ready = True

@bot.event
async def event_raw_data(data):
	if DEBUG:
		print("[RAW]", data)

	# Raid Detection
	if not "PRIVMSG" in data:
		if "USERNOTICE" in data and "msg-id=raid" in data:
			mname = re.search('msg-param-displayName\=(.+?);', data)
			mvcnt = re.search('msg-param-viewerCount\=([0-9]+?);', data)
			mid   = re.search('msg-param-login\=(.+?);', data)
			print("[RAID]", mname.group(1), "raiding with", mvcnt.group(1), "viewers!!")
			if dat.obsConnected:
				dat.ws.call(obsrequests.SetCurrentScene("raid")) # OBS scene change
			if dat.raid_autoso:
				print("[RAID] " + mname.group(1) + "(" + mid.group(1) + ") raiding with " + mvcnt.group(1) + " viewers!!")
				if dat.channel != None:
					if SO_SELF:
						if USE_TAPI:
							ci = dat.getChannelInfo(dat.getUIDfromName(mid.group(1)))
							if ci == None:
								await dat.channel.send("[shoutout] 不明なユーザー名です")
							else:
								if ci['broadcaster_name'] != mname.group(1):
									name = ci['broadcaster_name'] + "(" + mname.group(1) + ")"
								else:
									name = mname.group(1)
								await dat.channel.send(f"§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§  - - - - - Please check this awesome streamer!! - - - - - - - この素晴らしい配信者もチェックしてください！ - -  {name} : https://twitch.tv/{mid.group(1)} 最近の配信 Recent stream : {ci['game_name']} - {ci['title']}  §=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§")
						else:
							if mname.group(1) != mid.group(1):
								name = mname.group(1) + "(" + mid.group(1) + ")"
							else:
								name = mid.group(1)
							await dat.channel.send(f"§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§  - - - - - Please check this awesome streamer!! - - - - - - - この素晴らしい配信者もチェックしてください！ - -  {name} : https://twitch.tv/{mid.group(1)}  §=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§")
					else:
						await dat.channel.send("!so " + mid.group(1))
				else:
					print("dat.channel is None.")
			if SOUND and dat.raid_beep:
				simpleaudio.stop_all()
				gBeep.play()

#
#  commands (everyone)
# 
@bot.command(name='test', aliases=['t'])
async def test_command(ctx):
	print(f'test message for {ctx.author.name}') # print something to console
	await ctx.channel.send(f'test message for {ctx.author.name}') # comment to chat

# Discordのリンクを表示するcommand
#	@bot.command(name='discord')
#	async def discord_command(ctx):
#		ctx.channel.send("Please join my discord server!! https://discord.gg/abcdwf")
#
# Twitterのリンクを表示するcommand
#	@bot.command(name='twitter')
#	async def twitter_command(ctx):
#		ctx.channel.send("Please follow my twitter!! https://twitter.com/twitter")
#
# Shoutoutするcommand
@bot.command(name='shoutout', aliases=['so'])
async def shoutout_command(ctx, *arg):
	if not is_admin(ctx):
		return
	if USE_TAPI:
		ci = dat.getChannelInfo(dat.getUIDfromName(arg[0]))
		if ci == None:
			await dat.channel.send("[shoutout] 不明なユーザー名です")
		else:
			if ci['broadcaster_name'] != arg[0]:
				name = ci['broadcaster_name'] + "(" + arg[0] + ")"
			else:
				name = arg[0]
			await dat.channel.send(f"§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§  - - - - - Please check this awesome streamer!! - - - - - - この素晴らしい配信者もチェックしてください！ - -  {name} : https://twitch.tv/{arg[0]} 最近の配信 Recent stream : {ci['game_name']} - {ci['title']}  §=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§")
	else:
		await ctx.channel.send(f"§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§  - - - - - Please check this awesome streamer!! - - - - - - この素晴らしい配信者もチェックしてください！ - -  {arg[0]} : https://twitch.tv/{arg[0]}  §=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§")


#
#  commands (system)
# 
@bot.command(name='quit', aliases=['q'])
async def quit_command(ctx):
	if not ctx.author.is_mod:
		return
	dat.fQuit = True
	# bot.close() # will be impliment on TwitchIO 2.0
	exit()

@bot.command(name='viewers')
async def viewers_command(ctx):
	if not ctx.author.is_mod:
		return
	viewerList = dat.getViewer()
	print(viewerList)

@bot.command(name='beep')
async def beep_command(ctx):
	if not ctx.author.is_mod:
		return
	if SOUND:
		simpleaudio.stop_all()
		gBeep.play()
#
#  commands (OBS integration)
# 

@bot.command(name='obsconnect', aliases=['oc'])
async def obs_connect_command(ctx):
	if not ctx.author.is_mod:
		return
	if not dat.obsConnected:
		dat.ws = obsws(OBSHost, OBSPort, OBSPass) # change as your OBS setting
		dat.ws.connect()
		dat.obsConnected = True

@bot.command(name='obsscenelist', aliases=['oscenes', 'ol', 'l'])
async def obs_scenelist_command(ctx):
	if not ctx.author.is_mod:
		return
	if dat.obsConnected:
		scenes = dat.ws.call(obsrequests.GetSceneList())
		if scenes.status:
			print("[Scenes]")
			for s in scenes.getScenes():
				print(s["name"])

@bot.command(name='obsscene', aliases=['os', 's'])
async def obs_scenechange_command(ctx, name):
	if not ctx.author.is_mod:
		return
	if dat.obsConnected:
		res = dat.ws.call(obsrequests.SetCurrentScene(name))

@bot.command(name='obsdisconnect', aliases=['odc'])
async def obs_disconnect_command(ctx):
	if not ctx.author.is_mod:
		return
	if dat.obsConnected:
		dat.ws.disconnect()
		dat.obsConnected = False

#
#  commands (Keyboard emuration for Avatar ctrl)
# 

@bot.command(name='motion', aliases=['m'])
async def motion_command(ctx, *arg):
	if not ctx.author.is_mod:
		return
	if arg[0] == "enable":
		dat.motionEN = True
	elif arg[0] == "disable":
		dat.motionEN = False
	elif arg[0] == "test":
		if dat.motionEN:
			keyboard.press_and_release(dat.motionkey)
	elif arg[0] == "q":
		dat.motionkey = arg[0]
	elif arg[0] == "w":
		dat.motionkey = arg[0]
	elif arg[0] == "e":
		dat.motionkey = arg[0]
	elif arg[0] == "f9":
		dat.motionkey = arg[0]
	elif arg[0] == "f10":
		dat.motionkey = arg[0]
	elif arg[0] == "f11":
		dat.motionkey = arg[0]
	elif arg[0] == "f12":
		dat.motionkey = arg[0]
	elif arg[0] == "specify":
		dat.motionkey = arg[1]
	else:
		print("Invalid motion argument:", arg[0])
	


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
	
	if not dat.isInDenylist(message.author.name):
		if dat.isNewViewer(message.author.name):

			# ビューワーリストに追加:append user to list
			dat.appendViewer(message.author.name)

			# 通知音再生:play beep sound
			if SOUND:
				simpleaudio.stop_all()
				gBeep.play()

			# 有効時に登録したキーを入力:type registered key if enabled
			if dat.motionEN:
				keyboard.press_and_release(dat.motionkey)

			# 表示名取得：get display-name
			disp_name = re.search('display-name\=(.+?);', message.raw_data).group(1)

			# メッセージを表示：print message
			if disp_name == None:
				print(f'[New Viewer] {message.author.name} is coming!') # to console
			else:
				print(f'[New Viewer] {disp_name}({message.author.name}) is coming!') # to console
	
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
		elif cmd.lower() in {"viewers", "v"}:
			print(len(dat.viewer), "viewers:", dat.viewer)
		elif cmd.lower() in {"obsconnect", "oc"}:
			if not dat.obsConnected:
				dat.ws = obsws(OBSHost, OBSPort, OBSPass) # change as your OBS setting
				dat.ws.connect()
				dat.obsConnected = True
				print("OBS Connected.")
		elif cmd.lower() in {"obsdisconnect", "odc"}:
			if dat.obsConnected:
				dat.ws.disconnect()
				dat.obsConnected = False
		elif cmd != "":
			print("[CONSOLE]", cmd, "is invalid command.")
	print("interpreter end.")

if __name__ == "__main__":
	# init
	dat.ready = False
	dat.fQuit = False
	dat.channel = None
	dat.obsConnected = False

	# 機能選択
	dat.motionEN = False		# 新規ユニークコメント時ショートカットキー入力
	dat.motionkey = "e"			# デフォルトショートカットキー
	dat.raid_autoso = True		# raid時自動so
	dat.raid_beep = False		# raid時SE再生

	if USE_TAPI:
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

	# run
	t.start()
	interpreter()
	t.join()
