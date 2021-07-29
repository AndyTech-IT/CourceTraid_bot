import telebot
from telebot import types
from os import environ

import admins_manager
from admins_manager import Try_AddAdmin
from admins_manager import Begin_AddAdmin
from admins_manager import Commands as AdminCommands

import users_manager
from users_manager import Try_AddUser
from users_manager import Commands as UsersCommands

import bot_answers

import courses_manager
from os import environ

token = environ['BOT_TOKEN']
bot = telebot.TeleBot(token)



@bot.message_handler(commands=['start'])
def Registration_Handler(message):
	if Try_AddUser(message):
		answer = bot_answers.Answers['user_registered']
	else:
		answer = bot_answers.Answers['user_loginin']
	answerOnMessage(message, answer)
	CourcesList_Handler(message)



@bot.message_handler(commands=[AdminCommands.Help.Name], func=admins_manager.Admins.InAdminPanel)
def AdminHelp_Handler(message):
	answer = bot_answers.Answers['admin_help']
	answerOnMessage(message, answer)


@bot.message_handler(commands=[AdminCommands.GetAnswers.Name], func=admins_manager.Admins.InAdminPanel)
def GetAnswers_Handler(message):
	file = bot_answers.GetAnswers_File()
	answer = bot_answers.Answers['answers_file_caption']
	answerOnMessage(message, answer, data_file=file)

@bot.message_handler(func=admins_manager.Admins.InAdminPanel, content_types=['document'])
def SetAnswers_Handler(message):
	bot_answers.EditAllAnswers(message, bot, token)
	answer = bot_answers.Answers['all_answers_edited']
	answerOnMessage(message, answer)

@bot.message_handler(commands=[AdminCommands.Admin.Name], func=admins_manager.Admins.Is_Admin_Message)
def AdminEnter_Handler(message):
	admins_manager.Admins.Open_AdminPanel_ForSender(message)
	answer = bot_answers.Answers['admin_panel_enter']
	answerOnMessage(message, answer)


@bot.message_handler(commands=[AdminCommands.Exit.Name], func=admins_manager.Admins.InAdminPanel)
def AdminExit_Handler(message):
	admins_manager.Admins.Close_AdminPanel_FromSender(message)
	answer = bot_answers.Answers['admin_panel_exit']
	answerOnMessage(message, answer)


@bot.message_handler(commands=[AdminCommands.Commands.Name], func=admins_manager.Admins.InAdminPanel)
def Admin_ComadsList_Handler(message):
	answer = AdminCommands.GetInfoMessage()
	answerOnMessage(message, answer)

@bot.message_handler(commands=[AdminCommands.Command.Name], func=admins_manager.Admins.InAdminPanel)
def Admin_ComandsInfo_Handler(message):
	answer = AdminCommands.GetDetailMessage(message)
	answerOnMessage(message, answer)


@bot.message_handler(commands=[AdminCommands.AddAdmin.Name], func=admins_manager.Admins.InAdminPanel)
def Begin_AddAdmin_Handler(message):
	Begin_AddAdmin(message)
	answer = bot_answers.Answers['add_admin_enter_id']
	answerOnMessage(message, answer)

@bot.message_handler(content_types=['text'], func=admins_manager.Admins.Is_Message_By_Admin_Adding_NewAdmin)
def AddAdmin_Handler(message):
	if Try_AddAdmin(message):
		answer = bot_answers.Answers['add_admin_dialog_succesed'].replace('@id', message.text)
	else:
		answer = bot_answers.Answers['add_admin_dialog_failed']
	answerOnMessage(message, answer)


@bot.message_handler(commands=[AdminCommands.Courses.Name], func=admins_manager.Admins.InAdminPanel)
def CourceEditor_Handler(message):
	courses = courses_manager.Courses.GetCourses()
	if len(courses) > 0:
		for course in courses:
			course_info = f'{course.Title} {course.Category}'
			del_course_button = types.InlineKeyboardButton('Удалить', callback_data=f'DELETE {course.ID}')
			markup = types.InlineKeyboardMarkup().add(del_course_button)
			answer = course_info
			answerOnMessage(message, answer, markup)
	else:
		answer = bot_answers.Answers['courses_not_exist']
		answerOnMessage(message, answer)

