
import datetime
from email import message
from venv import create
import pytz
import six
import base64
import uuid
import json

from sympy import im
from ..models import *
from django.contrib.auth.models import AnonymousUser
from django.core.files.base import ContentFile
from romantik.settings import secret_settings

from telethon import TelegramClient
import asyncio
from telethon import events
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async, async_to_sync





class TelergamParser:
	def __init__(self):
		self.channel = 'gGIj6w7K51avX'
		self.api_id = secret_settings["tg_api_id"]
		self.api_hash = secret_settings["tg_api_hash"]
		self.client = TelegramClient('RomantikClient', self.api_id, self.api_hash)

	def check_for_updates(self):
		return asyncio.run(self.a_check_for_updates())

	async def a_check_for_updates(self):
		async with self.client:
			last_messages = await self.client.get_messages(self.channel, limit=1)
		
		if not len(last_messages):
			return None
		
		last_message = last_messages[0]
		prev_parsed_data = await self.get_parser_data()

		if last_message.id != prev_parsed_data.last_post_id:
			return True
		
		return False

	async def handle_message(event):
		message = event.message
		print(message.text)
		post_media = []
		saved_path = await message.download_media(file='./telegram/')
		post_media.append(saved_path)
		print(f"Photo saved at: {saved_path}")
		# print(post_media)
	
	def load_updates(self):
		messages = asyncio.run(self.a_load_updates())
		return messages

	async def a_load_updates(self):
		last_messages = []
		async with self.client:
			last_messages = await self.client.get_messages(self.channel, limit=10)
		
		result_messages = []

		for message in last_messages:
			message_props = {
				"id": message.id,
				"date": message.date,
				"message": message.message,
				"media": []
			}

			async with self.client:
				saved_path = await message.download_media(file='../../media/telegram_forced/')
			message_props["media"].append(saved_path)

			result_messages.append(message_props)
		
		print(result_messages)
					


	@database_sync_to_async
	def get_parser_data(self):
		parser = TelegramChannelParserData.objects.filter(channel=self.channel)
		print("___________________________________")
		if len(parser):
			return parser[0]
		else:
			parser = TelegramChannelParserData(channel=self.channel, last_post_id=-1, last_update=datetime.datetime(2023, 6, 1))
			parser.save()
		return parser







# async def start_client():
# 	client = TelegramClient('RomantikClient', secret_settings["tg_api_id"], secret_settings["tg_api_hash"])
# 	print("Client started")
# 	@client.on(events.NewMessage(chats='gGIj6w7K51avX'))
# 	async def handle_message(event):
# 		message = event.message
# 		print(message.text)

# 		post_media = []
# 		saved_path = await message.download_media(file='./telegram/')
# 		post_media.append(saved_path)
# 		print(f"Photo saved at: {saved_path}")
# 		print(post_media)
# 		await client.send_message('me', 'Hello to myself!')
# 	async with client:
# 		await client.run_until_disconnected()


# def start_observer():
# 	print("Observer started")
# 	loop = asyncio.new_event_loop()
# 	asyncio.set_event_loop(loop)
# 	async_result = loop.run_until_complete(start_client())
# 	loop.close()

  
	
	
	
# async for message in client.iter_messages('tk_romantik', limit=5):
#     await client.send_message('me', 'Hello to myself!')

#     client._download_photo(message.media, './image.png', message.media.photo.date, message.id, "")
#     print(message.id, message.text)
#     print("\n________________________________________\n")


def full_name(user):
	if user.last_name != '' and user.first_name != '':
		return user.first_name+' '+user.last_name
	elif user.first_name != '':
		return user.first_name
	elif user.last_name != '':
		return user.last_name
	else:
		return user.username


def base_context(request, **args):
	context = {}
	user = request.user

	context['title'] = 'none'
	context['user'] = 'none'
	context['header'] = 'none'
	context['error'] = 0
	context['message'] = ''
	context['is_superuser'] = False
	context['self_user_has_avatar'] = False
	context['page_name'] = 'default'

	if is_user_authenticated(request):

		context['username'] = user.username
		context['full_name'] = full_name(user)
		context['user'] = user

		if request.user.is_superuser:
			context['is_superuser'] = True

		if UserInfo.objects.filter(user=user).exists():
			user_profile = UserInfo.objects.get(user=user)
			if user_profile.avatar:
				context['self_user_has_avatar'] = True
				context['self_user_avatar'] = user_profile.avatar

	if args != None:
		for arg in args:
			context[arg] = args[arg]

	return context


def is_user_authenticated(request):
	user = request.user
	user_validation_properties = [
		type(request.user) != AnonymousUser,
		len(User.objects.filter(username=user.username)) != 0,
		user.is_active
	]
	return not False in user_validation_properties


def decode_base64_file(data):

	def get_file_extension(file_name, decoded_file):
		import imghdr

		extension = imghdr.what(file_name, decoded_file)
		extension = "jpg" if extension == "jpeg" else extension

		return extension

	if isinstance(data, six.string_types):
		if 'data:' in data and ';base64,' in data:
			header, data = data.split(';base64,')

		try:
			decoded_file = base64.b64decode(data)
		except TypeError:
			TypeError('invalid_image')

		file_name = str(uuid.uuid4())[:12]
		file_extension = get_file_extension(file_name, decoded_file)

		complete_file_name = "%s.%s" % (file_name, file_extension, )

		return ContentFile(decoded_file, name=complete_file_name)


def get_avatar(user):

	if len(UserInfo.objects.filter(user=user)):
		user_profile = UserInfo.objects.get(user=user)
	else:
		user_profile = UserInfo.objects.create(user=user)
		user_profile.save()

	avatar_url = ''
	
	try:
		avatar_url = user_profile.avatar.url
	except:
		avatar_url = ''

	return avatar_url


def beautify_datetime(raw_datetime):
	raw_datetime = raw_datetime
	now_datetime = raw_datetime.now(pytz.UTC)
	datetime_delta = now_datetime - raw_datetime

	def insert_u_or_y(number):
		if number == 0:
			return ''
		if 4 <number < 21:
			return ''
		elif number % 10 == 1:
			return 'у'
		elif number % 10 < 5:
			return 'и'
		else:
			return ''


	def return_ukr_day(days):
		if days < 4:
			return 'дні'
		elif 4 < days < 21:
			return 'днів'
		elif days % 10 == 1:
			return 'день'
		elif days % 10 < 5:
			return 'дні'
		else:
			return 'днів'
		
	def return_ukr_month(months):
		if months < 5:
			return 'місяці'
		else:
			return 'місяців'
	
		
	if datetime_delta.days < 2:
		if datetime_delta.seconds < 60:
			return str(datetime_delta.seconds) + " секунд"+insert_u_or_y(datetime_delta.seconds)+" тому"
		elif datetime_delta.seconds < 60 * 60:
			return str(datetime_delta.seconds // 60) + " хвилин"+insert_u_or_y(datetime_delta.seconds//60)+" тому"
		elif datetime_delta.seconds < 24 *  60 * 60:
			return str(datetime_delta.seconds // 60 // 60) + " годин"+insert_u_or_y(datetime_delta.seconds//60//60)+" тому"
	elif datetime_delta.days < 60:
		return str(datetime_delta.days) + " " + return_ukr_day(datetime_delta.days) + " тому"
	elif datetime_delta.days < 600:
		return str(datetime_delta.days // 30) + " "+return_ukr_month(datetime_delta.days//30)+" тому"
	else:
		return raw_datetime.strftime('%d, %b %Y')

