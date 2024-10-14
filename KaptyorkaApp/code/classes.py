from .data_conventers import *

class UserRentedUniqueEquipment:
	def __init__(self, id, name, cathegory, price, amount):
		self.id = id
		self.name = name
		self.cathegory = cathegory
		self.price = price

class UserRentedCountableEquipment:
	def __init__(self, id, name, cathegory, price, amount, returned_amount):
		self.id = id
		self.name = name
		self.cathegory = cathegory
		self.price = price
		self.amount = amount
		self.returned_amount = returned_amount

class UserRentAccounting:
	def __init__(self, id, start_date, end_date, fact_start_date, fact_end_date):
		self.id = id
		self.start_date = start_date
		self.end_date = end_date
		self.fact_start_date = fact_start_date
		self.fact_end_date = fact_end_date
		self.equipment_list = []

class NewEquipment:
	def __init__(self, name, cathegory, description, price, amount):
		self.name = name
		self.cathegory = cathegory
		self.description = description
		self.price = price
		self.amount = amount