import requests
from lib import system
from random import choice
import json
from time import time as timestamp

"""
	Made by Xsarz (@DXsarz)
	GitHub: https://github.com/xXxCLOTIxXx
	Telegram channel: https://t.me/DxsarzUnion
	YouTube: https://www.youtube.com/channel/UCNKEgQmAvt6dD7jeMLpte9Q]

"""

class Client():
	def __init__(self):
		self.sid = None
		self.uid = None
		self.session = requests.Session()
		self.api = "https://service.narvii.com/api/v1"
		self.web_api = "https://aminoapps.com/api"
		self.generator = system.Generator()
		self.device = self.generator.deviceId()
		self.User_Agent = self.device["user_agent"]
		self.device_id = self.device["device_id"]

	def headers(self, data=None, content_type=None):
		headers = {
			"NDCDEVICEID": self.device_id,
			"Accept-Language": "en-US",
			"Content-Type": "application/json; charset=utf-8",
			"User-Agent": self.User_Agent,
			"Host": "service.narvii.com",
			"Accept-Encoding": "gzip",
			"Connection": "Upgrade"
		}

		if data is not None:
			headers["Content-Length"] = str(len(data))
			headers["NDC-MSG-SIG"] = self.generator.signature(data=data)
		if self.sid is not None:
			headers["NDCAUTH"] = f"sid={self.sid}"
		if content_type is not None:
			headers["Content-Type"] = content_type
		return headers

	def web_headers(self, referer):
		headers = {
			"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36",
			"content-type": "application/json",
			"x-requested-with": "xmlhttprequest",
			"cookie": f"sid={self.sid}",
			"referer": referer
		}
		return headers


	def login(self, email: str, password: str):
		data = json.dumps({
			"email": email,
			"v": 2,
			"secret": f"0 {password}",
			"deviceID": self.device_id,
			"clientType": 100,
			"action": "normal",
			"timestamp": int(timestamp() * 1000)
		})
		response = self.session.post(f"{self.api}/g/s/auth/login", headers=self.headers(data=data), data=data)
		if response.status_code != 200: raise Exception(json.loads(response.text))
		else:json_response = json.loads(response.text)
		self.sid = json_response["sid"]
		self.uid = json_response["account"]["uid"]
		return self.uid

	def get_my_communities(self, start: int = 0, size: int = 25):
		response = self.session.get(f"{self.api}/g/s/community/joined?v=1&start={start}&size={size}", headers=self.headers())
		if response.status_code != 200: raise Exception(json.loads(response.text))
		else: return json.loads(response.text)["communityList"]


	def join_community(self, comId: str):
		data = json.dumps({"timestamp": int(timestamp() * 1000)})
		response = self.session.post(f"{self.api}/x{comId}/s/community/join", headers=self.headers(data=data), data=data)
		if response.status_code != 200: raise Exception(json.loads(response.text))
		else: return response.status_code


	def join_chat(self, chatId: str, comId: str):
		response = self.session.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/member/{self.uid}", headers=self.headers())
		if response.status_code != 200: raise Exception(json.loads(response.text))
		else: return response.status_code


	def send_message(self, chatId: str, comId: str, message: str, messageType: int = 0):
		data = {
			"ndcId": f"x{comId}",
			"threadId": chatId,
			"message": {
				"content": message,
				"mediaType": 0,
				"type": messageType,
				"sendFailed": False,
				"clientRefId": 0
			}
		}
		data = json.dumps(data)
		response = self.session.post(f"https://aminoapps.com/api/add-chat-message",headers=self.web_headers(referer=f"https://aminoapps.com/partial/main-chat-window?ndcId={comId}"),data=data)
		if response.status_code != 200: raise Exception(json.loads(response.text))
		else: return response.status_code


	def get_public_chat_threads(self, comId: str, type: str = "recommended", start: int = 0, size: int = 25):
		response = self.session.get(f"{self.api}/x{comId}/s/chat/thread?type=public-all&filterType={type}&start={start}&size={size}", headers=self.headers())
		if response.status_code != 200: raise Exception(json.loads(response.text))
		else: return json.loads(response.text)["threadList"]

	def change_profile(self, comId: str, name: str = None, content: str = None):
		data = {"timestamp": int(timestamp() * 1000)}
		if name!=None: data["nickname"] = name
		if content!=None: data["content"] = content
		data = json.dumps(data)
		response = self.session.post(f"{self.api}/x{comId}/s/user-profile/{self.uid}", headers=self.headers(data=data), data=data)
		if response.status_code != 200: return Exception(json.loads(response.text))
		else:return response.status_code