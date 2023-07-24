from create_bot import bot, logger
from telebot.types import Message
from emoji import emojize


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    """Функция отвечающая на команду /start"""
    try:
        bot.send_message(message.from_user.id, f'{emojize("👋")}Привет.\n'
                                               f'Я бот по поиску и предоставлении информации по отелям зарубежом, выбери'
                                               f' команду из меню.')
        logger.info('Команда /start выполнена успешно...')
    except BaseException as BE:
        logger.error(BE)
        bot.send_message(message.from_user.id, 'Упс... Что-то пошло не так. Повтори команду заново')





