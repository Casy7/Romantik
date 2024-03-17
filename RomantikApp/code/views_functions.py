
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
        self.channel = 'tk_romantik'
        self.api_id = secret_settings["tg_api_id"]
        self.api_hash = secret_settings["tg_api_hash"]
        self.client = TelegramClient('RomantikClient', self.api_id, self.api_hash)

    def get_last_forced_post_info(self):
        last_post_tg_id = TelegramPostId.objects.filter(channel=self.channel).order_by('-post_tg_id')
        if len(last_post_tg_id):
            last_post_tg_id = last_post_tg_id[0]

            post = last_post_tg_id.post

            post_dict = {
                "id": post.id,
                "tg_id": last_post_tg_id.post_tg_id,
                "datetime": post.datetime,
            }
            return post_dict

        return {
            "id": -1,
            "tg_id": -1,
            "datetime": datetime.datetime(2023, 6, 1)
        }

    @database_sync_to_async
    def a_get_last_forced_post_info(self):
        return self.get_last_forced_post_info()

    async def handle_message(event):
        message = event.message
        print(message.text)
        post_media = []
        saved_path = await message.download_media(file='./telegram/')
        post_media.append(saved_path)
        print(f"Photo saved at: {saved_path}")
        # print(post_media)

    def load_updates(self, max_posts_amount=30, min_date=datetime.datetime(2023, 6, 1)):

        # #
        # self.client.loop.close()
        # self.client = TelegramClient('RomantikClient', self.api_id, self.api_hash)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        messages = loop.run_until_complete(self.a_load_updates(
            max_posts_amount=max_posts_amount, min_date=min_date))
        loop.close()
        return messages

    async def a_load_updates(self, offset_id=0, rec_result_messages=[], start_counter_from=0, max_posts_amount=30, min_date=datetime.datetime(2023, 6, 1)):

        PARSE_THIS_AMOUNT_AT_ONCE = 3

        result_messages = rec_result_messages
        last_messages = []

        async with self.client:
            last_messages = await self.client.get_messages(self.channel, limit=PARSE_THIS_AMOUNT_AT_ONCE, offset_id=offset_id, offset_date=min_date)

        last_checked_id = -1
        for message in last_messages:

            last_post_info = await self.a_get_last_forced_post_info()

            if message.id <= last_post_info["id"] or message.date.timestamp() <= last_post_info["datetime"].timestamp():
                return result_messages

            if start_counter_from >= max_posts_amount:
                return result_messages

            message_props = {
                "id": message.id,
                "date": message.date,
                "message": message.message,
                "media": []
            }

            offset_id = message.id
            print("Message parsed from TG: ", message.id)
            start_counter_from += 1

            async with self.client:
                saved_path = await message.download_media(file="./RomantikApp/media/telegram_forced/")
            message_props["media"].append(saved_path)

            result_messages.append(message_props)
        await self.a_load_updates(offset_id=offset_id, rec_result_messages=result_messages, start_counter_from=start_counter_from, max_posts_amount=max_posts_amount)

        # print(result_messages)
        return result_messages

    def force_posts_to_db(self, max_posts_amount=30, min_date=datetime.datetime(2023, 6, 1)):
        messages = self.load_updates(
            max_posts_amount=max_posts_amount, min_date=min_date)

        posts_author = User.objects.get(username="romantik")
        for message in messages:
            res_message = "<p>" + message["message"] + "</p>"
            res_message = res_message.replace("\n", "<br>")
            if message["media"][0] is not None:
                media_path = message["media"][0].replace("./RomantikApp", "")
                if media_path.split(".")[-1].lower() in ("mp4", "mov", "webm"):
                    res_message += """<video class="image_resized" style="width:80%;" src=" """ + \
                        media_path + """"></video>"""
                else:
                    res_message += """<img class="image_resized" style="width:80%;" src=" """ + \
                        media_path + """">"""

            if not TelegramPostId.objects.filter(channel=self.channel, post_tg_id=message["id"]).exists():
                post = NewsPost(user=posts_author, datetime=message["date"], content=res_message, img_paths={})
                post.save()

                post_tg_id = TelegramPostId(channel=self.channel, post_tg_id=message["id"], post=post)
                post_tg_id.save()


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
        if 4 < number < 21:
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
        elif datetime_delta.seconds < 24 * 60 * 60:
            return str(datetime_delta.seconds // 60 // 60) + " годин"+insert_u_or_y(datetime_delta.seconds//60//60)+" тому"
    elif datetime_delta.days < 60:
        return str(datetime_delta.days) + " " + return_ukr_day(datetime_delta.days) + " тому"
    elif datetime_delta.days < 600:
        return str(datetime_delta.days // 30) + " "+return_ukr_month(datetime_delta.days//30)+" тому"
    else:
        return raw_datetime.strftime('%d, %b %Y')
