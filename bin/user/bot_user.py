class BotUser:
	def __init__(self, message):
		self.ID = message.chat.id
		pass

	def __init__(self, id):
		self.ID = id

	def __str__(self):
		return self.ID