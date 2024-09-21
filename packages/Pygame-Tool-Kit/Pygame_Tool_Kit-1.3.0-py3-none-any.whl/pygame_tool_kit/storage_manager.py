"""
Module containing the Storage_Manager class for managing the loading and saving of data from JSON files.

Also contains the DATABASE_MANAGER constant for managing the interaction with a SQLite database.
"""
from json import load, dump

from .config import STORAGE_PATH, STORAGE_WITH_JSON, STORAGE_DATABASE_NAME

class Storage_Manager ():
	"""
	Manages the loading and saving of data from JSON files.

	Args:
		at (str): The name of the data to load.
		static (bool): If the data is static, it will be loaded from the static.json file.

	Returns:
		dict: The loaded data.
	"""

	def load (self, at : str, static : bool = True) -> dict:

		if (static):
			with open (f"{STORAGE_PATH}/static.json", "r") as file:
				return load (file)[at]
		
		else:
			with open (f"{STORAGE_PATH}/dynamic/{at}.json", "r") as file:
				return load (file)[at]

	def save (self, at : str, data : any) -> None:

		with open (f"{STORAGE_PATH}/dynamic/{at}.json", "w") as file:
			dump ({at : data}, file, indent = 4)

STORAGE_MANAGER : Storage_Manager = Storage_Manager () if (STORAGE_WITH_JSON) else None

if (STORAGE_DATABASE_NAME):
	from py_simple_select import Database_Manager
	DATABASE_MANAGER : Database_Manager = Database_Manager (f"{STORAGE_PATH}/{STORAGE_DATABASE_NAME}")

else:
	DATABASE_MANAGER = None