@bot.callback_query_handler(func=lambda cb: cb.data.split(' ')[0] == 'DELETE')
def DeleteCourse_Handler(callback):
	course = courses_manager.GetCourse_By_Callback(callback)
	courses_manager.DeleteCourse(callback)
	answer = bot_answers.Answers['course_removed'].replace('@title', course.Title).replace('@category', course.Category)
	answerOnCallback(callback, answer)

@bot.message_handler(commands=[AdminCommands.AddCourse.Name], func=admins_manager.Admins.InAdminPanel)
def Begin_AddCourse_Handler(message):
	courses_manager.Begin_AddCourse(message)
	answer = bot_answers.Answers['add_course_enter_category']
	markup = types.ReplyKeyboardMarkup(row_width=2)
	battons = [types.KeyboardButton(category) for category in courses_manager.Courses.GetCategorys_List()]
	markup.add(*battons)
	answerOnMessage(message, answer, markup)

@bot.message_handler(content_types=['text'], func=admins_manager.Admins.Is_Message_By_Admin_Select_NewCourse_Category)
def Select_NewCourse_Category_Handler(message):
	courses_manager.Select_NewCourse_Category(message)
	answer = bot_answers.Answers['add_course_enter_title']
	answerOnMessage(message, answer)

@bot.message_handler(content_types=['text'], func=admins_manager.Admins.Is_Message_By_Admin_Select_NewCourse_Title)
def Select_NewCourse_Title_Handler(message):
	courses_manager.Select_NewCourse_Title(message)
	answer = bot_answers.Answers['add_course_enter_description']
	answerOnMessage(message, answer)

@bot.message_handler(content_types=['text'], func=admins_manager.Admins.Is_Message_By_Admin_Select_NewCourse_Description)
def Select_NewCourse_Description_Handler(message):
	courses_manager.Select_NewCourse_Description(message)
	answer = bot_answers.Answers['add_course_enter_detail']
	answerOnMessage(message, answer)

@bot.message_handler(content_types=['text'], func=admins_manager.Admins.Is_Message_By_Admin_Select_NewCourse_Content)
def Select_NewCourse_Content_Handler(message):
	courses_manager.Select_NewCourse_Content(message)
	answer = bot_answers.Answers['add_course_enter_image']
	answerOnMessage(message, answer)

@bot.message_handler(content_types=['photo'], func=admins_manager.Admins.Is_Message_By_Admin_Select_NewCourse_Image)
def Select_NewCourse_Content_Handler(message):
	courses_manager.Select_NewCourse_Image(message, token, bot)
	course = courses_manager.AddCourseFromBuffer(message)
	answer = bot_answers.Answers['add_course_dialog_succesed']
	answerOnMessage(message, answer)
	notify_message = f'Добавлен новый курс:\n{course.GetInfo()}'
	Notify_Users(message, notify_message)


@bot.message_handler(commands=[AdminCommands.Feedback.Name], func=admins_manager.Admins.InAdminPanel)
def CourceEditor_Handler(message):
	answer = 'Feedback menu'
	answerOnMessage(message, answer)


@bot.message_handler(commands=[AdminCommands.Contacts.Name], func=admins_manager.Admins.InAdminPanel)
def CourceEditor_Handler(message):
	answer = bot_answers.Answers['contacts_message']
	answerOnMessage(message, answer)

@bot.message_handler(commands=[AdminCommands.Notifications.Name], func=admins_manager.Admins.InAdminPanel)
def CourceEditor_Handler(message):
	answer = 'Notifications list'
	answerOnMessage(message, answer)

@bot.message_handler(commands=[AdminCommands.Notification.Name], func=admins_manager.Admins.InAdminPanel)
def CourceEditor_Handler(message):
	answer = 'Notification menu'
	answerOnMessage(message, answer)




@bot.message_handler(commands=[UsersCommands.Help.Name], func=users_manager.Users.Is_Users_Message)
def UserHelp_Handler(message):
	answer = bot_answers.Answers['user_help']
	answerOnMessage(message, answer)


@bot.message_handler(commands=[UsersCommands.Commands.Name], func=users_manager.Users.Is_Users_Message)
def ComadsList_Handler(message):
	answer = UsersCommands.GetInfoMessage()
	answerOnMessage(message, answer)

	if admins_manager.Admins.Is_Admin_Message(message):
		answer = bot_answers.Answers['if_user_is_admin'].replace('@admin', AdminCommands.Admin.Name)
	answerOnMessage(message, answer)

@bot.message_handler(commands=[UsersCommands.Command.Name], func=users_manager.Users.Is_Users_Message)
def ComandsInfo_Handler(message):
	answer = UsersCommands.GetDetailMessage(message)
	answerOnMessage(message, answer)


