import sqlite3

_db_filename = 'DB.py'

_user_table_select_query = 	'SELECT ID FROM USER'
_user_table_insert_query = 	'INSERT INTO USER (ID) ' \
							'	VALUES (?)'
_user_table_create_query =	'CREATE TABLE USER (' \
							'	ID INT NOT NULL,' \
							'	PRIMARY KEY (ID)' \
							');'



_admin_table_select_query =	'SELECT ID FROM ADMIN'
_admin_table_insert_query =	'INSERT INTO ADMIN (ID)' \
							'	VALUES (?)'
_admin_table_create_query =	'CREATE TABLE ADMIN (' \
							'	ID INT NOT NULL,' \
							'	PRIMARY KEY (ID)' \
							');'



_course_table_select_query = 	'SELECT ID, CATEGORY, TITLE, DESCRIPTION, CONTENT, IMAGE FROM COURSE'
_course_table_insert_query = 	'INSERT INTO COURSE (CATEGORY, TITLE, DESCRIPTION, CONTENT, IMAGE)' \
								'	VALUES (?, ?, ?, ?, ?)'

_course_table_update_query = 	'UPDATE COURSE SET' \
								'	ID = ?, CATEGORY = ?, TITLE = ?, DESCRIPTION = ?, CONTENT = ?, IMAGE = ?' \
								'	WHERE ID = ?'
_course_table_delete_query = 	'DELETE FROM COURSE' \
								'	WHERE ID = ?'
_course_table_create_query = 	'CREATE TABLE COURSE (' \
								'	ID INTEGER PRIMARY KEY AUTOINCREMENT,' \
								'	CATEGORY VARCHAR(255) NOT NULL,' \
								'	TITLE VARCHAR(255) NOT NULL,' \
								'	DESCRIPTION VARCHAR(255) NOT NULL,' \
								'	CONTENT VARCHAR(255) NOT NULL,' \
								'	IMAGE MEDIUMBLOB NOT NULL' \
								');'



def GetUsersList():
	with sqlite3.connect(_db_filename) as con:
		cursor = con.cursor()
		try:
			table = cursor.execute(_user_table_select_query).fetchall()
		except:
			cursor.execute(_user_table_create_query)
			table = ()

	return [{'ID': data[0]} for data in table]

def AddUser(user_id):
	with sqlite3.connect(_db_filename) as con:
		cursor = con.cursor()
		cursor.execute(_user_table_insert_query, (user_id,))



def GetAdminsList():
	with sqlite3.connect(_db_filename) as con:
		cursor = con.cursor()
		try:
			table = cursor.execute(_admin_table_select_query).fetchall()
		except:
			cursor.execute(_admin_table_create_query)
			table = ()

	return [{'ID': data[0]} for data in table]

def AddAdmin(admin_id):
	with sqlite3.connect(_db_filename) as con:
		cursor = con.cursor()
		cursor.execute(_admin_table_insert_query, (admin_id,))


def GetCoursesDict():
	with sqlite3.connect(_db_filename) as con:
		cursor = con.cursor()
	try:
		table = cursor.execute(_course_table_select_query).fetchall()
	except:
		cursor.execute(_course_table_create_query).fetchall()
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

def AddCourse(course):
	with sqlite3.connect(_db_filename) as con:
		cursor = con.cursor()
		cursor.execute(_course_table_insert_query, (course.Category, course.Title, course.Description, course.Content, course.Image,))


def Try_UpdateCourse(old_id, course, new_id=None):
	if new_id is None:
		new_id = old_id
	with sqlite3.connect(_db_filename) as con:
		cursor = con.cursor()
		try:
			cursor.execute(_course_table_update_query, (new_id, course.Category, course.Title, course.Description, course.Content, course.Image, old_id))
			return True
		except:
			return False

def DeleteCourse_byID(id):
	with sqlite3.connect(_db_filename) as con:
		cursor = con.cursor()
		cursor.execute(_course_table_delete_query, (id,))