import telebot
from telebot import types
from os import environ

from admins_manager import Try_AddAdmin
from admins_manager import Begin_AddAdmin
from admins_manager import Admins
from admins_manager import Commands as AdminCommands

from users_manager import Try_AddUser
from users_manager import Users
from users_manager import Commands as UsersCommands

import courses_manager
from os import environ

token = environ['BOT_TOKEN']
bot = telebot.TeleBot(token)



@bot.message_handler(commands=['start'])
def Registration_Handler(message):
	if Try_AddUser(message):
		ansver = 	'Вы были зарегистрированны в системе. Добро пожаловать!'
	else:
		ansver = 'С возвращением!'
	AnsverOnMessage(message, ansver)

	ansver = 'Введите /help для получения справочной информации'
	AnsverOnMessage(message, ansver)



@bot.message_handler(commands=[AdminCommands.Help.Name], func=Admins.InAdminPanel)
def AdminHelp_Handler(message):
	ansver = 	'Вы находитесь в панели администрирования.\n'\
				'Здесь вы можите просмотреть списки пользователей и администраторов.' \
				'Так же в этом режиме вы можите добавлять, изменять и удалять курсы.'
	AnsverOnMessage(message, ansver)
	ansver = 'Для ознакомления со списком доступных комманд введите /commands'
	AnsverOnMessage(message, ansver)


@bot.message_handler(commands=[AdminCommands.Admin.Name], func=Admins.Is_Admin_Message)
def AdminEnter_Handler(message):
	Admins.Open_AdminPanel_ForSender(message)
	ansver = 'Вы вошли в панель администратора.'
	AnsverOnMessage(message, ansver)


@bot.message_handler(commands=[AdminCommands.Exit.Name], func=Admins.InAdminPanel)
def AdminExit_Handler(message):
	Admins.Close_AdminPanel_FromSender(message)
	ansver = 'Вы покинули панель администратора.'
	AnsverOnMessage(message, ansver)


@bot.message_handler(commands=[AdminCommands.Commands.Name], func=Admins.InAdminPanel)
def Admin_ComadsList_Handler(message):
	ansver = AdminCommands.GetInfoMessage()
	AnsverOnMessage(message, ansver)

@bot.message_handler(commands=[AdminCommands.Command.Name], func=Admins.InAdminPanel)
def Admin_ComandsInfo_Handler(message):
	ansver = AdminCommands.GetDetailMessage(message)
	AnsverOnMessage(message, ansver)


@bot.message_handler(commands=[AdminCommands.AddAdmin.Name], func=Admins.InAdminPanel)
def Begin_AddAdmin_Handler(message):
	Begin_AddAdmin(message)
	ansver = 'Введите идентификатор пользователя которому хотите дать права администратора'
	AnsverOnMessage(message, ansver)

@bot.message_handler(content_types=['text'], func=Admins.Is_Message_By_Admin_Adding_NewAdmin)
def AddAdmin_Handler(message):
	if Try_AddAdmin(message):
		ansver = f'Пользователь с идентификатором {message.text} добавлен в список администрации.'
	else:
		ansver = 'Добавление отклонено!'
	AnsverOnMessage(message, ansver)


@bot.message_handler(commands=[AdminCommands.Courses.Name], func=Admins.InAdminPanel)
def CourceEditor_Handler(message):
	ansver = 'Cources list'
	courses = courses_manager.Courses.GetCourses()
	if len(courses) > 0:
		for course in courses:
			course_info = f'{course.Title} {course.Category}'
			del_course_button = types.InlineKeyboardButton('Удалить', callback_data=f'DELETE {course.ID}')
			markup = types.InlineKeyboardMarkup().add(del_course_button)
			ansver = course_info
			AnsverOnMessage(message, ansver, markup)
	else:
		ansver = 'Курсы не найдены!'
		AnsverOnMessage(message, ansver)

