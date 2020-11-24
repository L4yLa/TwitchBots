import os
import re
import threading
import simpleaudio
from twitchio.ext import commands

DEBUG = False

bot = commands.Bot(
	irc_token = os.environ['TMI_TOKEN'],
	client_id = os.environ['CLIENT_ID'],
	nick      = os.environ['BOT_NICK'],
	prefix    = os.environ['BOT_PREFIX'],
	initial_channels = [os.environ['CHANNEL']],
	webhook_server   = False
)

class ChatbotStorage:
	def __init__(self):
		self.fQuit = False
		self.ready = False
		self.channel = None
		self.modmode = True
		self.banword = [
			'In search of followers, primes and view',
			'bigfollows',
			'Wanna become famous? Buy followers, primes and viewers',
			'Followimbot',
			#'ctrl+r', 'ctrl r', # Getting over it
		]
		self.timeoutword = [
			''
		]

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
	bot.get_channel(channelname)
	dat.ready = True

@bot.event
async def event_raw_data(data):
	if dat.ready:
		
		if DEBUG:
			print("[RAW]", data)

		# Raid Detection
		if not "PRIVMSG" in data:
			if "USERNOTICE" in data and "msg-id=raid" in data:
				mname = re.search('msg-param-displayName\=(.+?);', data)
				mvcnt = re.search('msg-param-viewerCount\=([0-9]+?);', data)
				mid   = re.search('msg-param-login\=(.+?);', data)
				print("[RAID] " + mname.group(1) + "(" + mid.group(1) + ") raiding with " + mvcnt.group(1) + " viewers!!")
				if dat.channel != None:
					await dat.channel.send(f"Please check this awesome streamer!! この素晴らしい配信者もチェックしてください！ {mid.group(1)} : https://twitch.tv/{mid.group(1)}") # Raid時のshoutout
				simpleaudio.stop_all()
				gBeep.play()

#
#  commands (mods only)
# 
@bot.command(name='test', aliases=['t'])
async def test_command(ctx):
	if not is_admin(ctx):
		return
	print(f'test message for {ctx.author.name}') # print something to console
	await ctx.channel.send(f'test message for {ctx.author.name}') # comment to chat

# Discordのリンクを表示するcommand
@bot.command(name='discord', aliases=['d', 'ディスコ'])
async def discord_command(ctx):
	if not is_admin(ctx):
		return
	await ctx.channel.send("Discord → https://discord.gg/")

# Shoutoutするcommand
@bot.command(name='shoutout', aliases=['so'])
async def shoutout_command(ctx, *arg):
	if not is_admin(ctx):
		return
	await ctx.channel.send(f"§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§  - - - - - Please check this awesome streamer!! - - - - - - - この素晴らしい配信者もチェックしてください！ - -  {arg[0]} : https://twitch.tv/{arg[0]}  §=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§=§")

# Ban wordを一時的に追加するcommand
@bot.command(name='banword', aliases=['badd', 'bw'])
async def banword_command(ctx, *arg):
	if not is_admin(ctx):
		return
	dat.banword.append(arg[0])
	await ctx.channel.send(f"{arg[0]}を永久追放ワードに追加しました. {arg[0]} added to ban words.")

# Timeout wordを一時的に追加するcommand
@bot.command(name='timeoutword', aliases=['tadd', 'tw'])
async def timeoutword_command(ctx, *arg):
	if not is_admin(ctx):
		return
	dat.timeoutword.append(arg[0])
	await ctx.channel.send(f"{arg[0]}をタイムアウトワードに追加しました. {arg[0]} added to timeout words.")

# Ban wordを一時的に削除するcommand
@bot.command(name='rmbanword', aliases=['brm', 'rmb'])
async def rmbanword_command(ctx, *arg):
	if not is_admin(ctx):
		return
	try:
		dat.banword.remove(arg[0])
	except:
		await ctx.channel.send(f"{arg[0]}を永久追放ワードから削除できませんでした. Unable to remove {arg[0]} from ban word.")
	else:
		await ctx.channel.send(f"{arg[0]}を永久追放ワードから削除しました. {arg[0]} removed from ban words.")

# Timeout wordを一時的に削除するcommand
@bot.command(name='rmtimeoutword', aliases=['trm', 'rmt'])
async def rmtimeoutword_command(ctx, *arg):
	if not is_admin(ctx):
		return
	try:
		dat.timeoutword.remove(arg[0])
	except:
		await ctx.channel.send(f"{arg[0]}をタイムアウトワードから削除できませんでした. Unable to remove {arg[0]} from timeout word.")
	else:
		await ctx.channel.send(f"{arg[0]}をタイムアウトワードから削除しました. {arg[0]} removed from timeout words.")


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
	
	if message.content[0] != "!": # message is not command
		if dat.modmode:
			# Deny-word list: Auto banning
			for dw in dat.banword:
				if dw.lower() in message.content.lower():
					# BAN
					print("[AUTO BANNED] " + message.author.name + ' word:"' + dw + '"')
					await message.channel.ban(message.author.name)
					break
			# Deny-word list: Auto timeout
			for dw in dat.timeoutword:
				if dw.lower() in message.content.lower():
					# TIMEOUT
					print("[AUTO TIMEOUT] " + message.author.name + ' word:"' + dw + '"')
					await message.channel.timeout(message.author.name, 300)
					break
	
	
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
		elif cmd.lower() in {"modmode", "mod"}:
			if dat.modmode:
				dat.modmode = False
				print("Mod-mode: disabled")
			else:
				dat.modmode = True
				print("Mod-mode: enabled")
		elif cmd.lower() in {"banword", "bw"}:
			print("[BAN WORD] ")
			for dw in dat.banword:
				print('"' + dw + '", ')
		elif cmd.lower() in {"timeoutword", "tw"}:
			print("[TIMEOUT WORD] ")
			for dw in dat.timeoutword:
				print('"' + dw + '", ')
		elif cmd != "":
			print("[CONSOLE]", cmd, "is invalid command.")
	print("interpreter end.")

if __name__ == "__main__":
	# init
	dat.fQuit = False
	t = threading.Thread(target=bot.run)

	# run
	t.start()
	interpreter()
	t.join()
