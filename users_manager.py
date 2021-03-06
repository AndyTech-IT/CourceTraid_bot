import users
from bot_user import BotUser
from user_commands import UserCommands
import DB_manager
from ovner_info import Ovner_User

Users = None
Commands = UserCommands()

def UpdateUsers():
	global Users
	users_list = DB_manager.GetUsersList()
	users_dict = {}
	for data in users_list:
		users_dict.update({data['ID']: BotUser(data['ID'])})

	if Ovner_User.ID not in users_dict:
		DB_manager.AddUser(Ovner_User.ID)

	Users = users.Users_List(Ovner_User, users_dict)

def Try_AddUser(message):
	global Users
	user_data = message.from_user
	if Users.Is_Users_Message(message):
		return False

	DB_manager.AddUser(user_data.id)
	UpdateUsers()
	return True


UpdateUsers()