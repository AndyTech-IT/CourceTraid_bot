import admins
from bot_admin import BotAdmin
from admin_commands import AdminCommands
import DB_manager
from ovner_info import Ovner_Admin

Admins = None
Commands = AdminCommands()

def UpdateAdmins():
	global Admins
	admins_list = DB_manager.GetAdminsList()
	admins_dict = {}
	for data in admins_list:
		admins_dict.update({data['ID']: BotAdmin(data['ID'])})

	if Ovner_Admin.ID not in admins_dict:
		DB_manager.AddAdmin(Ovner_Admin.ID)

	Admins = admins.Admins_List(Ovner_Admin, admins_dict)

def Begin_AddAdmin(message):
	Admins[message.from_user.id].IsAddingAdmin = True
	pass

def Try_AddAdmin(message):
	Admins[message.from_user.id].IsAddingAdmin = False
	try:
		id = int(message.text)
		DB_manager.AddAdmin(id)
		UpdateAdmins()
		return True
	except:
		return False
	

UpdateAdmins()