class BotAdmin:
	def __init__(self, id):
		self.ID = id

		self.In_Panel = True

		self.IsAddingAdmin = False

		self.IsSelecting_NewCourseCategory = False
		self.IsSelecting_NewCourseTitle = False
		self.IsSelecting_NewCourseDescription = False
		self.IsSelecting_NewCourseContent = False
		self.IsSelecting_NewCourseImage = False
		self.IsAccepting_NewCourse = False

		self.IsAccepting_EditingCourse = False

		self.Dialog_Buffer = None
