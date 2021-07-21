import DB_manager 
import requests
from admins_manager import Admins
from course import Courses_List, Course

Courses = None

def UpdateCourses():
	global Courses
	courses_dict = DB_manager.GetCoursesDict()
	Courses = Courses_List(courses_dict)

def Begin_AddCourse(message):
	Admins[message.from_user.id].IsSelecting_NewCourseCategory = True
	Admins[message.from_user.id].Dialog_Buffer = {}

#ID, CATEGORY, TITLE, DESCRIPTION, CONTENT, IMAGE
def Select_NewCourse_Category(message):
	Admins[message.from_user.id].IsSelecting_NewCourseCategory = False
	Admins[message.from_user.id].IsSelecting_NewCourseTitle = True
	Admins[message.from_user.id].Dialog_Buffer.update({'CATEGORY': message.text})

def Select_NewCourse_Title(message):
	Admins[message.from_user.id].IsSelecting_NewCourseTitle = False
	Admins[message.from_user.id].IsSelecting_NewCourseDescription = True
	Admins[message.from_user.id].Dialog_Buffer.update({'TITLE': message.text})

def Select_NewCourse_Description(message):
	Admins[message.from_user.id].IsSelecting_NewCourseDescription = False
	Admins[message.from_user.id].IsSelecting_NewCourseContent = True
	Admins[message.from_user.id].Dialog_Buffer.update({'DESCRIPTION': message.text})

def Select_NewCourse_Content(message):
	Admins[message.from_user.id].IsSelecting_NewCourseContent = False
	Admins[message.from_user.id].IsSelecting_NewCourseImage = True
	Admins[message.from_user.id].Dialog_Buffer.update({'CONTENT': message.text})

def Select_NewCourse_Image(message, token, bot):
	fileID = message.photo[-1].file_id
	path = bot.get_file(fileID).file_path
	image = requests.get(f'https://api.telegram.org/file/bot{token}/{path}').content
	Admins[message.from_user.id].Dialog_Buffer.update({'IMAGE': image})
	Admins[message.from_user.id].IsSelecting_NewCourseImage = False

def AddCourseFromBuffer(message):
	course_dict = Admins[message.from_user.id].Dialog_Buffer
	course = Course(
		course_dict['CATEGORY'], 
		course_dict['TITLE'], 
		course_dict['DESCRIPTION'],
		course_dict['CONTENT'],
		course_dict['IMAGE']
	)

	DB_manager.AddCourse(course)
	Admins[message.from_user.id].Dialog_Buffer = None
	UpdateCourses()

def DeleteCourse(callback):
	global Courses
	id = int(callback.data.split(' ')[1])
	DB_manager.DeleteCourse_byID(id)
	UpdateCourses()

UpdateCourses()