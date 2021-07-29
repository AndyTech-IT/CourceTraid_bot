import DB_manager
import json
import requests

Answers = None

def UpdateAnswers():
	global Answers
	Answers = DB_manager.GetAnswers()

def EditAnswer(message):
	Answers[name] = new_text
	DB_manager.UpdateAnswer(name, new_text)

def EditAllAnswers(message, bot, token):
	global Answers
	fileID = message.document.file_id
	path = bot.get_file(fileID).file_path
	uri = f'https://api.telegram.org/file/bot{token}/{path}'
	data = requests.get(uri).text
	answers_dict = json.loads(data)
	Answers = answers_dict
	DB_manager.UpdateAllAnswers(answers_dict)

def SetDefaultAnswers():
	DB_manager.LoadDefault()
	UpdateAnswers()

def GetAnswers_File():
	global Answers
	with open('Answers.json', 'w', encoding='utf-8') as file:
		json.dump(Answers, file, ensure_ascii=False, sort_keys=True, indent=4)

	file = open('Answers.json', encoding='utf-8')

	return file

UpdateAnswers()
