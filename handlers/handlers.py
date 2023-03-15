__all__ = [
    'register_message_handlers'
]


import aiohttp
from aiogram import types, Router
from aiogram.filters import Command, Text
from config import API_KEY

API_URL = "https://api-inference.huggingface.co/models/IlyaGusev/rubertconv_toxic_clf"
headers = {"Authorization": f"Bearer {API_KEY}"}


help_str = '''HELP'''


async def help_command(message: types.Message):
    '''Help command.

    :usage: /help'''
    await message.answer(help_str)


async def main_handler(message: types.Message):
    '''Main handler for toxicity classification

    :params: message - any text.
    If toxic score greater then 0.9 it classified as toxic message.
    And then bot delete the message.
    '''
    playload = { 'inputs': message.text }
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=playload) as resp:
            text = await resp.json()
            for el in text[0]:
                if el['label'] == 'toxic' and el['score'] > 0.9:
                    await message.reply("It's toxic!")
                    await message.delete()

def register_message_handlers(router: Router):
    router.message.register(help_command, Command(commands=['help', 'start']))
    router.message.register(help_command, Text(text=['help']))
    router.message.register(main_handler)