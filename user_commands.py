from chat_command import Command, Commands_List

class UserCommand(Command):
	Name: str
	Info: str
	Detail: str

	def __init__(self, name, info, detail):
		super().__init__(name, info, detail)

class UserCommands(Commands_List):
	def __init__(self):
		self.Help = UserCommand(
			'help', 
			'Справочная информация',
			'Введите @command для получения сообщения со справочной информацией'
		)
		self.Commands = UserCommand(
			'commands', 
			'Список доступных комманд',
			'Введите @command и в ответном сообщение получите список всех доступных комманд с их описанием.'
		)
		self.Command = UserCommand(
			'command', 
			'Демонстрирует пример вызова комманды',
			'Введите @command <command name>, где <command name> имя комманды без (/)'
		)
		self.Courses = UserCommand(
			'courses', 
			'Список всех доступных курсов',
			'Введите @command  для перехода в соответствующее меню'
		)
		self.Course = UserCommand(
			'course', 
			'Подробная информация о курсе',
			'Введите @command <course id>, где <course id> идентификатор курса'
		)
		self.Contacts = UserCommand(
			'contacts', 
			'Выводит все доступные способы связи с администрацией',
			'Введите @command для получения списка'
		)
		self.Developer = UserCommand(
			'developer', 
			'Информация о разработчике',
			'Введите @command, и в ответном сообщение будет информация о разработчике используеммых инструментах'
		)
		self.Feedback = UserCommand(
			'feedback', 
			'Отправляет сообщение администрации',
			'Введите @command, и в последующем сообщении введите ваше сообщение (об ошибке или пожелании)'
			)
		self.Notifications = UserCommand(
			'notifications', 
			'Меню для настройки уведомлений',
			'Введите @command для перехода в соответствующее меню'
			)

		commands = [
			self.Help,
			self.Commands,
			self.Command,
			self.Courses,
			self.Course,
			self.Feedback,
			self.Notifications,
			self.Contacts,
			self.Developer,
		]

		super().__init__(commands)

	def GetInfoMessage(self):
		message = '' 
		for key in self._commands_dict:
			command = self._commands_dict[key]
			message += f'/{command.Name}: {command.Info}\n'
		return message

	def GetDetailMessage(self, message):
		key = message.text.rpartition(' ')[2].replace('/', '')
		if key in self._commands_dict:
			command = self._commands_dict[key]
			return 	f'/{command.Name}\n' \
					f'{command.Info}\n' \
					f'{command.Detail}'

		return f'Неизвестная комманда {key}'

	def __contains__(self, item):
		return item in self._commands_dict


	def __iter__(self):
		for key in self._commands_dict:
			yield self._commands_dict[key]
