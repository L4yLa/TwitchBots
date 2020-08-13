import os
import simpleaudio
import pyautogui
from twitchio.ext import commands

from chatbotstorage import ChatbotStorage

bot = commands.Bot(
	irc_token = os.environ['TMI_TOKEN'],
	client_id = os.environ['CLIENT_ID'],
	nick      = os.environ['BOT_NICK'],
	prefix    = os.environ['BOT_PREFIX'],
	initial_channels = [os.environ['CHANNEL']]
)

dat = ChatbotStorage() # bot内管理データ:bot internal manage data

gBeep = simpleaudio.WaveObject.from_wave_file("beep.wav") # 通知音:New-viewer notification sound

channelname = os.environ['CHANNEL'].replace('#', '');
botname = os.environ['BOT_NICK']

@bot.event
async def event_ready():
	print(f"Bot {botname} is ready.")

#
#  commands (everyone)
# 
@bot.command(name='test', aliases=['t'])
async def test_command(ctx):
	print(f'test message for {ctx.author.name}') # print something to console
	await ctx.channel.send(f'test message for {ctx.author.name}') # comment to chat

# lurk command
#	@bot.command(name='lurk', aliases=['l'])
#	async def lurk_command(ctx):
#		if not dat.isLurking(ctx.author.name):
#			dat.toLurk(ctx.author.name)
#			print(f'{ctx.author.name} -> lurk')
#	
#	@bot.command(name='unlurk', aliases=['ul'])
#	async def unlurk_command(ctx):
#		if dat.isLurking(ctx.author.name):
#			dat.unLurk(ctx.author.name)
#			print(f'{ctx.author.name} <- unlurk')

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
#  commands (mods only)
# 
@bot.command(name='quit')
async def quit_command(ctx):
	if not ctx.author.is_mod:
		return
	# bot.close() # will be impliment on TwitchIO 2.0
	exit()

#	@bot.command(name='lurkers')
#	async def lurkers_command(ctx):
#		if not ctx.author.is_mod:
#			return
#		lurkerList = dat.getLurker()
#		print(lurkerList)

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
	simpleaudio.stop_all()
	gBeep.play()

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


if __name__ == "__main__":
	dat.motionkey = "e"
	dat.motionEN = False
	bot.run()
