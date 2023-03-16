__all__ = [
    'register_message_handlers'
]


import aiohttp
import logging
from aiogram import types, Router
from aiogram.filters import Command, Text

API_URL = 'http://172.21.0.2:8888/toxicity'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    try:
        msg = str(message.text)
        playload = { 'input': message.text }
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, headers=headers, json=playload) as resp:
                text = await resp.json()
                if text['response']['toxicity'] > 2.5:
                    await message.reply("It's toxic!")
                    await message.delete()
        logger.debug(f'User {message.from_user.id} send {message.text}. Response {text["response"]}')
    except (ValueError, KeyError):
        logger.info(f'User {message.from_user.id} send non-text message')


async def check_value_command(message: types.Message):
    '''Check value of toxicity in message.
    '''
    playload = { 'input': message.text[6:] }
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=playload) as resp:
            text = await resp.json()
            await message.reply(str(text['response']))
    logger.debug(f'User {message.from_user.id} send {message.text[6:]}. Response {text["response"]}')

def register_message_handlers(router: Router):
    router.message.register(help_command, Command(commands=['help', 'start']))
    router.message.register(help_command, Text(text=['help']))
    router.message.register(check_value_command, Command(commands=['check']))
    router.message.register(main_handler)