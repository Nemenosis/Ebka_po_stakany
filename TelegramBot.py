import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
import os


def ensure_user_file_exists():
    if not os.path.exists("user_ids.txt"):
        with open("user_ids.txt", "w") as f:
            pass


class TelegramBot:
    def __init__(self, bot_token):
        self.bot = Bot(token=bot_token)
        self.dp = Dispatcher()
        self.user_ids = self.load_user_ids()
        self.dp.message.register(self.start_command, Command("start"))

    def load_user_ids(self):
        ensure_user_file_exists()
        with open("user_ids.txt", "r") as f:
            return set(line.strip() for line in f)

    def save_user_id(self, user_id):
        if str(user_id) not in self.user_ids:
            with open("user_ids.txt", "a") as f:
                f.write(str(user_id) + "\n")
            self.user_ids.add(str(user_id))

    async def start_command(self, message: types.Message):
        self.save_user_id(message.from_user.id)
        await message.reply(
            "Вітаю! Я буду сповіщати вас про арбітражні ситуації. Тепер ви будете отримувати повідомлення.")

    async def send_message(self, chat_id, text):
        try:
            await self.bot.send_message(chat_id, text)
        except Exception as e:
            print(f"Помилка при відправці повідомлення користувачу {chat_id}: {e}")

    async def start_polling(self):
        await self.dp.start_polling(self.bot)