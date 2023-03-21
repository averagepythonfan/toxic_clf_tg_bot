__all__ = [
    'register_message_handlers'
]


import aiohttp
import logging
from aiogram import types, Router
from aiogram.filters import Command, Text
from config import FASTAPI_ADDRESS, TOXICITY_LEVEL


API_URL = FASTAPI_ADDRESS
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


help_str = '''Чат-бот для определения токсичности в сообщениях.
Добавьте бота в свой чат, дайте ему права администратора и разрешите ему удалять сообщения.
Также для бота доступна команда "/check (ваще сообщение)" для вывода результатов проверки.'''


async def help_command(message: types.Message):
    '''Обработчик для команды помощи.

    :usage: /help'''
    await message.answer(help_str)


async def main_handler(message: types.Message):
    '''Главный обработчик сообщений для классификации токсичности

    :params: message - любой текст на русском.

    Если показатель токсичности выше 2.5,
    то сообщение определяется как неприемлемое и удаляется ботом.
    '''
    try:
        msg = str(message.text)
        playload = { 'input': msg }
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, headers=headers, json=playload) as resp:
                text = await resp.json()
                if text['response']['toxicity'] > TOXICITY_LEVEL:
                    await message.reply("It's toxic!")
                    await message.delete()
        logger.debug(f'User {message.from_user.id} send {message.text}. Response {text["response"]}')
    except (ValueError, KeyError):
        logger.info(f'User {message.from_user.id} send non-text message')


async def check_value_command(message: types.Message):
    '''Обработчик для команды /check. Возвращает результаты проверки.

    :params: message - любой текст на русском.
    :usage: /check (ваш текст)
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
