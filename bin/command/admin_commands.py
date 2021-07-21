from .chat_command import Command, Commands_List

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
		self.Course = AdminCommand(
			'course', 
			'Меню настройки курса',
			'Введите @command <course id>, где <course id> идентификатор курса'
		)
		self.AddCourse = AdminCommand(
			'add_course',
			'Добавление нового курса в базу данных',
			'Введите @command для начала диалога'
		)
		self.Contacts = AdminCommand(
			'contacts', 
			'Меню настройки способов обратной связи пользователя с администрацией (e-main, номер телефона и т.п.)',
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

		commands = [
			self.Help,
			self.Admin,
			self.Exit,
			self.Commands,
			self.Command,
			self.AddCourse,
			self.AddAdmin,
			self.Courses,
			self.Course,
			self.Feedback,
			self.Contacts,
			self.Notifications,
			self.Notification,
		]

		super().__init__(commands)