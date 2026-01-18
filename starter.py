import subprocess
import time
import sys, os
import datetime
from telegram_api import send_to_telegram
from dotenv import load_dotenv

load_dotenv()
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
MONITOR_ID = os.getenv("MONITOR_ID")

def check_config():
    """Проверяет конфигурацию перед запуском"""
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    MAX_TOKEN = os.getenv("MAX_TOKEN") or ""
    MAX_CHAT_IDS_STR = os.getenv("MAX_CHAT_IDS") or ""
    TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN") or ""
    TG_CHAT_ID = os.getenv("TG_CHAT_ID") or ""
    
    errors = []
    if not MAX_TOKEN:
        errors.append("MAX_TOKEN не указан")
    if not MAX_CHAT_IDS_STR:
        errors.append("MAX_CHAT_IDS не указан")
    if not TG_BOT_TOKEN:
        errors.append("TG_BOT_TOKEN не указан")
    if not TG_CHAT_ID:
        errors.append("TG_CHAT_ID не указан")
    
    if errors:
        print(f"[{datetime.datetime.now()}] [КРИТИЧЕСКАЯ ОШИБКА] Конфигурация неверна:")
        for error in errors:
            print(f"  - {error}")
        print("\nЗаполните файл .env и запустите скрипт снова.")
        return False
    return True

def is_critical_error(stderr_text):
    """Проверяет, является ли ошибка критической (не требующей перезапуска)"""
    if not stderr_text:
        return False
    
    critical_errors = [
        "Ошибка в .env",
        "Неверный токен",
        "login.token",
        "MAX_TOKEN не указан",
        "MAX_CHAT_IDS не указан",
        "TG_BOT_TOKEN не указан",
        "TG_CHAT_ID не указан"
    ]
    
    stderr_lower = stderr_text.lower()
    for error in critical_errors:
        if error.lower() in stderr_lower:
            return True
    return False

def run_with_restart():
    # Проверяем конфигурацию перед запуском
    if not check_config():
        print(f"\n[{datetime.datetime.now()}] Остановка. Исправьте ошибки в .env файле и запустите снова.")
        sys.exit(1)
    
    restart_alarm = False
    consecutive_critical_errors = 0
    max_critical_errors = 3  # Максимум критических ошибок подряд
    
    while True:
        try:
            print(f"[{datetime.datetime.now()}] Запуск main.py...")
            
            process = subprocess.Popen(
                [sys.executable, "main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Объединяем stderr с stdout
                text=True,
                bufsize=1)  # Небуферизованный вывод
            
            if MONITOR_ID and MONITOR_ID != "":
                try:
                    send_to_telegram(
                        TG_BOT_TOKEN,
                        MONITOR_ID,
                        f"<b>Бот встал</b>",
                    )
                except:
                    pass
            
            restart_alarm = True
            
            # Выводим вывод в реальном времени
            output_lines = []
            while True:
                line = process.stdout.readline()
                if line == '' and process.poll() is not None:
                    break
                if line:
                    print(line, end='', flush=True)
                    output_lines.append(line)
            
            stdout = ''.join(output_lines)
            exit_code = process.returncode
            
            # Проверяем, критическая ли ошибка
            if is_critical_error(stdout):
                consecutive_critical_errors += 1
                print(f"\n[{datetime.datetime.now()}] [КРИТИЧЕСКАЯ ОШИБКА] Обнаружена критическая ошибка конфигурации!")
                print(f"[{datetime.datetime.now()}] Остановка перезапуска. Исправьте ошибки и запустите скрипт снова.")
                
                if MONITOR_ID and MONITOR_ID != "":
                    try:
                        send_to_telegram(
                            TG_BOT_TOKEN,
                            MONITOR_ID,
                            f"<b>Критическая ошибка!</b>\nСкрипт остановлен из-за ошибки конфигурации.\n\nОшибка:\n{stderr[:500] if stderr else stdout[:500]}"
                        )
                    except:
                        pass
                
                sys.exit(1)
            else:
                consecutive_critical_errors = 0  # Сбрасываем счетчик при некритической ошибке
            
            if MONITOR_ID and MONITOR_ID != "" and restart_alarm:
                try:
                    send_to_telegram(
                        TG_BOT_TOKEN,
                        MONITOR_ID,
                        f"[{datetime.datetime.now()}] Скрипт упал (код: {exit_code})\nstderr: {stderr[:500] if stderr else 'нет'}"
                    )
                except:
                    pass
                restart_alarm = False
            
            print(f"[{datetime.datetime.now()}] Скрипт упал (код: {exit_code}). Перезапуск через 3 секунды...")
            time.sleep(3)
                
        except KeyboardInterrupt:
            print(f"\n[{datetime.datetime.now()}] Остановлено пользователем")
            if process:
                process.terminate()
            break
        except Exception as e:
            print(f"[{datetime.datetime.now()}] Ошибка: {e}")
            time.sleep(3)

if __name__ == "__main__":
    run_with_restart()