@bot.callback_query_handler(func=lambda cb: cb.data.split(' ')[0] == 'DELETE')
def DeleteCourse_Handler(callback):
	info, image= courses_manager.Courses.Try_GetCourseInfo_and_Image_byCallback(callback)
	AnsverOnCallback(callback, info, image_file=image)
	courses_manager.DeleteCourse(callback)
	ansver = 'Курс удалён!'
	AnsverOnCallback(callback, ansver)

@bot.message_handler(commands=[AdminCommands.Course.Name], func=Admins.InAdminPanel)
def CourceEditor_Handler(message):
	ansver = 'Cource padge'
	AnsverOnMessage(message, ansver)

@bot.message_handler(commands=[AdminCommands.AddCourse.Name], func=Admins.InAdminPanel)
def Begin_AddCourse_Handler(message):
	courses_manager.Begin_AddCourse(message)
	ansver = 'Введите категорию курса, или выберите существующую'
	markup = types.ReplyKeyboardMarkup(row_width=2)
	battons = [types.KeyboardButton(category) for category in courses_manager.Courses.GetCategorys_List()]
	markup.add(*battons)
	AnsverOnMessage(message, ansver, markup)

@bot.message_handler(content_types=['text'], func=Admins.Is_Message_By_Admin_Select_NewCourse_Category)
def Select_NewCourse_Category_Handler(message):
	courses_manager.Select_NewCourse_Category(message)
	ansver = 'Введите название курса'
	AnsverOnMessage(message, ansver)

@bot.message_handler(content_types=['text'], func=Admins.Is_Message_By_Admin_Select_NewCourse_Title)
def Select_NewCourse_Title_Handler(message):
	courses_manager.Select_NewCourse_Title(message)
	ansver = 'Введите краткое описание курса'
	AnsverOnMessage(message, ansver)

@bot.message_handler(content_types=['text'], func=Admins.Is_Message_By_Admin_Select_NewCourse_Description)
def Select_NewCourse_Description_Handler(message):
	courses_manager.Select_NewCourse_Description(message)
	ansver = 'Введите основную информация курса'
	AnsverOnMessage(message, ansver)

@bot.message_handler(content_types=['text'], func=Admins.Is_Message_By_Admin_Select_NewCourse_Content)
def Select_NewCourse_Content_Handler(message):
	courses_manager.Select_NewCourse_Content(message)
	ansver = 'Отправте изображение для курса'
	AnsverOnMessage(message, ansver)

@bot.message_handler(content_types=['photo'], func=Admins.Is_Message_By_Admin_Select_NewCourse_Image)
def Select_NewCourse_Content_Handler(message):
	courses_manager.Select_NewCourse_Image(message, token, bot)
	courses_manager.AddCourseFromBuffer(message)
	ansver = 'Курс успешно добавлен!'
	AnsverOnMessage(message, ansver)


@bot.message_handler(commands=[AdminCommands.Feedback.Name], func=Admins.InAdminPanel)
def CourceEditor_Handler(message):
	ansver = 'Feedback menu'
	AnsverOnMessage(message, ansver)


@bot.message_handler(commands=[AdminCommands.Contacts.Name], func=Admins.InAdminPanel)
def CourceEditor_Handler(message):
	ansver = 'Contacts menu'
	AnsverOnMessage(message, ansver)

@bot.message_handler(commands=[AdminCommands.Notifications.Name], func=Admins.InAdminPanel)
def CourceEditor_Handler(message):
	ansver = 'Notifications list'
	AnsverOnMessage(message, ansver)

@bot.message_handler(commands=[AdminCommands.Notification.Name], func=Admins.InAdminPanel)
def CourceEditor_Handler(message):
	ansver = 'Notification menu'
	AnsverOnMessage(message, ansver)




@bot.message_handler(commands=[UsersCommands.Help.Name], func=Users.Is_Users_Message)
def UserHelp_Handler(message):
	ansver = 	'Вы находитесь в меню пользователя чат-бота.\n' \
				'Здесь вы можите ознакомится со списком доступных курсов и подать заявку о записи на курс'
	AnsverOnMessage(message, ansver)
	ansver = 	'Чтобы ознакомитсья со списком всех комманд: \n' \
				f'Отправте сообщение с текстом /{UsersCommands.Commands.Name}'
	AnsverOnMessage(message, ansver)


