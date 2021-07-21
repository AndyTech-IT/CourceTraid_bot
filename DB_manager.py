import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

_db_filename = 'DB'

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
	cursor = ConnectToDB()
	try:
		table = cursor.execute(_user_table_select_query).fetchall()
	except:
		cursor.execute(_user_table_create_query)
		table = ()

	return [{'ID': data[0]} for data in table]

def AddUser(user_id):
	cursor = ConnectToDB()
	cursor.execute(_user_table_insert_query, (user_id,))



def GetAdminsList():
	cursor = ConnectToDB()
	try:
		table = cursor.execute(_admin_table_select_query).fetchall()
	except:
		cursor.execute(_admin_table_create_query)
		table = ()

	return [{'ID': data[0]} for data in table]

def AddAdmin(admin_id):
	cursor = ConnectToDB()
	cursor.execute(_admin_table_insert_query, (admin_id,))


def GetCoursesDict():
	cursor = ConnectToDB()
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
	cursor = ConnectToDB()
	cursor.execute(_course_table_insert_query, (course.Category, course.Title, course.Description, course.Content, course.Image,))


def DeleteCourse_byID(id):
	cursor = ConnectToDB()
	cursor.execute(_course_table_delete_query, (id,))


def ConnectToDB():
	try:
		with psycopg2.connect(
			user="khjhfboutmiizc",
			password="390f718a8b0e583cb6fe6120fbb479e364690b6f9140f4284791553d3b1f5574",
			host="ec2-79-125-30-28.eu-west-1.compute.amazonaws.com",
			port="5432",
			database="dfa74tvmhupjn0"
		) as connection:
			connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
			return connection.cursor()
	except (Exception, Error) as error:
		print(error)