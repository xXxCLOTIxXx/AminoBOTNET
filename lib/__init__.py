from .client import Client
from .config import name, links
from .system import Generator
from colored import fore, style
from os import system as s


"""
	Made by Xsarz (@DXsarz)
	GitHub: https://github.com/xXxCLOTIxXx
	Telegram channel: https://t.me/DxsarzUnion
	YouTube: https://www.youtube.com/channel/UCNKEgQmAvt6dD7jeMLpte9Q]

"""

def init():
	s("cls")
	print(fore.MEDIUM_PURPLE_4 + style.BOLD, name, links, fore.PURPLE_3)
init()