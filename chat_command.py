class Command:
	Name: str
	Info: str
	Detail: str

	def __init__(self, name, info, detail):
		self.Name = name.lower().replace(' ', '_')
		self.Info = info
		self.Detail = detail.replace('@command', f'/{self.Name}')

	def __str__(self):
		return self.Name

class Commands_List:
	def __init__(self, commands):
		self._commands_dict = {}
		for command in commands:
			self._commands_dict.update({command.Name: command})

	def GetInfoMessage(self):
		lines = [] 
		for key in self._commands_dict:
			command = self._commands_dict[key]
			lines.append(f'/{command.Name}: {command.Info}')
		return '\n'.join(lines)

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
