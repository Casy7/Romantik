
import datetime
from venv import create
import pytz
import six
import base64
import uuid

from KaptyorkaApp.models import *
from RomantikApp.models import *

from django.contrib.auth.models import AnonymousUser
from django.core.files.base import ContentFile
from romantik.settings import secret_settings


def get_post_raiting(post):
	upvotes = UpVote.objects.filter(news=post)
	downvotes = DownVote.objects.filter(news=post)
	int_total_raiting = upvotes.count() - downvotes.count()
	total_raiting = str(int_total_raiting)
	if int_total_raiting > 0:
		total_raiting = "+"+str(int_total_raiting)
	else:
		total_raiting = str(int_total_raiting)
	return total_raiting


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
				context['_user_has_avatar'] = True
				context['_user_avatar'] = user_profile.avatar

	if args != None:
		for arg in args:
			context[arg] = args[arg]

	return context


def is_user_authenticated(request):
	user = request.user
	user_validation_properties = [
		request.user != None,
		not request.user.is_anonymous,
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
		elif 4 < number < 21:
			return ''
		elif number % 10 == 1:
			return 'у'
		elif number % 10 == 0:
			return ''
		elif number % 10 < 5:
			return 'и'

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
		elif datetime_delta.seconds < 24 * 60 * 60:
			return str(datetime_delta.seconds // 60 // 60) + " годин"+insert_u_or_y(datetime_delta.seconds//60//60)+" тому"
	elif datetime_delta.days < 60:
		return str(datetime_delta.days) + " " + return_ukr_day(datetime_delta.days) + " тому"
	elif datetime_delta.days < 600:
		return str(datetime_delta.days // 30) + " "+return_ukr_month(datetime_delta.days//30)+" тому"
	else:
		return raw_datetime.strftime('%d, %b %Y')
