from create_bot import bot, db
from database_sqlite.model import History
from telebot.custom_filters import StateFilter
from commands.commands import set_default_commands
import handlers


if __name__ == '__main__':
    with db:
        History.create_table()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()


