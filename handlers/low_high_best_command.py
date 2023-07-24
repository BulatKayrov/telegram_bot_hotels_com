from create_bot import bot, logger
from telebot.types import Message, CallbackQuery, InputMediaPhoto
from keyboards.inline.keyboards import inline_get_city, inline_need_photo, inline_count_photo, inline_choise_hotel
from callBack_data.callback_data import SEARCH_LOCATION, NEED_PHOTO, COUNT_PHOTO, ID_HOTEL, RATING, PRICE
from datetime import datetime as dt
from templates_API.Hotels_com.api import detail_information
from emoji import emojize
from database_sqlite.db_controller import save_info



# словарь состояния

save_dict = {
    'commands': '',
    'city_ID': '',
    'count_hotels': '',
    'need_photo': '',
    'count_photo': '',
    'day': '',
    'month': '',
    'year': '',
}


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def start(message: Message) -> None:
    """Хендлер реагирует только на определенные команды"""
    try:
        save_dict['commands'] = message.text[1:]
        bot.send_message(message.from_user.id, f'Введи город в котором будет производить поиск:')
        bot.register_next_step_handler(message, get_city)
        logger.info('Команда выполненая пользователем, выполнена успешно...')
    except BaseException as BE:
        logger.error(BE)
        bot.send_message(message.from_user.id, 'Упс... Что-то пошло не так. Повтори команду заново')


def get_city(message: Message) -> None:
    """Ф-ция сохраняет в словарик данные веденные пользователем, и вызываются кнопки. Параллельно наполняя константу
    SEARCH_LOCATION"""
    try:
        save_dict['city'] = message.text
        bot.send_message(message.from_user.id, f'Уточните город:',
                         reply_markup=inline_get_city(city=message.text))
        logger.info(f'Команда веденная пользователем, выполнена успешно...')
    except BaseException as BE:
        logger.error(BE)
        bot.send_message(message.from_user.id, 'Упс... Что-то пошло не так. Повтори команду заново')


@bot.callback_query_handler(func=lambda callback: callback.data in SEARCH_LOCATION)
def callback_set_city(callback: CallbackQuery) -> None:
    """Ловим наши ID городов, сохраняем, и фиксируем дату. Вызываем след. ф-цию отвечающую
    за кол-во отелей"""
    try:
        save_dict['city_ID'] = callback.data
        date = dt.now().strftime('%d-%m-%Y').split('-')
        save_dict['day'] = date[0]
        save_dict['month'] = date[1]
        save_dict['year'] = date[2]

        bot.send_message(callback.message.chat.id, f'Сколько отображать отелей? (Не больше 15 шт)')
        bot.register_next_step_handler(callback.message, count_hotels)
        logger.info('Команда выполненая пользователем, выполнена успешно...')
    except BaseException as BE:
        logger.error(BE)
        bot.send_message(callback.message.chat.id, 'Упс... Что-то пошло не так. Повтори команду заново')


def count_hotels(message: Message) -> None:
    """Созраняем кол-во отелей.
    При команде bestdeal пропускаем некоторые шаги, потому что команда bestdeal подразумевает фото,
    поэтому сразу запрашиваем стоимость.
    Если другая команда , то запрашиваем инф-ию на отображение фото"""
    try:
        if save_dict['commands'] == 'bestdeal':
            if int(message.text) > 15:
                save_dict['count_hotels'] = '15'
            else:
                save_dict['count_hotels'] = message.text
            save_dict['need_photo'] = 'Да'
            save_dict['count_photo'] = '7'
            bot.send_message(message.chat.id, f'{emojize("💵")}   Введи минимальную цену в долларах: {emojize("🇺🇸")}')
            bot.register_next_step_handler(message, min_price)
        elif int(message.text) < 15:
            save_dict['count_hotels'] = message.text
            bot.send_message(message.from_user.id, f'Загружать фото?', reply_markup=inline_need_photo())
        elif int(message.text) >= 15:
            save_dict['count_hotels'] = '15'
            bot.send_message(message.from_user.id, f'Загружать фото?', reply_markup=inline_need_photo())
        logger.info('Команда выполненая пользователем, выполнена успешно...')
    except BaseException as BE:
        logger.error(BE)
        bot.send_message(message.from_user.id, 'Упс... Что-то пошло не так. Повтори команду заново')


