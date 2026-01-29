from max import MaxClient as Client
from filters import filters
from classes import Message
import time
import sys

try:
    client = Client()
    phone_number = "+7XXXXXXXXXX"  # Replace with your phone number
    
    print(f"Попытка авторизации для номера: {phone_number}")
    print("Подключение к серверу MAX...")
    
    client.auth(phone_number)
    print("\n[OK] Авторизация успешна!")
    print(f"Токен: {client.auth_token}")
    
except ValueError as e:
    error_msg = str(e)
    if "service.unavailable" in error_msg or "auth forbidden" in error_msg.lower():
        print("\n[ОШИБКА] Авторизация запрещена сервером MAX")
        print("\nСервер возвращает: 'auth forbidden'")
        print("\nВозможные причины:")
        print("1. Сервер MAX блокирует автоматизированные запросы на авторизацию")
        print("2. API MAX изменился, требуется другой способ получения токена")
        print("3. Токен нужно получать через веб-интерфейс или мобильное приложение")
        print("\nАльтернативные способы получения токена:")
        print("1. Зайдите в группу Telegram: https://t.me/intchaserlive")
        print("2. Следуйте инструкции из закрепленного сообщения")
        print("3. Получите токен через веб-версию MAX: https://web.max.ru")
        print("4. Используйте инструменты разработчика браузера (F12) для извлечения токена")
        sys.exit(1)
    else:
        print(f"\n[ОШИБКА] Ошибка авторизации: {error_msg}")
        sys.exit(1)
        
except KeyboardInterrupt:
    print("\n\n[ПРЕРВАНО] Прервано пользователем")
    sys.exit(0)
    
except Exception as e:
    print(f"\n[ОШИБКА] Неожиданная ошибка: {e}")
    print(f"Тип ошибки: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

