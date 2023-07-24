from telebot.types import BotCommand


default_commands = (
    ('start', 'Запустить команду'),
    ('help', 'Помощь'),
    ('lowprice', 'Сортировка от меньшей к большей цене'),
    ('highprice', 'Сортировка по цене и выбору'),
    ('bestdeal', 'Лучшие|Рекомендованные отели'),
    ('history', 'История запросов (последние 10)'),
    ('custom', 'Возможно тут, что-то появится'),
)


def set_default_commands(bot) -> None:
    """Создаем команды в ТГ_Бот"""
    bot.set_my_commands(
        [BotCommand(*i) for i in default_commands]
    )
