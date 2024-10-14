# a code that connects to the Postgres database

import psycopg
from datetime import datetime

from KaptyorkaApp.models import Cathegory
from .classes import *

class DBConnection:
	def __init__(self, user, password, host="127.0.0.1", port="5432", db="rentequipmentservicedb"):
		self.host = host
		self.port = port
		self.db = db
		self.user = user
		self.password = password

	def get_connection_credentials(self):
		return "host="+self.host+" port="+self.port+" dbname="+self.db+" user="+self.user+" password='"+self.password+"'"

	def connect(self):
		try:
			self.conn = psycopg.connect(host=self.host, port=self.port, dbname=self.db, user=self.user, password=self.password)
		except:
			print("Unable to connect to database")

	def create_accounting(self, start_date, end_date):
		with psycopg.connect(self.get_connection_credentials()) as conn:
			with conn.cursor() as cur:
				start_datetime = start_date + ' ' + datetime.datetime.now().strftime("%H:%M:%S")
				result = cur.execute("INSERT INTO rent_accounting (username, comment, start_date, end_date) VALUES (%s, %s, %s, %s)", (self.user, '', start_date, end_date))

	def add_equipment_to_accounting(self, equipment_id):
		with psycopg.connect(self.get_connection_credentials()) as conn:
			with conn.cursor() as cur:

				acc_id = cur.execute("SELECT id FROM public.rent_accounting ra WHERE ra.username = %s ORDER BY id DESC LIMIT 1", [self.user]).fetchone()[0]
				result = cur.execute("INSERT INTO public.rented_equipment (accounting, deterioration, equipment) VALUES (%s, %s, %s)", (acc_id, 0, equipment_id))

	def add_countable_equipment_to_accounting(self, equipment_id, amount):
		with psycopg.connect(self.get_connection_credentials()) as conn:
			with conn.cursor() as cur:

				acc_id = cur.execute("SELECT id FROM public.rent_accounting ra WHERE ra.username = %s ORDER BY id DESC LIMIT 1", [self.user]).fetchone()[0]
				result = cur.execute("INSERT INTO public.rented_countable_equipment (accounting, equipment, amount, returned_amount) VALUES (%s, %s, %s, %s)", (acc_id, equipment_id, amount, 0))	

	def get_all_user_accountings(self):
		with psycopg.connect(self.get_connection_credentials()) as conn:
			with conn.cursor() as cur:

				acc_id = cur.execute("SELECT * FROM public.rent_accounting ra WHERE ra.username = %s ORDER BY id DESC", [self.user]).fetchall()

				user_rent_accountings = []

				for acc in acc_id:
					user_rent_accounting = UserRentAccounting(acc[0], acc[3], acc[4], acc[5], acc[6]) 
					user_rent_accountings.append(user_rent_accounting)
					acc_unique_equipment = cur.execute("SELECT * FROM public.rented_equipment WHERE accounting = %s", [acc[0]]).fetchall()
					for eq in acc_unique_equipment:
						eq_info = cur.execute("SELECT id, name, cathegory, price FROM public.equipment WHERE id = %s", [eq[2]]).fetchone()
						user_rent_accounting.equipment_list.append(UserRentedUniqueEquipment(eq_info[0], eq_info[1], eq_info[2], eq_info[3], 1))
					
					acc_countable_equipment = cur.execute("SELECT * FROM public.rented_countable_equipment WHERE accounting = %s", [acc[0]]).fetchall()
					for eq in acc_countable_equipment:
						eq_info = cur.execute("SELECT id, name, cathegory, price FROM public.equipment WHERE id = %s", [eq[1]]).fetchone()
						user_rent_accounting.equipment_list.append(UserRentedCountableEquipment(eq_info[0], eq_info[1], eq_info[2], eq_info[3], eq[2], eq[3]))

				return user_rent_accountings
			
	def get_cathegory_by_path(self, path):
		parent_cathegory = None

		path_list = path.split('/')
		parent_dir = path_list[0]
		parent_cathegory_request = Cathegory.objects.filter(name=parent_dir)

		parent_cathegory = None

		if len(parent_cathegory_request):
			parent_cathegory = parent_cathegory_request[0]
		else:
			parent_cathegory = Cathegory.objects.create(name=parent_dir)

		curr_cathegory = parent_cathegory

		for curr_cathegory_name in path_list[1:]:
			curr_cathegory_request = Cathegory.objects.filter(name=curr_cathegory_name, parent_cathegory=parent_cathegory)

			if len(curr_cathegory_request):
				curr_cathegory = curr_cathegory_request[0]
			else:
				curr_cathegory = Cathegory.objects.create(name=curr_cathegory_name, parent_cathegory=parent_cathegory)
				parent_cathegory = curr_cathegory
		
		return curr_cathegory

	def create_new_equipment(self, new_equipment):
		new_equipment_id = -1
		with psycopg.connect(self.get_connection_credentials()) as conn:
			with conn.cursor() as cur:
				result = cur.execute("INSERT INTO equipment (name, cathegory, price, img_path, description, amount) VALUES (%s, %s, %s, %s, %s, %s)",
				                     (new_equipment.name, self.get_cathegory_id(new_equipment.cathegory), new_equipment.price, './', new_equipment.description, new_equipment.amount))
				
				new_equipment_id = cur.execute("SELECT id FROM equipment WHERE name = %s AND cathegory = %s AND description = %s AND amount = %s", (
										new_equipment.name,
										self.get_cathegory_id(new_equipment.cathegory),
										new_equipment.description,
										new_equipment.amount)
									).fetchone()[0]
				if new_equipment.amount == 1:

					unique_equipment_deterioration = cur.execute(
										"INSERT INTO unique_equipment (id, deterioration) VALUES (%s, %s)", (new_equipment_id, 1))
		
		return new_equipment_id
	
	def update_equipment(self, equipment_id, new_equipment):
		with psycopg.connect(self.get_connection_credentials()) as conn:
			with conn.cursor() as cur:
				result = cur.execute("UPDATE equipment SET name = %s, cathegory = %s, price = %s, img_path = %s, description = %s, amount = %s WHERE id = %s",
				                     (new_equipment.name, self.get_cathegory_id(new_equipment.cathegory), new_equipment.price, './', new_equipment.description, new_equipment.amount, equipment_id))
		
	def delete_equipment(self, equipment_id):
		with psycopg.connect(self.get_connection_credentials()) as conn:
			with conn.cursor() as cur:
				del_all_rented_equipment = cur.execute("DELETE FROM rented_equipment WHERE equipment = %s", [equipment_id])
				del_all_rented_countable_equipment = cur.execute("DELETE FROM rented_countable_equipment WHERE equipment = %s", [equipment_id])
				del_from_unique_equipment = cur.execute("DELETE FROM unique_equipment WHERE id = %s", [equipment_id])
				result = cur.execute("DELETE FROM equipment WHERE id = %s", [equipment_id])
					
	def get_all_accountings(self):

		accountings = []

		with psycopg.connect(self.get_connection_credentials()) as conn:
			with conn.cursor() as cur:
				raw_accountings = cur.execute("SELECT * FROM rent_accounting").fetchall()
				accountings = []
				for accounting in raw_accountings:
					user_rent_accounting = UserRentAccounting(accounting[0], accounting[3], accounting[4], accounting[5], accounting[6]) 
					accounting_info = {}
					accounting_info['username'] = accounting[1]
					user_info = cur.execute("SELECT * FROM users WHERE username = %s", [accounting[1]]).fetchall()[0]
					accounting_info['full_name'] = " ".join([user_info[1], user_info[2]])
					accounting_info['email'] = user_info[3]
					accounting_info['phone'] = user_info[4]
					accounting_info['confidence_factor'] = user_info[5]
					accounting_info['accounting'] = user_rent_accounting
					accounting_info['date_interval'] = beauty_date_interval(user_rent_accounting.start_date, user_rent_accounting.end_date, True, True)
					accounting_info['fact_start_date'] = ""
					if user_rent_accounting.fact_start_date != None:
						accounting_info['fact_start_date'] = beauty_date(user_rent_accounting.fact_start_date)

					accounting_info['fact_end_date'] = ""
					if user_rent_accounting.fact_end_date != None:
						accounting_info['fact_end_date'] = beauty_date(user_rent_accounting.fact_end_date)					


					acc_unique_equipment = cur.execute("SELECT * FROM public.rented_equipment WHERE accounting = %s", [accounting[0]]).fetchall()
					for eq in acc_unique_equipment:
						eq_info = cur.execute("SELECT id, name, cathegory, price FROM public.equipment WHERE id = %s", [eq[2]]).fetchone()
						user_rent_accounting.equipment_list.append(UserRentedUniqueEquipment(eq_info[0], eq_info[1], eq_info[2], eq_info[3], 1))
					
					acc_countable_equipment = cur.execute("SELECT * FROM public.rented_countable_equipment WHERE accounting = %s", [accounting[0]]).fetchall()
					for eq in acc_countable_equipment:
						eq_info = cur.execute("SELECT id, name, cathegory, price FROM public.equipment WHERE id = %s", [eq[1]]).fetchone()
						user_rent_accounting.equipment_list.append(UserRentedCountableEquipment(eq_info[0], eq_info[1], eq_info[2], eq_info[3], eq[2], eq[3]))
					
					accountings.append(accounting_info)
		
		return accountings
	
	def set_fact_start_accounting_date(self, id, start_date):
		with psycopg.connect(self.get_connection_credentials()) as conn:
			with conn.cursor() as cur:
				cur.execute("UPDATE rent_accounting SET fact_start_date = %s WHERE id = %s", (start_date, id))
	
	def set_fact_end_accounting_date(self, id, end_date):
		with psycopg.connect(self.get_connection_credentials()) as conn:
			with conn.cursor() as cur:
				cur.execute("UPDATE rent_accounting SET fact_end_date = %s WHERE id = %s", (end_date, id))

		
