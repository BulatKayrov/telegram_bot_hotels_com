from .model import History
from create_bot import db, bot, logger
from telebot.types import Message
from emoji import emojize


@logger.catch
def save_info(name, address, desc, price, rating):
    """Сохраняем информацию в БД"""
    with db:
        History(name_city=name, address=address, description=desc, price=price, rating=rating).save()


@logger.catch
def get_info(message: Message):
    """Достаем из БД, последние 10 записей"""
    with db:
        for data in History.select().order_by(History.id.desc()).limit(10):
            text = f'{emojize("🌆")}Название: {data.name_city}\n{emojize("🌍")}Адресс: {data.address}\n' \
                      f'{emojize("📑")}Описание: {data.description.strip()}\n' \
                      f'{emojize("💵")}Цена: {data.price}\n{emojize("📈")}Рейтинг: {data.rating}'
            bot.send_message(message.from_user.id, text=text)





