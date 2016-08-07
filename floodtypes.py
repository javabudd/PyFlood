import sqlite3
import json


class FloodTypes:
	def __init__(self):
		return

	@staticmethod
	def get_connection():
		return sqlite3.connect('flood_types.db')

	@classmethod
	def get_types(cls):
		con = cls.get_connection()
		cursor = con.cursor()
		cursor.execute("SELECT * FROM flood_types")
		results = cursor.fetchall()
		con.close()

		flood_types = []
		for result in results:
			flood_type = FloodType
			flood_type.set_type_id(result.__getitem__(0))
			flood_type.set_name(result.__getitem__(1))
			flood_type.set_socket_type(result.__getitem__(2))
			flood_type.set_socket_options(result.__getitem__(3))
			flood_types.append(flood_type)

		return flood_types

	@classmethod
	def get_by_type(cls, type_id):
		con = cls.get_connection()
		cursor = con.cursor()
		cursor.execute('SELECT * FROM flood_types ft WHERE ft.id = ?', (type_id,))
		result = cursor.fetchone()
		con.close()

		flood_type = FloodType

		flood_type.set_type_id(result.__getitem__(0))
		flood_type.set_name(result.__getitem__(1))
		flood_type.set_socket_type(result.__getitem__(2))
		flood_type.set_socket_options(result.__getitem__(3))

		return flood_type

	@classmethod
	def insert_row(cls, name):
		con = cls.get_connection()
		con.execute('INSERT INTO flood_types (\"name\") VALUES (?)', (name,))
		con.commit()
		con.close()

	@classmethod
	def delete_row(cls, type_id):
		con = cls.get_connection()
		con.execute('DELETE FROM flood_types WHERE id = ?', (type_id,))
		con.commit()
		con.close()


class FloodType:
	type_id = None
	name = None
	socket_type = None
	socket_options = {}

	@classmethod
	def get_type_id(cls):
		return cls.type_id

	@classmethod
	def set_type_id(cls, type_id):
		cls.type_id = type_id

		return cls

	@classmethod
	def get_name(cls):
		return cls.name

	@classmethod
	def set_name(cls, name):
		cls.name = name

		return cls

	@classmethod
	def get_socket_type(cls):
		return cls.socket_type

	@classmethod
	def set_socket_type(cls, socket_type):
		cls.socket_type = socket_type

		return cls

	@classmethod
	def get_socket_options(cls):
		return json.loads(cls.socket_options)

	@classmethod
	def set_socket_options(cls, socket_options):
		cls.socket_options = socket_options

		return cls

