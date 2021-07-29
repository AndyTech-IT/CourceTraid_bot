from chat_command import Command, Commands_List

class AdminCommand(Command):
	Name: str
	Info: str
	Detail: str

	def __init__(self, name, info, detail):
		super().__init__(name, info, detail)

class AdminCommands(Commands_List):
	def __init__(self):
		self.Help = AdminCommand(
			'help', 
			'Справочная информация',
			'Введите @command для получения сообщения со справочной информацией'
		)
		self.Commands = AdminCommand(
			'commands', 
			'Список доступных комманд',
			'Введите @command и в ответном сообщение получите список всех доступных комманд с их описанием.'
		)
		self.Command = AdminCommand(
			'command', 
			'Демонстрирует пример вызова комманды',
			'Введите @command <command name>, где <command name> имя комманды без (/)'
		)
		self.Courses = AdminCommand(
			'courses', 
			'Список всех курсов хранящихся в базе данных',
			'Введите @command для перехода в соответствующее меню'
		)
		self.AddCourse = AdminCommand(
			'add_course',
			'Добавление нового курса в базу данных',
			'Введите @command для начала диалога'
		)
		self.Contacts = AdminCommand(
			'contacts', 
			'Меню настройки способов обратной связи пользователя с администрацией (e-mail, номер телефона и т.п.)',
			'Введите @command для перехода в соответствующее меню'
		)
		self.Feedback = AdminCommand(
			'feedback', 
			'Настройка интерфейса отправки отзыва',
			'Введите @command, для перехода в соответствующее меню'
			)
		self.Notifications = AdminCommand(
			'notifications', 
			'Меню для настройки уведомлений',
			'Введите @command для перехода в соответствующее меню'
			)
		self.Notification = AdminCommand(
			'notification',
			'Настройка конкретного уведомаления',
			'Введите @command для перехода в соответствующее меню'
		)
		self.AddAdmin = AdminCommand(
			'add_admin',
			'Предоставление прав администратора пользователю',
			'Введите @command для начала диалога'
		)
		self.Admin = AdminCommand(
			'admin',
			'Комманда для входа в панель администратора',
			'Введите @command для перехода в панель администратора'
		)
		self.Exit = AdminCommand(
			'exit',
			'Комманда для выхода из панели администратора',
			'Введите @command для перехода в панель пользователя'
		)
		self.SetNewAnswer = AdminCommand(
			'set_answer',
			'Комманда для изменения текста сообщения бота',
			'Введите @command <answer name> <new text>, где <answer name> кодовое название сообщения'
		)
		self.GetAnswers = AdminCommand(
			'get_answers',
			'Комманда для получения json файла содержащего все сообщения бота, доступные для редактирования, а <new text> новый текст сообщения',
			'Введите @command для получения конфигурационного файла'
		)
		self.SetAnswers = AdminCommand(
			'set_answers',
			'Комманда для отметки сообщеия с json файлом содержащим сообщения бота',
			'Прикрепите файл json, и в поле Caption укажите @command'
		)
		self.SetDefaultAnswers = AdminCommand(
			'default_answers',
			'Устанавливает текст сообщений бота в стандартный вид, установленный разработчиком',
			'Введите @command для сброса всех сообщений бота к стандартным'
		)

		commands = [
			self.Help,
			self.Admin,
			self.Exit,
			self.Commands,
			self.Command,
			self.AddCourse,
			self.AddAdmin,
			self.Courses,
			self.Feedback,
			self.Contacts,
			self.Notifications,
			self.Notification,
			self.SetNewAnswer,
			self.GetAnswers,
			self.SetAnswers,
			self.SetDefaultAnswers,
		]

		super().__init__(commands)