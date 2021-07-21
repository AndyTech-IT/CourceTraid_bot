import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

_db_filename = 'DB'

_user_table_select_query = 	'SELECT ID FROM USER1'
_user_table_insert_query = 	'INSERT INTO USER1 (ID) ' \
							'	VALUES (?)'
_user_table_create_query =	'CREATE TABLE USER1 (' \
							'	ID INT NOT NULL,' \
							'	PRIMARY KEY (ID)' \
							');'



_admin_table_select_query =	'SELECT ID FROM ADMIN1'
_admin_table_insert_query =	'INSERT INTO ADMIN1 (ID)' \
							'	VALUES (?)'
_admin_table_create_query =	'CREATE TABLE ADMIN1 (' \
							'	ID INT NOT NULL,' \
							'	PRIMARY KEY (ID)' \
							');'



_course_table_select_query = 	'SELECT ID, CATEGORY, TITLE, DESCRIPTION, CONTENT, IMAGE FROM COURSE1'
_course_table_insert_query = 	'INSERT INTO COURSE1 (CATEGORY, TITLE, DESCRIPTION, CONTENT, IMAGE)' \
								'	VALUES (?, ?, ?, ?, ?)'

_course_table_update_query = 	'UPDATE COURSE1 SET' \
								'	ID = ?, CATEGORY = ?, TITLE = ?, DESCRIPTION = ?, CONTENT = ?, IMAGE = ?' \
								'	WHERE ID = ?'
_course_table_delete_query = 	'DELETE FROM COURSE1' \
								'	WHERE ID = ?'
_course_table_create_query = 	'CREATE TABLE COURSE1 (' \
								'	ID SERIAL PRIMARY KEY,' \
								'	CATEGORY VARCHAR(255) NOT NULL,' \
								'	TITLE VARCHAR(255) NOT NULL,' \
								'	DESCRIPTION VARCHAR(255) NOT NULL,' \
								'	CONTENT VARCHAR(255) NOT NULL,' \
								'	IMAGE MEDIUMBLOB NOT NULL' \
								');'



def GetUsersList():
	connection = ConnectToDB()
	cursor = connection.cursor()
	try:
		cursor.execute(_user_table_select_query)
		table = cursor.fetchall()
	except:
		cursor.execute(_user_table_create_query)
		connection.commit()
		table = ()

	connection.close()
	return [{'ID': data[0]} for data in table]

def AddUser(user_id):
	connection = ConnectToDB()
	cursor = connection.cursor()
	cursor.execute(_user_table_insert_query, (user_id,))
	connection.commit()
	connection.close()



def GetAdminsList():
	connection = ConnectToDB()
	cursor = connection.cursor()
	try:
		cursor.execute(_admin_table_select_query)
		table = cursor.fetchall()
	except:
		cursor.execute(_admin_table_create_query)
		connection.commit()
		table = ()

	connection.close()
	return [{'ID': data[0]} for data in table]

def AddAdmin(admin_id):
	connection = ConnectToDB()
	cursor = connection.cursor()
	cursor.execute(_admin_table_insert_query, (admin_id,))
	connection.commit()
	connection.close()


def GetCoursesDict():
	connection = ConnectToDB()
	cursor = connection.cursor()
	try:
		cursor.execute(_course_table_select_query)
		table = cursor.fetchall()
	except:
		cursor.execute(_course_table_create_query)
		connection.commit()
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
	connection.close()
	return courses_dict

def AddCourse(course):
	connection = ConnectToDB()
	cursor = connection.cursor()
	cursor.execute(_course_table_insert_query, (course.Category, course.Title, course.Description, course.Content, course.Image,))
	connection.commit()
	connection.close()

def DeleteCourse_byID(id):
	connection = ConnectToDB()
	cursor = connection.cursor()
	cursor.execute(_course_table_delete_query, (id,))
	connection.commit()
	connection.close()


def ConnectToDB():
	try:
		connection = psycopg2.connect(
			user="khjhfboutmiizc",
			password="390f718a8b0e583cb6fe6120fbb479e364690b6f9140f4284791553d3b1f5574",
			host="ec2-79-125-30-28.eu-west-1.compute.amazonaws.com",
			port="5432",
			database="dfa74tvmhupjn0"
		)
		connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		return connection
	except (Exception, Error) as error:
		print(error)