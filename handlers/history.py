from create_bot import bot, logger

from telebot.types import Message
from database_sqlite.db_controller import get_info


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    """Функция которая выводит историю запросов"""
    try:
        bot.send_message(message.from_user.id, '💾 Последние 10 запросов\n')
        get_info(message)
        logger.info('Команда /history выполнена успешно...')
    except BaseException as BE:
        logger.error(BE)
        bot.send_message(message.from_user.id, 'Упс... Что-то пошло не так. Повтори команду заново')