@bot.message_handler(commands=[UsersCommands.Courses.Name], func=users_manager.Users.Is_Users_Message)
def CourcesList_Handler(message):
	categorys =  courses_manager.Courses.GetCategorys_List()
	answer = f'Используйте комманду /{UsersCommands.Course.Name} чтобы узнать информацию о курсе.'
	answerOnMessage(message, answer)
	if len(categorys) > 0:
		for category in categorys:
			header = f'Категория {category}'
			extend_button = types.InlineKeyboardButton('Список курсов', callback_data=f'EXTEND {category}')
			markup = types.InlineKeyboardMarkup().add(extend_button)
			answerOnMessage(message, header, markup)
	else:
		answer = bot_answers.Answers['courses_not_exist']
		answerOnMessage(message, answer)

@bot.callback_query_handler(func=lambda cb: cb.data.split(' ')[0] == 'EXTEND')
def Extend_CourseCategory(callback):
	category = callback.data.split(' ')[1]
	courses = courses_manager.Courses.GetCategory_CoursesList(category)
	answer = f'Категория {category}\n'
	for course in courses:
		answer += course.GetInfo()
	Edit_OnCallback(callback, answer)


@bot.message_handler(commands=[UsersCommands.Course.Name], func=users_manager.Users.Is_Users_Message)
def CourceInfo_Handler(message):
	result = courses_manager.Courses.Try_GetCourseInfo_and_Image_byMessage(message)
	if result:
		answer, image = result
		answerOnMessage(message, answer, image_file=image)
	else:
		answer = bot_answers.Answers['course_not_exits']
		answerOnMessage(message, answer)


@bot.message_handler(commands=[UsersCommands.Feedback.Name], func=users_manager.Users.Is_Users_Message)
def Feedback_Handler(message):
	answer = 'Feedback dialog'
	answerOnMessage(message, answer)


@bot.message_handler(commands=[UsersCommands.Notifications.Name], func=users_manager.Users.Is_Users_Message)
def NotificationsSettings_Handler(message):
	answer = 'Notifications menu'
	answerOnMessage(message, answer)


@bot.message_handler(commands=[UsersCommands.Contacts.Name], func=users_manager.Users.Is_Users_Message)
def ContactsList_Handler(message):
	answer = bot_answers.Answers['contacts_message']
	answerOnMessage(message, answer)

@bot.message_handler(commands=[UsersCommands.Developer.Name], func=users_manager.Users.Is_Users_Message)
def DevelopInfo_Handler(message):
	answer = 	'Разработчик: Коковихин Андрей\n' \
				'Хостинг: Heroku.com\n' \
				'Язык программирования: Python\n' \
				'Библиотека чат бота: TelegramBotAPI'
	answerOnMessage(message, answer)




@bot.message_handler(commands=['help'])
def GuestHelp_Handler(message):
	answer = bot_answers.Answers['guest_help']
	answerOnMessage(message, answer)




@bot.message_handler(func = lambda msg: True)
def DefaultMessage_Handler(message):
	answer = bot_answers.Answers['incomprehensible_command']
	answerOnMessage(message, answer)


def Notify_Users(message, text, image=None, file=None, markup=None):
	for user in users_manager.Users:
		if user.ID != message.from_user.id:
			Send_Answer(user.ID, text, markup, image, file)

def Edit_OnCallback(callback, new_text, markup = None):
	message_id = callback.message.id
	id = callback.from_user.id
	bot.edit_message_text(chat_id=id, message_id=message_id, text=new_text, reply_markup=markup)

def answerOnCallback(callback, answer, markup=None, image_file=None, data_file=None):
	Send_Answer(callback.from_user.id, answer, markup, image_file, data_file)


def answerOnMessage(message, answer, markup=None, image_file=None, data_file=None):
	Send_Answer(message.from_user.id, answer, markup, image_file, data_file)
	

def Send_Answer(id, answer, markup=None, image=None, file=None):
	if markup is None:
		markup = types.ReplyKeyboardRemove(selective=False)
	if image:
		bot.send_photo(id, image, caption=answer, reply_markup=markup)
	elif file:
		bot.send_document(id, file, caption=answer, reply_markup=markup)
	else:
		bot.send_message(id, answer, reply_markup=markup)

if __name__ == '__main__':
	print('Start')
	bot.polling()