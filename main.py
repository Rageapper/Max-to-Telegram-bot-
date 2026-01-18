from max import MaxClient as Client
from filters import filters
from classes import Message
from telegram import send_to_telegram
import time, os, sys
from dotenv import load_dotenv

load_dotenv()

MAX_TOKEN = os.getenv("MAX_TOKEN") or ""
MAX_CHAT_IDS_STR = os.getenv("MAX_CHAT_IDS") or ""
MAX_CHAT_IDS = [int(x.strip()) for x in MAX_CHAT_IDS_STR.split(",") if x.strip()] if MAX_CHAT_IDS_STR else []

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN") or ""
TG_CHAT_ID_STR = os.getenv("TG_CHAT_ID") or ""

# Преобразуем TG_CHAT_ID в int, если возможно
TG_CHAT_ID = None
if TG_CHAT_ID_STR:
    try:
        TG_CHAT_ID = int(TG_CHAT_ID_STR)
    except ValueError:
        TG_CHAT_ID = None

if not MAX_TOKEN or not MAX_CHAT_IDS or not TG_BOT_TOKEN or TG_CHAT_ID is None:
    print("[ОШИБКА] Ошибка в .env файле. Проверьте следующие параметры:")
    print(f"  MAX_TOKEN: {'не указан' if not MAX_TOKEN else 'указан'}")
    print(f"  MAX_CHAT_IDS: {'не указан' if not MAX_CHAT_IDS else f'указан ({len(MAX_CHAT_IDS)} чатов)'}")
    print(f"  TG_BOT_TOKEN: {'не указан' if not TG_BOT_TOKEN else 'указан'}")
    print(f"  TG_CHAT_ID: {'не указан' if TG_CHAT_ID is None else f'указан ({TG_CHAT_ID})'}")
    if TG_CHAT_ID_STR and TG_CHAT_ID is None:
        print(f"  Проблема: TG_CHAT_ID='{TG_CHAT_ID_STR}' - должно быть числом (например: -1001234567890 или 123456789)")
    print("\nУбедитесь, что все параметры заполнены в файле .env")
    sys.exit(1)
MONITOR_ID = os.getenv("MONITOR_ID")
client = Client(MAX_TOKEN)

print("[ИНИЦИАЛИЗАЦИЯ] Создание клиента MAX...")
print("[ПОДКЛЮЧЕНИЕ] Подключение к серверу MAX...")

@client.on_connect
def onconnect():
    if client.me != None:
        print(f"[УСПЕХ] Подключено к MAX")
        print(f"Имя: {client.me.contact.names[0].name}, Номер: {client.me.contact.phone} | ID: {client.me.contact.id}")
        print(f"Отслеживаемые чаты: {MAX_CHAT_IDS}")
        print("Бот запущен и готов к работе!")


@client.on_message(filters.any())
def onmessage(client: Client, message: Message):
    # Отладочный вывод для проверки получения сообщений
    print(f"[DEBUG] Получено сообщение: chat_id={message.chat.id}, text_length={len(message.text) if message.text else 0}, status={message.status}")
    print(f"[DEBUG] Отслеживаемые чаты: {MAX_CHAT_IDS}")
    print(f"[DEBUG] Сообщение в отслеживаемом чате: {message.chat.id in MAX_CHAT_IDS}")
    
    if message.chat.id in MAX_CHAT_IDS and message.status != "REMOVED":
        msg_text = message.text
        msg_attaches = message.attaches
        name = message.user.contact.names[0].name if message.user and message.user.contact else "Неизвестно"
        if "link" in message.kwargs.keys():
            if "type" in message.kwargs["link"]:
                if message.kwargs["link"]["type"] == "REPLY": # TODO
                    ...
                if message.kwargs["link"]["type"] == "FORWARD":
                    msg_text = message.kwargs["link"]["message"]["text"]
                    msg_attaches = message.kwargs["link"]["message"]["attaches"]
                    forwarded_msg_author = client.get_user(id=message.kwargs["link"]["message"]["sender"], _f=1)
                    name = f"{name}\n(Переслано: {forwarded_msg_author.contact.names[0].name})"

        if msg_text != "" or msg_attaches != []:
            print(f"[ОТПРАВКА] Отправка в Telegram: от {name}, текст: {msg_text[:50]}...")
            try:
                send_to_telegram(
                    TG_BOT_TOKEN,
                    TG_CHAT_ID,
                    f"<blockquote>{name}</blockquote>\n{msg_text}" if msg_text != "" else f"<blockquote>{name}</blockquote>",
                    msg_attaches
                    # [attach['baseUrl'] for attach in msg_attaches if 'baseUrl' in attach]
                )
                print(f"[УСПЕХ] Сообщение отправлено в Telegram")
            except Exception as e:
                print(f"[ОШИБКА] Ошибка при отправке в Telegram: {e}")
                import traceback
                traceback.print_exc()
client.run()

