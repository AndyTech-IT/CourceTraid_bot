@bot.message_handler(commands=['commands_editor'], func=Admins.InAdminPanel)
def ComandsEditor_Handler(message):
	Begin_EditCommand(message)
	ansver = 'Выберите комманду в меню или прекрепите файл:'
	markup = types.ReplyKeyboardMarkup(row_width=2)
	user_commands = [types.KeyboardButton(f'UserCommand {command.Name}') for command in UsersCommands]
	markup.add(*user_commands)
	AnsverOnMessage(message, ansver, markup)

@bot.message_handler(content_types=['text'], func=Admins.Is_Message_by_Admin_Begin_EditCommand)
def Select_Command(message):
	if Try_SelectEditingCommand(message):
		ansver = 'Enter new Info text'
	else:
		ansver = 'You enter wrong data!'
	AnsverOnMessage(message, ansver)

@bot.message_handler(content_types=['text'], func=Admins.Is_Message_by_Admin_EditingCommandInfo)
def Edit_CommandInfo(message):
	EditCommandInfo(message)
	ansver = 'Enter new Detail'
	AnsverOnMessage(message, ansver)

@bot.message_handler(content_types=['text'], func=Admins.Is_Message_by_Admin_EditingCommandDetail)
def Edit_CommandDetail(message):
	ansver =	f'You shure want to set:\n' \
				f'{EditCommandDetail(message)}'
	markup = types.ReplyKeyboardMarkup(row_width=2)
	user_commands = [types.KeyboardButton(adswer) for adswer in ['Yes', 'No']]
	markup.add(*user_commands)
	AnsverOnMessage(message, ansver, markup)

@bot.message_handler(content_types=['text'], func=Admins.Is_Message_by_Admin_AcceptingEditedCommand)
def Accept_CommandEditing(message):
	if message.text == 'Yes':
		AcceptEditingCommand(message)
		ansver = 'Editing finish'
	else:
		ansver = 'Editing denied'

	AnsverOnMessage(message, ansver)
def Begin_EditCommand(message):
	Admins[message.from_user.id].Begin_EditCommand = True

def Try_SelectEditingCommand(message):
	commands_list = UsersCommands
	commandType, _, commandName = message.text.rpartition(' ')
	if commandType in _command_types:
		Admins[message.from_user.id].Begin_EditCommand = False
		Admins[message.from_user.id].IsEditingCommand_Info = True
		if commandType == _command_types[0] and commandName in UsersCommands:
			Admins[message.from_user.id].Dialog_Buffer = UserCommand(commandName, '', '')
			return True
	
	Admins[message.from_user.id].Begin_EditCommand = False
	return False

def EditCommandInfo(message):
	command = Admins[message.from_user.id].Dialog_Buffer
	Admins[message.from_user.id].IsEditingCommand_Info = False
	if isinstance(command, UserCommand):
		Admins[message.from_user.id].Dialog_Buffer.Info = message.text
	else:
		raise Exeption('In buffer may be UserCommand')

	Admins[message.from_user.id].IsEditingCommand_Detail = True

def EditCommandDetail(message):
	command = Admins[message.from_user.id].Dialog_Buffer
	Admins[message.from_user.id].IsEditingCommand_Detail = False
	if isinstance(command, UserCommand):
		Admins[message.from_user.id].Dialog_Buffer.Detail = message.text
	else:
		raise Exeption('In buffer may be UserCommand')

	Admins[message.from_user.id].IsAcceptingEditedCommand = True
	return 	f'{command.Name}\n' \
			f'{command.Info}\n' \
			f'{command.Detail}'

def AcceptEditingCommand(message):
	command = Admins[message.from_user.id].Dialog_Buffer
	Admins[message.from_user.id].Dialog_Buffer = None
	Admins[message.from_user.id].IsAcceptingEditedCommand = False

	if isinstance(command, UserCommand):
		DB_manager.UpdateUserCommand(command)
		UpdateCommands()
	else:
		raise Exeption('In buffer may be UserCommand')


def processPhotoMessage(message):
	fileID = message.photo[-1].file_id
	image = bot.get_file(fileID)
	with open('test.png', 'wb') as file:
		ufr = requests.get(f'https://api.telegram.org/file/bot{token}/{image.file_path}')
		file.write(ufr.content)

	with open('test.png', 'rb') as file:
		bot.send_photo(message.from_user.id, file, caption='Teafsdgsgdrhdhbsbgsgsgsgsdgsgsggsdgsg\nasdfghj\nafdsghj\nadfsgfh\nadgsfh\nasfdghfg\nasd\ndfsgsgsgsg')

@bot.message_handler(content_types=['photo'])
def photo(message):
    processPhotoMessage(message)