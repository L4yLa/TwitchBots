import os
import re
import threading
import simpleaudio
import pyautogui
from twitchio.ext import commands
from obswebsocket import obsws, requests

from chatbotstorage import ChatbotStorage

DEBUG = False

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
channelname = os.environ['CHANNEL'].replace('#', '');
botname = os.environ['BOT_NICK']

# OBS Websocket
OBSHost='localhost'
OBSPort=4444
OBSPass="password"

@bot.event
async def event_ready():
	print(f"Bot {botname} is ready.")

@bot.event
async def event_raw_data(data):
	if DEBUG:
		print("[RAW]", data)

	# Raid Detection
	if not "PRIVMSG" in data:
		if "USERNOTICE" in data and "msg-id=raid" in data:
			mname = re.search('msg-param-displayName\=(.+?);', data)
			mvcnt = re.search('msg-param-viewerCount\=([0-9]+?);', data)
			print("[RAID]", mname.group(1), "raiding with", mvcnt.group(1), "viewers!!")
#			if dat.obsConnected:
#				dat.ws.call(requests.SetCurrentScene("raid")) # OBS scene change

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
#	@bot.command(name='shoutout', aliases=['so'])
#	async def shoutout_command(ctx, *arg):
#		ctx.channel.send("Please check this awesome streamer!! {arg[0]}")



#
#  commands (mods only)
# 
@bot.command(name='quit', aliases=['q'])
async def quit_command(ctx):
	if not ctx.author.is_mod:
		return
	dat.fQuit = True
	# bot.close() # will be impliment on TwitchIO 2.0
	exit()

#	@bot.command(name='viewers')
#	async def viewers_command(ctx):
#		if not ctx.author.is_mod:
#			return
#		viewerList = dat.getViewer()
#		print(viewerList)

@bot.command(name='beep')
async def beep_command(ctx):
	if not ctx.author.is_mod:
		return
	simpleaudio.stop_all()
	gBeep.play()

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
		scenes = dat.ws.call(requests.GetSceneList())
		if scenes.status:
			print("[Scenes]")
			for s in scenes.getScenes():
				print(s["name"])

@bot.command(name='obsscene', aliases=['os', 's'])
async def obs_scenechange_command(ctx, name):
	if not ctx.author.is_mod:
		return
	if dat.obsConnected:
		res = dat.ws.call(requests.SetCurrentScene(name))

@bot.command(name='obsdisconnect', aliases=['odc'])
async def obs_disconnect_command(ctx):
	if not ctx.author.is_mod:
		return
	if dat.obsConnected:
		dat.ws.disconnect()
		dat.obsConnected = False

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
			pyautogui.typewrite(dat.motionkey)
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
	
	if not dat.isInDenylist(message.author.name):
		if dat.isNewViewer(message.author.name):

			# ビューワーリストに追加:append user to list
			dat.appendViewer(message.author.name)

			# 通知音再生:play beep sound
			simpleaudio.stop_all()
			gBeep.play()

			# 有効時に登録したキーを入力:type registered key if enabled
			if dat.motionEN:
				pyautogui.typewrite([dat.motionkey])

			# メッセージを表示：print message
			print(f'[New Viewer] {message.author.name} is coming!') # to console
	
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
	dat.motionkey = "e"
	dat.motionEN = False
	dat.fQuit = False
	dat.obsConnected = False
	t = threading.Thread(target=bot.run)

	# run
	t.start()
	interpreter()
	t.join()
