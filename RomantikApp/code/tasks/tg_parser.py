import datetime
import time
from telethon import TelegramClient
from telethon import events
import requests
import json
import os

secret_settings = {
	"api_id": 31415926,
	"api_hash": "your_hash_code",
	"production": False,
	"channel": "tk_romantik"
}

previous_parsing_results = {
	"last_post_tg_id": -1,
	"already_parsed_posts": [],
}


class TelergamParser:
	def __init__(self, channel, api_id, api_hash, client_name="DefaultClient"):
		self.channel = channel
		self.api_id = api_id
		self.api_hash = api_hash
		self.client_name = client_name
		self.client = TelegramClient(self.client_name, self.api_id, self.api_hash)

	def message_in_ids(self, message_id, ids_list):
		for id in ids_list:
			ids_in_one_post = id.split("|")
			if str(message_id) in ids_in_one_post:
				return True
		return False

	async def download_media_from_message(self, message, path="../../media/telegram_forced/"):
		media_path = await message.download_media(file=path)
		media_path = media_path.replace("\\", "/")

		if media_path.split("/")[-1][0] == ".":
			new_media_path = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + media_path
			await os.rename(media_path, new_media_path)
			media_path = new_media_path

		media_size = os.stat(media_path).st_size
		for old_media_path in os.listdir(path):
			old_media_path = path+old_media_path
			if old_media_path != media_path and media_size == os.stat(old_media_path).st_size:

				if old_media_path.split(" ")[0] == media_path.split(" ")[0]:
					os.remove(media_path)
					return old_media_path

		return media_path

	async def a_load_last_posts(self,  max_posts_amount=30):

		last_messages = []
		result_messages = []

		last_messages = await self.client.get_messages(self.channel, limit=max_posts_amount)

		last_grouped_id = -1

		for message in last_messages:

			if self.message_in_ids(message.id, previous_parsing_results["already_parsed_posts"]):
				continue

			if message.grouped_id is not None and last_grouped_id == message.grouped_id:
				last_message = result_messages[-1]
				last_message["id"] += "|"+str(message.id)
				last_message["message"] += " " + message.message
				saved_path = await self.download_media_from_message(message)
				last_message["media"].append(saved_path)
				continue

			last_grouped_id = message.grouped_id if message.grouped_id is not None else -1

			message_props = {
				"id": str(message.id),
				"date": message.date,
				"message": message.message,
				"media": []
			}

			saved_path = await message.download_media(file="../../media/telegram_forced/")
			message_props["media"].append(saved_path)

			result_messages.append(message_props)
			print("Message parsed from TG: ", message.id)

		return result_messages

	async def get_latest_posts(self, max_posts_amount=30):
		messages = await self.a_load_last_posts(max_posts_amount=max_posts_amount)

		for message in messages:
			if message["message"] is None:
				message["message"] = ""
			res_message = "<p>" + message["message"] + "</p>"
			res_message = res_message.replace("\n", "<br>")
			if len(message["media"]):
				res_message += "<div class='image-from-tg-container'>"
				for media in message["media"]:

					if media is None:
						continue
					media_path = media.replace("./RomantikApp", "")
					if media_path.split(".")[-1].lower() in ("mp4", "mov", "webm"):
						res_message += """<video class="image-from-tg" src=" """ + media_path + """"></video>"""
					else:
						res_message += """<img class="image-from-tg" src=" """ + media_path + """">"""
				res_message += "</div>"

			message["message"] = res_message
			message["date"] = str(message["date"])

		return messages


if __name__ == '__main__':
	try:
		with open('../../../secret.json') as f:
			d = json.load(f)
			secret_settings.update(d)
	except:
		pass

	parser = TelergamParser(secret_settings["channel"], secret_settings["tg_api_id"], secret_settings["tg_api_hash"])

	@parser.client.on(events.NewMessage(chats='gGIj6w7K51avX'))
	async def update_posts(event=None):

		try:
			async with open('./parser_data.json') as f:
				d = await json.load(f)
				await previous_parsing_results.update(d)
		except:
			pass

		messages = await parser.get_latest_posts(20)

		url = "https://www.romantik.space/get_posts_from_tg/" if secret_settings["production"] else "http://127.0.0.1:8000/get_posts_from_tg/"

		session = requests.Session()
		get_response = session.get(url)

		csrftoken = session.cookies.get('csrftoken', None)

		headers = {
			"X-CSRFToken": csrftoken,
			"Content-Type": "application/json",
			"X-Requested-With": "XMLHttpRequest",
			"csrftoken": csrftoken,
			"Referer": url
		}
		
		session.headers.update(headers)
		

		post_data = {"messages": messages, "secret_key": secret_settings["secret_key"], "csrfmiddlewaretoken": csrftoken, "next": "/"}
		post_response = session.post(url, data=json.dumps(post_data), json=post_data, headers=headers)
		result = json.loads(post_response.text)
		print("Result: ", result)

		if result["result"] == "success":
			message_ids = [message["id"] for message in messages]
			previous_parsing_results["already_parsed_posts"].extend(message_ids)
			deduplicated_list = list()

			[deduplicated_list.append(item) for item in previous_parsing_results["already_parsed_posts"] if item not in deduplicated_list]
			previous_parsing_results["already_parsed_posts"] = deduplicated_list

			json.dump(previous_parsing_results, open('./parser_data.json', 'w'), indent=4, ensure_ascii=False)

	while True:
		try:
			with parser.client:
				parser.client.loop.run_until_complete(update_posts())
				parser.client.run_until_disconnected()
		except (ConnectionError, BrokenPipeError, OSError) as e:
			print(f"Connection error occurred: {e}")
			# Логика для повторного подключения, например, задержка перед новой попыткой
			time.sleep(10)  # Пауза перед следующей попыткой подключения
			continue  # Попробуйте подключиться заново
		except KeyboardInterrupt:
			print("Keyboard interrupt detected, exiting...")
			break
