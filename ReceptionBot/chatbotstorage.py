import os

class ChatbotStorage:
	
	def __init__(self):
		self.viewer = []
		self.lurker = []
		self.denylist = [os.environ['BOT_NICK'], "streamelements", "Streamlabs", "Nightbot"]

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