@bot.callback_query_handler(func=lambda callback: callback.data in NEED_PHOTO)
def need_photo(callback: CallbackQuery) -> None:
    """Выбираем кол-во фото если пользователь нажал ДА, иначе выводим информацию по выбору отелей"""
    try:
        if callback.data == NEED_PHOTO[0]:
            save_dict['need_photo'] = callback.data
            bot.send_message(callback.message.chat.id, f'Выбери количество фото', reply_markup=inline_count_photo())
        else:
            save_dict['need_photo'] = callback.data
            save_dict['count_photo'] = 'None'
            if save_dict['commands'] == 'lowprice':
                command = 'lowprice'
            if save_dict['commands'] == 'highprice':
                command = 'highprice'
            reply_markup = inline_choise_hotel(
                city_id=save_dict['city_ID'], count_hotels=save_dict['count_hotels'], commands=command,
                day=save_dict['day'], month=save_dict['month'], year=save_dict['year'])
            bot.send_message(callback.message.chat.id, f'Выбери отель', reply_markup=reply_markup)
        logger.info('Команда выполненая пользователем, выполнена успешно...')
    except BaseException as BE:
        logger.error(BE)
        bot.send_message(callback.message.chat.id, 'Упс... Что-то пошло не так. Повтори команду заново')


@bot.callback_query_handler(func=lambda callback: int(callback.data) in COUNT_PHOTO)
def count_photo(callback: CallbackQuery) -> None:
    """Сохраняем кол-во фото. выводим информацию по выбору отелей если на предыдущем шаге, клиент нажал да"""
    try:
        if callback.data:
            save_dict['count_photo'] = callback.data
            if save_dict['commands'] == 'lowprice':
                reply_markup = inline_choise_hotel(
                    city_id=save_dict['city_ID'], count_hotels=save_dict['count_hotels'], commands=save_dict['commands'],
                    day=save_dict['day'], month=save_dict['month'], year=save_dict['year'])
                bot.send_message(callback.message.chat.id, f'{emojize("🏢")} Выбери отель', reply_markup=reply_markup)
            if save_dict['commands'] == 'highprice':
                reply_markup = inline_choise_hotel(
                    city_id=save_dict['city_ID'], count_hotels=save_dict['count_hotels'], commands=save_dict['commands'],
                    day=save_dict['day'], month=save_dict['month'], year=save_dict['year'])
                bot.send_message(callback.message.chat.id, f'{emojize("🏢")}  Выбери отель', reply_markup=reply_markup)
        logger.info('Команда выполненая пользователем, выполнена успешно...')
    except BaseException as BE:
        logger.error(BE)
        bot.send_message(callback.message.from_user.id, 'Упс... Что-то пошло не так. Повтори команду заново')


def min_price(message: Message) -> None:
    """Регистрируем мин.цену и запраиваем макс.цену"""
    try:
        save_dict['minPrice'] = int(message.text)
        bot.send_message(message.from_user.id, f'{emojize("💵")}   Введи максимальную цену в долларах: {emojize("🇺🇸")}')
        bot.register_next_step_handler(message, max_price)
        logger.info('Команда выполненая пользователем, выполнена успешно...')
    except BaseException as BE:
        logger.error(BE)
        bot.send_message(message.from_user.id, 'Упс... Что-то пошло не так. Повтори команду заново')


def max_price(message: Message) -> None:
    """Сохраняем макс прайс. И предлагаю выбрать отель для bestdeal"""
    try:
        save_dict['maxPrice'] = int(message.text)
        reply_markup = inline_choise_hotel(
            city_id=save_dict['city_ID'], count_hotels=save_dict['count_hotels'], commands=save_dict['commands'],
            day=save_dict['day'], month=save_dict['month'], year=save_dict['year'],
            priceIn=save_dict['minPrice'], priceOut=save_dict['maxPrice'])
        bot.send_message(message.chat.id, f'{emojize("🏢")} Выбери отель', reply_markup=reply_markup)
        logger.info('Команда выполненая пользователем, выполнена успешно...')
    except BaseException as BE:
        logger.error(BE)
        bot.send_message(message.from_user.id, 'Упс... Что-то пошло не так. Повтори команду заново')


