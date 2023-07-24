from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from templates_API.Hotels_com.api import get_search_location, post_hotels_list
from callBack_data.callback_data import SEARCH_LOCATION, NEED_PHOTO, COUNT_PHOTO, ID_HOTEL, RATING, PRICE
from emoji import emojize


def inline_get_city(city: str) -> InlineKeyboardMarkup:
    """Функция выводящая список городов"""
    reply_markup = InlineKeyboardMarkup()
    response = get_search_location(city=city)
    for cities in response:
        SEARCH_LOCATION.append(cities[1])
        reply_markup.add(InlineKeyboardButton(text=cities[0], callback_data=cities[1]))
    return reply_markup


def inline_need_photo() -> InlineKeyboardMarkup:
    """Функция спрашивающая у пользователя необходимость загрузки фотографий"""
    reply_markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text=f'{emojize("✅")}', callback_data=NEED_PHOTO[0]),
        InlineKeyboardButton(text=f'{emojize("❌")}', callback_data=NEED_PHOTO[1]),
    )
    return reply_markup


def inline_count_photo() -> InlineKeyboardMarkup:
    """Функция уточняющая у пользователя кол-во фотографий"""
    reply_markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text=f'{emojize("3️⃣")}', callback_data=str(COUNT_PHOTO[0])),
        InlineKeyboardButton(text=f'{emojize("5️⃣")}', callback_data=str(COUNT_PHOTO[1])),
        InlineKeyboardButton(text=f'{emojize("7️⃣")}', callback_data=str(COUNT_PHOTO[2])),
    )

    return reply_markup


def inline_choise_hotel(city_id, count_hotels,
                        commands, day, month, year, priceIn=None, priceOut=None) -> InlineKeyboardMarkup:
    """Функция предоставляет выбор отеля"""
    response = post_hotels_list(city_id=city_id, count_hotels=count_hotels,
                                command=commands, day=day, month=month, year=year, priceIn=priceIn, priceOut=priceOut)
    reply_markup = InlineKeyboardMarkup()
    for hotel in response:
        RATING[hotel[1]] = hotel[2]
        PRICE[hotel[1]] = hotel[3]
        ID_HOTEL.append(hotel[1])
        reply_markup.add(InlineKeyboardButton(text=f'{hotel[0][:30]}',
                                              callback_data=hotel[1]))

    return reply_markup


