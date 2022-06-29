import hmac
from os import urandom
from hashlib import sha1
import json
from base64 import b64encode


class Generator():
	PREFIX = bytes.fromhex("42")
	SIG_KEY = bytes.fromhex("F8E7A61AC3F725941E3AC7CAE2D688BE97F30B93")
	DEVICE_KEY = bytes.fromhex("02B258C63559D8804321C5D5065AF320358D366F")
	def deviceId(self):
		try:
			with open("device.json", "r") as stream:
				data = json.load(stream)
		except (FileNotFoundError, json.decoder.JSONDecodeError):
			device = self.generate_device_info()
			with open("device.json", "w") as stream:
				json.dump(device, stream, indent=4)
			with open("device.json", "r") as stream:
				data = json.load(stream)
		return data


	def signature(self, data) -> str:
		try: dt = data.encode("utf-8")
		except Exception: dt = data
		mac = hmac.new(bytes.fromhex("F8E7A61AC3F725941E3AC7CAE2D688BE97F30B93"), dt, sha1)
		return b64encode(bytes.fromhex("42") + mac.digest()).decode("utf-8")

	def generate_device_info(self):
		identifier = urandom(20)
		key = bytes.fromhex("02B258C63559D8804321C5D5065AF320358D366F")
		mac = hmac.new(key, bytes.fromhex("42") + identifier, sha1)
		device = f"42{identifier.hex()}{mac.hexdigest()}".upper()
		return {
			"device_id": device,
			"user_agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.5.33562)"
		}