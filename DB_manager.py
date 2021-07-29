import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from os import environ

import sqlite3
import json

_db_filename = 'DB'

_user_table_select_query = 	'SELECT ID FROM BOT_USER'
_user_table_insert_query = 	'INSERT INTO BOT_USER (ID) ' \
							'	VALUES (%s)'
_user_table_create_query =	'CREATE TABLE BOT_USER (' \
							'	ID INTEGER PRIMARY KEY' \
							');'



_admin_table_select_query =	'SELECT ID FROM BOT_ADMIN'
_admin_table_insert_query =	'INSERT INTO BOT_ADMIN (ID)' \
							'	VALUES (%s)'
_admin_table_create_query =	'CREATE TABLE BOT_ADMIN (' \
							'	ID INTEGER PRIMARY KEY' \
							');'



_course_table_select_query = \
'SELECT ID, CATEGORY, TITLE, DESCRIPTION, CONTENT, IMAGE FROM COURSE'

_course_table_insert_query = \
'''INSERT INTO COURSE (CATEGORY, TITLE, DESCRIPTION, CONTENT, IMAGE)
	VALUES (%s, %s, %s, %s, %s)'''

_course_table_update_query = \
'''UPDATE COURSE SET
	ID = %s, CATEGORY = %s, TITLE = %s, DESCRIPTION = %s, CONTENT = %s, IMAGE = %s
	WHERE ID = %s;'''

_course_table_delete_query =  \
'''DELETE FROM COURSE
	WHERE ID = %s'''

_course_table_create_query = \
'''CREATE TABLE COURSE (	
	ID SERIAL PRIMARY KEY, 			
	--ID INTEGER PRIMARY KEY AUTOINCREMENT,
	CATEGORY VARCHAR(255) NOT NULL,
	TITLE VARCHAR(255) NOT NULL,
	DESCRIPTION VARCHAR(255) NOT NULL,
	CONTENT VARCHAR(255) NOT NULL,
	IMAGE bytea NOT NULL
);'''


_answer_table_select_query = \
'SELECT NAME, TEXT FROM BOT_ANSWER'

_answer_table_insert_query = \
'''INSERT INTO BOT_ANSWER (NAME, TEXT)
	VALUES (%s, %s)'''

_answer_table_update_query = \
'''UPDATE BOT_ANSWER SET
	TEXT = %s
	WHERE NAME = %s'''

_answer_table_create_query = \
'''CREATE TABLE BOT_ANSWER (
	NAME VARCHAR(40) PRIMARY KEY,
	TEXT VARCHAR(255) NOT NULL 
);'''



def GetSQLite3_Connection():
	return sqlite3.connect('DB.sqlite3')

def GetPostgress_Connection():
	connection = psycopg2.connect(
		user=environ['DB_USER'],
		password=environ['DB_PASSWORD'],
		host=environ['DB_HOST'],
		port=environ['DB_PORT'],
		database=environ['DB']
	)
	connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	return connection

def ConnectToDB(func):
	def wrapper(*args, **kvargs):
		connection = GetPostgress_Connection()
		cursor = connection.cursor()
		result = func(cursor, *args, **kvargs)
		connection.commit()
		connection.close()
		return result
	return wrapper



@ConnectToDB
def GetUsersList(cursor):
	try:
		cursor.execute(_user_table_select_query)
		table = cursor.fetchall()
	except:
		cursor.execute(_user_table_create_query)
		table = ()

	return [{'ID': data[0]} for data in table]

@ConnectToDB
def AddUser(cursor, user_id):
	cursor.execute(_user_table_insert_query, (user_id,))
	return cursor.lastrowid



@ConnectToDB
def GetAdminsList(cursor):
	try:
		cursor.execute(_admin_table_select_query)
		table = cursor.fetchall()
	except:
		cursor.execute(_admin_table_create_query)
		table = ()

	return [{'ID': data[0]} for data in table]

@ConnectToDB
def AddAdmin(cursor, admin_id):
	cursor.execute(_admin_table_insert_query, (admin_id,))
	return cursor.lastrowid


@ConnectToDB
def GetCoursesDict(cursor):
	try:
		cursor.execute(_course_table_select_query)
		table = cursor.fetchall()
	except:
		cursor.execute(_course_table_create_query)
		table = ()
	courses_dict = {}
	for data in table:
		course_dict = \
		{
			data[0]:
			{
				'CATEGORY': data[1],
				'TITLE': data[2],
				'DESCRIPTION': data[3],
				'CONTENT': data[4],
				'IMAGE': data[5]
			}
		}
		courses_dict.update(course_dict)
	return courses_dict

@ConnectToDB
def AddCourse(cursor, course):
	cursor.execute(_course_table_insert_query, (course.Category, course.Title, course.Description, course.Content, course.Image,))
	return cursor.lastrowid
	
@ConnectToDB
def DeleteCourse_byID(cursor, id):
	cursor.execute(_course_table_delete_query, (id,))



@ConnectToDB
def GetAnswers(cursor):
	try:
		cursor.execute(_answer_table_select_query)
		table = cursor.fetchall()
		answers_dict = {}
		for row in table:
			answers_dict.update({row[0]: row[1]}) 
	except:
		cursor.execute(_answer_table_create_query)
		answers_dict = LoadDefault()
	return answers_dict

@ConnectToDB
def LoadDefault(cursor):
	default_answers_file = 'default_answers.json'
	with open(default_answers_file, encoding='utf-8') as file:
		data = file.read()
		answers_dict = json.loads(data)
	UpdateAllAnswers(answers_dict)
	return answers_dict

@ConnectToDB
def UpdateAllAnswers(cursor, answers_dict):
	for name in answers_dict:
		text = answers_dict[name]
		UpdateAnswer(name, text)
		
@ConnectToDB
def UpdateAnswer(cursor, name, new_text):
	try:
		cursor.execute(_answer_table_insert_query, (name, new_text,))
	except:
		cursor.execute(_answer_table_update_query, (new_text, name,))
