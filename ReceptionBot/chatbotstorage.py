import os
import requests
from obswebsocket import obsws

class ChatbotStorage:
	
	def __init__(self):
		self.ready = bool
		self.channel = None
		self.viewer = []
		self.lurker = []
		self.denylist = [os.environ['BOT_NICK'], "streamelements", "Streamlabs", "Nightbot"]
		self.motionkey = str
		self.motionEN = bool
		self.ws = obsws
		self.obsConnected = bool
		self.fQuit = bool
		self.raid_autoso = bool
		self.raid_beep = bool
		self.header = None

	def getViewerCount(self):
		return len(self.viewer)

	def appendViewer(self, name):
		self.viewer.append(name)

	def isInDenylist(self, name):
		return name in self.denylist

	def isNewViewer(self, name):
		return not name in self.viewer

	def isLurking(self, name):
		return (name in self.lurker)

	def toLurk(self, name):
		if not (name in self.lurker):
			self.lurker.append(name)

	def unLurk(self, name):
		if(name in self.lurker):
			self.lurker.remove(name)

	def getViewer(self):
		return self.viewer

	def getLurker(self):
		return self.lurker

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
		return None
