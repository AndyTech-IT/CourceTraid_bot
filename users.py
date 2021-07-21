from bot_user import BotUser

class Users_List:

	_users_dict: list

	def __init__(self, ovner, users_dict):
		if ovner.ID not in users_dict:
			users_dict.update({ovner.ID: ovner})
		self._users_dict = users_dict
		pass

	def Is_Users_Message(self, message):
		return message.from_user.id in self._users_dict

	pass