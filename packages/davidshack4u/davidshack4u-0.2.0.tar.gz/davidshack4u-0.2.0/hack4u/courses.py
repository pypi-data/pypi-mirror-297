#!/usr/bin/env python3

class Academy:
	def __init__(self, name, duration, link):
		self.name = name
		self.duration = duration
		self.link = link

	def __repr__(self):
		return f"La clase de {self.name} dura [{self.duration} horas]. Link: {self.link}"


courses = [
	Academy("Introduccion a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/"),
	Academy("Personalizacion de Linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/"),
	Academy("Introduccion al hacking", 55, "https://hack4u.io/cursos/introduccion-al-hacking/"),
	Academy("Python Ofensivo",35,"https://hack4u.io/cursos/python-ofensivo/")
]

def list_courses():
	for course in courses:
		print(course)

def search_course_by_name(name):
	for course in courses:
		if course.name == name:
			return course
	return None
