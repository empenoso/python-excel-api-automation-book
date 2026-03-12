# pip install telethon python-dotenv pytz

import sys
sys.stdout.reconfigure(encoding='utf-8')

import asyncio
from telethon import TelegramClient, utils
from datetime import datetime, timedelta, time
import random
from dotenv import load_dotenv
import os
import pytz

# Загрузка переменных окружения из .env
load_dotenv()
api_id = os.getenv("api_id")  # Ваш API ID
api_hash = os.getenv("api_hash")  # Ваш API Hash
session_name = 'nodejs_session'  # Название сессии

# Сообщения
greetings = [
    "Доброе утро! Как ты себя чувствуешь сегодня?",
    "Привет, как настроение? Готовность к новому дню?",
    "Доброе утро! Что нового на сегодня?",
    "Утро доброе! Как у тебя всё происходит с утра?",
    "Доброе утро, как ты себя сегодня чувствуешь?",
    "Привет! Как ты, как сны?",
    "Как твои дела, готовность к этому дню?",
    "Доброе утро! Как настроение, что планируешь на день?",
    "Здравствуй! Как ты себя чувствуешь после сна?"
]
supportive_messages = [
    "Как ты там? Всё в порядке?",
    "Как проходит твой день?",
    "Надеюсь, день не слишком утомительный для тебя!",
    "Как настроение? Всё ли хорошо?",
    "Не забывай делать перерывы, если устала!",
    "Как ты? Чем занимаешься сейчас?",
    "Если что-то нужно, не стесняйся мне писать.",
    "Надеюсь, день приносит тебе только положительные   оменты!",
    "Как ты себя чувствуешь? Хочешь поговорить?"
]

# Таймзона Екатеринбурга
ekb_timezone = pytz.timezone('Asia/Yekaterinburg')

async def schedule_messages(client, user, messages, start_hour, end_hour, days, description):
    """Планирует сообщения для заданного пользователя на несколько дней."""
    for day in range(days):
        # Вычисляем дату и время в Екатеринбурге
        now_ekb = datetime.now(ekb_timezone)
        schedule_date_ekb = now_ekb.date() + timedelta(days=day + 1)
        schedule_time_ekb = ekb_timezone.localize(datetime.combine(schedule_date_ekb, time(hour=random.randint(start_hour, end_hour), minute=random.randint(0, 30))))

        # Конвертируем время в UTC для Telethon
        schedule_time_utc = schedule_time_ekb.astimezone(pytz.UTC)

        message_text = random.choice(messages)

        try:
            await client.send_message(user, message_text, schedule=schedule_time_utc)
            print(f"✅ Отложенное сообщение отправлено для {description} на {schedule_time_ekb.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"❌ Ошибка при отправке сообщения для {description}: {e}")


async def main():
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()

    print("🚀 Запуск программы...")
    try:
        tasks = []

        user_Name1 = await client.get_entity("empenoso") # имя пользователя
        tasks.append(schedule_messages(client, user_Name1, greetings, 7, 7, 3, "пользователя userName"))  # Утренние сообщения
        tasks.append(schedule_messages(client, user_Name1, supportive_messages, 12, 12, 3, "пользователя userName"))  # Дневные сообщения

        user_Name2 = await client.get_input_entity("+7912XXXXX")  # Непосредственно номер телефона
        tasks.append(schedule_messages(client, user_Name2, greetings, 7, 7, 3, "пользователя +7912XXXXX"))  # Утренние сообщения

        await asyncio.gather(*tasks)
        print("🎉 Все сообщения успешно настроены.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await client.disconnect()
        print("🔌 Соединение с Telegram завершено.")


if __name__ == '__main__':
    asyncio.run(main())