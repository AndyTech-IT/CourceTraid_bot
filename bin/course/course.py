class Course:
	ID: int
	Category: str
	Title: str
	Description: str
	Content: str
	Image: bytes
	def __init__(self, category, title, description, content, image, id=None):
		self.Category = category
		self.Title = title
		self.Description = description
		self.Content = content
		self.Image = image
		self.ID = id

	pass

class Courses_List:
	def __init__(self, courses_dicts):
		self._coursesid_by_category_dict = {}
		self._courses_by_id_dict = {}
		for id in courses_dicts:
			self.AddCourse(id, courses_dicts[id])
	
	def AddCourse(self, id, course_dict):
		course = Course(
			course_dict['CATEGORY'], 
			course_dict['TITLE'], 
			course_dict['DESCRIPTION'],
			course_dict['CONTENT'],
			course_dict['IMAGE'],
			id
		)
		if id > 99999:
			print(f'Внимание! Слишком большой идентификатор {id}!')

		if course.Category not in self._coursesid_by_category_dict:
			self._coursesid_by_category_dict.update({course.Category: []})

		self._coursesid_by_category_dict[course.Category].append(id)
		self._courses_by_id_dict.update({id: course})

	def Try_GetCourseInfo_and_Image_byMessage(self, message):
		course_id = int(message.text.rpartition(' ')[2])
		if course_id in self._courses_by_id_dict:
			course = self._courses_by_id_dict[course_id]
			message = 	f'Курс {course.Category} "{course.Title}":\n\n' \
						f'	{course.Description}\n\n' \
						f'{course.Content}'
			return 	message, course.Image
		else:
			return False

	def Try_GetCourseInfo_and_Image_byCallback(self, callback):
		course_id = int(callback.data.rpartition(' ')[2])
		if course_id in self._courses_by_id_dict:
			course = self._courses_by_id_dict[course_id]
			message = 	f'Курс {course.Category} "{course.Title}":\n\n' \
						f'	{course.Description}\n\n' \
						f'{course.Content}'
			return 	message, course.Image
		else:
			return False

	def GetCourses_InfoList(self):
		info_list = []
		for category in self._coursesid_by_category_dict:
			category_courses_info = ''
			for id in self._coursesid_by_category_dict[category]:
				course = self._courses_by_id_dict[id]
				category_courses_info += f'ID: {id:>05d}| "{course.Title}" - {course.Description}\n'

			info_list.append(f'Категория: "{category}"')
			info_list.append(category_courses_info)
		return info_list

	def GetCourses(self):
		return [self._courses_by_id_dict[id] for id in self._courses_by_id_dict]

	def GetCategorys_List(self):
		return [category for category in self._coursesid_by_category_dict]

	def GetCourse_ByID(self, id):
		return self._courses_by_id_dict[id]
	pass