@bot.message_handler(commands=[UsersCommands.Commands.Name], func=Users.Is_Users_Message)
def ComadsList_Handler(message):
	ansver = UsersCommands.GetInfoMessage()
	AnsverOnMessage(message, ansver)

	if Admins.Is_Admin_Message(message):
		ansver = 'И вам как администратору доступна панель администратора - /admin'
	AnsverOnMessage(message, ansver)

@bot.message_handler(commands=[UsersCommands.Command.Name], func=Users.Is_Users_Message)
def ComandsInfo_Handler(message):
	ansver = UsersCommands.GetDetailMessage(message)
	AnsverOnMessage(message, ansver)


@bot.message_handler(commands=[UsersCommands.Courses.Name], func=Users.Is_Users_Message)
def CourcesList_Handler(message):
	courses =  courses_manager.Courses.GetCourses_InfoList()
	if len(courses) > 0:
		for line in courses:
			ansver = line
			AnsverOnMessage(message, ansver)
	else:
		ansver = 'Курсы не найдены'
		AnsverOnMessage(message, ansver)

@bot.message_handler(commands=[UsersCommands.Course.Name], func=Users.Is_Users_Message)
def CourceInfo_Handler(message):
	result = courses_manager.Courses.Try_GetCourseInfo_and_Image_byMessage(message)
	if result:
		ansver, image = result
		AnsverOnMessage(message, ansver, image_file=image)
	else:
		ansver = 'Указанного курса не существует!'
		AnsverOnMessage(message, ansver)


@bot.message_handler(commands=[UsersCommands.Feedback.Name], func=Users.Is_Users_Message)
def Feedback_Handler(message):
	ansver = 'Feedback dialog'
	AnsverOnMessage(message, ansver)


@bot.message_handler(commands=[UsersCommands.Notifications.Name], func=Users.Is_Users_Message)
def NotificationsSettings_Handler(message):
	ansver = 'Notifications menu'
	AnsverOnMessage(message, ansver)


@bot.message_handler(commands=[UsersCommands.Contacts.Name], func=Users.Is_Users_Message)
def ContactsList_Handler(message):
	ansver = 'Contacts list'
	AnsverOnMessage(message, ansver)

@bot.message_handler(commands=[UsersCommands.Developer.Name], func=Users.Is_Users_Message)
def DevelopInfo_Handler(message):
	ansver = 	'Разработчик: Коковихин Андрей\n' \
				'Хостинг: Heroku.com\n' \
				'Язык программирования: Python\n' \
				'Библиотека чат бота: TelegramBotAPI'
	AnsverOnMessage(message, ansver)




@bot.message_handler(commands=['help'])
def GuestHelp_Handler(message):
	ansver =	'Вы находитесь в гостевом режиме. \n' \
				'Доступ ко многим функциям закрыт!\n'
	AnsverOnMessage(message, ansver)

	ansver = 'Введите /start для регистрации в системе'
	AnsverOnMessage(message, ansver)




@bot.message_handler(func = lambda msg: True)
def DefaultMessage_Handler(message):
	ansver = 	f'Не понятное сообщение:\n' \
				f'{message.text}'
	AnsverOnMessage(message, ansver)


def AnsverOnCallback(message, ansver, markup=None, image_file=None):
	if markup is None:
		markup = types.ReplyKeyboardRemove(selective=False)
	if image_file is None:
		bot.send_message(message.from_user.id, ansver, reply_markup=markup)
	else:
		bot.send_photo(message.from_user.id, image_file, caption=ansver, reply_markup=markup)

def AnsverOnMessage(message, ansver, markup=None, image_file=None):
	if markup is None:
		markup = types.ReplyKeyboardRemove(selective=False)
	if image_file is None:
		bot.send_message(message.chat.id, ansver, reply_markup=markup)
	else:
		bot.send_photo(message.chat.id, image_file, caption=ansver, reply_markup=markup)




if __name__ == '__main__':
	bot.polling()