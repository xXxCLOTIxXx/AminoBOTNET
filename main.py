import lib
from colored import fore, style
from threading import Thread
from json import load
client = lib.Client()
communities = []
chats = []
try:
	with open("accounts.json", "r") as file:
		accounts = load(file)
		print(fore.GREEN, f"{len(accounts)} accounts loaded", fore.PURPLE_3)
except Exception as error:print(fore.RED, error); exit()


while True:
	try:client.login(email=input("\nGeneral account gmail>> "), password=input("General account password>>")); print(fore.GREEN, "\nSuccessful login\n", fore.PURPLE_3); break
	except Exception as error:print(fore.RED, error, fore.PURPLE_3)
message = input("Message>> ")

while True:
	mt = input("MessageType (0 or 109) >> ")
	if mt == '0':print(fore.GREEN, "\nOK.\n", fore.PURPLE_3); messageType = 0; break
	elif mt == '109':print(fore.GREEN, "\nOK.\n", fore.PURPLE_3); messageType = 109; break
	else: print("\nError type.\nRegular message - 0\nSystem message - 109\n")
for num, my_communities in  enumerate(client.get_my_communities(size=100), 1): print(f'{num})',my_communities['name']); communities.append(my_communities)
while True:
	try:
		selected_community = int(input("Select community>> "))-1
		comId = communities[selected_community]['ndcId']
		print(fore.GREEN, "\nOK.\n", fore.PURPLE_3); break
	except ValueError:
		print(fore.RED,"\nPlease enter a number\n", fore.PURPLE_3)
	except IndexError:
		print(fore.RED,"\nNumber not found\n", fore.PURPLE_3)
	except Exception as error:print(fore.RED, error, fore.PURPLE_3)
for chats_ in client.get_public_chat_threads(size=100, comId=comId):
	if chats_['title']!=None:chats.append(chats_['threadId'])


def spam(client, chatId):
	while True:
		try:
			Thread(target=client.send_message, args=(chatId, comId, message, messageType)).start()
		except:break
	while True:client.send_message(chatId=chatId, comId=comId, message=message, messageType=messageType)

def start_bots(account):
	try:
		bot_client = lib.Client()
		gmail = account['email']
		password = account['password']
		bot_client.login(email=gmail, password=password); print(fore.GREEN, f"\n{gmail}: Successful login\n", fore.PURPLE_3)
		for i in range(len(chats)):
			try:bot_client.join_chat(comId=comId, chatId=chats[i])
			except:pass
			try:client.change_profile(comId=comId, name='Free scripts -> @DXsarz | Бесплатные скрипты -> @DXsarz', content=open("antiban.txt", encoding='utf-8').read())
			except:pass
		print(fore.GREEN, f"\n{gmail}: Successful join all chats\n{gmail}: I start spamming...\n", fore.PURPLE_3)
		for i in range(len(chats)): Thread(target=spam, args=(bot_client, chats[i])).start()
	except Exception as error:print(fore.RED, f'{gmail}: This account has been stopped, error:\n',error, fore.PURPLE_3)
for i in range(len(accounts)):Thread(target=start_bots, args=(accounts[i],)).start()