from create_bot import bot, logger
from telebot.types import Message


@bot.message_handler(commands=['help'])
@logger.catch
def help(message: Message) -> None:
    """Команда help"""
    bot.send_message(message.from_user.id, f'👋 Привет. Выбери команду из меню.')