@bot.callback_query_handler(func=lambda callback: callback.data in ID_HOTEL)
def pred_total_info(callback: CallbackQuery) -> None:
    """Выаодим собранную информацию, и выводим результат"""
    try:
        rating = RATING.get(callback.data)
        price = PRICE.get(callback.data)
        text = f"{emojize('📖')} Исходные данные:\n" \
               f"{emojize('🕒')} Дата и время запроса: {save_dict['day']}/{save_dict['month']}/{save_dict['year']}\n" \
               f"{emojize('➡')} Введенная команда: {save_dict['commands']}\n" \
               f"{emojize('🌆')} Введенный город: {save_dict['city']}\n{emojize('🆔')}: {save_dict['city_ID']}\n" \
               f"{emojize('🔢')} Количество отелей: {save_dict['count_hotels']}\n" \
               f"{emojize('🖼')} Нужны ли фотографии? {save_dict['need_photo']}\n" \
               f"{emojize('🧮')} Количество фотографий: {save_dict['count_photo']}"
        bot.send_message(callback.message.chat.id, text=text)
        if save_dict['commands'] in ['lowprice', 'highprice'] and save_dict['need_photo'] == 'Нет':
            response = detail_information(id_hotels=callback.data, N=0)
            caption = f'{emojize("🌆")}Название: {response["name"]}\n{emojize("🌍")}Адресс: {response["address"]}\n' \
                      f'{emojize("📑")}Описание: {response["description"].strip()}\n' \
                      f'{emojize("💵")}Цена: {price}\n{emojize("📈")}Рейтинг: {rating}'
            bot.send_message(callback.message.chat.id, text=caption)


            save_info(name=response["name"], price=price, desc=response["description"].strip(),
                      rating=rating, address=response["address"])
        elif save_dict['commands'] in ['lowprice', 'highprice'] and save_dict['need_photo'] == 'Да':
            response = detail_information(id_hotels=callback.data, N=save_dict['count_photo'])
            caption = f'{emojize("🌆")}Название: {response["name"]}\n{emojize("🌍")}Адресс: {response["address"]}\n' \
                      f'{emojize("📑")}Описание: {response["description"].strip()}\n' \
                      f'{emojize("💵")}Цена: {price}\n{emojize("📈")}Рейтинг: {rating}'
            photo = [InputMediaPhoto(media=i, caption=caption) for i in response['images']]
            bot.send_media_group(callback.message.chat.id, media=photo)
            bot.send_message(callback.message.chat.id, text=caption)
            save_info(name=response["name"], price=price, desc=response["description"].strip(),
                      rating=rating, address=response["address"])

        elif save_dict['commands'] == 'bestdeal':
            response = detail_information(id_hotels=callback.data, N=save_dict['count_photo'])
            caption = f'{emojize("🌆")}Название: {response["name"]}\n{emojize("🌍")}Адресс: {response["address"]}\n' \
                      f'{emojize("📑")}Описание: {response["description"].strip()}\n' \
                      f'{emojize("💵")}Цена: {price}\n{emojize("📈")}Рейтинг: {rating}'
            photo = [InputMediaPhoto(media=i, caption=caption) for i in response['images']]
            bot.send_media_group(callback.message.chat.id, media=photo)
            bot.send_message(callback.message.chat.id, text=caption)
            save_info(name=response["name"], price=price, desc=response["description"].strip(),
                      rating=rating, address=response["address"])
        logger.info('Команда выполненая пользователем, выполнена успешно...')

    except BaseException as BE:
        logger.error(BE)
        bot.send_message(callback.message.from_user.id, 'Упс... Что-то пошло не так. Повтори команду заново')