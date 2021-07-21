from bot_admin import BotAdmin

class Admins_List:
	
	_admins_Dict: dict

	def __init__(self, ovner, admins_dict):
		if ovner not in admins_dict:
			admins_dict.update({ovner.ID: ovner})
		self._admins_Dict = admins_dict
		pass

	def __getitem__(self, key):
		return self._admins_Dict[key]

	def __setitem__(self, key, value):
		self._admins_Dict[key] = value


	def Is_Admin_Message(self, message):
		return message.from_user.id in self._admins_Dict


	def Open_AdminPanel_ForSender(self, message):
		self._admins_Dict[message.from_user.id].In_Panel = True

	def Close_AdminPanel_FromSender(self, message):
		self._admins_Dict[message.from_user.id].In_Panel = False

	def InAdminPanel(self, message):
		if self.Is_Admin_Message(message):
			return self._admins_Dict[message.from_user.id].In_Panel
		return False

	def Is_Message_By_Admin_Adding_NewAdmin(self, message):
		if self.Is_Admin_Message(message):
			return self._admins_Dict[message.from_user.id].IsAddingAdmin

		return False

	def Is_Message_By_Admin_Select_NewCourse_Category(self, message):
		if self.Is_Admin_Message(message):
			return self._admins_Dict[message.from_user.id].IsSelecting_NewCourseCategory

		return False	

	def Is_Message_By_Admin_Select_NewCourse_Title(self, message):
		if self.Is_Admin_Message(message):
			return self._admins_Dict[message.from_user.id].IsSelecting_NewCourseTitle

		return False

	def Is_Message_By_Admin_Select_NewCourse_Description(self, message):
		if self.Is_Admin_Message(message):
			return self._admins_Dict[message.from_user.id].IsSelecting_NewCourseDescription

		return False	

	def Is_Message_By_Admin_Select_NewCourse_Content(self, message):
		if self.Is_Admin_Message(message):
			return self._admins_Dict[message.from_user.id].IsSelecting_NewCourseContent

		return False	

	def Is_Message_By_Admin_Select_NewCourse_Image(self, message):
		if self.Is_Admin_Message(message):
			return self._admins_Dict[message.from_user.id].IsSelecting_NewCourseImage

		return False
	pass