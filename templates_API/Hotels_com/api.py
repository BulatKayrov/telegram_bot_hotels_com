from typing import List, Tuple, Any

import requests
from create_bot import API_KEY_HOTELS_COM


def get_search_location(city: str) -> list[tuple[str, str]]:
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q": city, "locale": "en_US"}

    headers = {
        "X-RapidAPI-Key": API_KEY_HOTELS_COM,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring).json()
    result = []

    for first_data in response['sr']:
        for key in first_data.keys():
            if key == 'gaiaId':
                result.append((first_data['regionNames']['shortName'], first_data[key]))

    return result


def post_hotels_list(city_id: str, count_hotels: str, day: str,
                     month: str, year: str, command: str, priceIn=None, priceOut=None) -> \
        List[Tuple[Any, Any, Any, Any]]:
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": city_id},
        "checkInDate": {"day": int(day), "month": int(month), "year": int(year)},
        "checkOutDate": {"day": int(day), "month": int(month), "year": int(year)},
        "rooms": [{"adults": 1}],
        "resultsStartingIndex": 0,
        "resultsSize": int(count_hotels),
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {}
    }

    if command == 'lowprice':
        payload["sort"] = "PRICE_LOW_TO_HIGH"
    if command == 'highprice':
        payload["sort"] = "PRICE_RELEVANT"
    if command == 'bestdeal':
        payload["filters"]["price"] = {"max": priceOut, "min": priceIn}
        payload["filters"]["guestRating"] = "40"
        payload["sort"] = "RECOMMENDED"

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": API_KEY_HOTELS_COM,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers).json()
    data_list = []

    for i in response['data']['propertySearch']['properties']:
        data_list.append((i['name'], i['id'], i['reviews']['score'], i['price']['options'][0]['formattedDisplayPrice']))
    return data_list


def detail_information(id_hotels: str, N: str) -> dict:
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": id_hotels
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": API_KEY_HOTELS_COM,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers).json()

    hotels_info = {
        'name': response['data']['propertyInfo']['summary']['name'],
        'address': response['data']['propertyInfo']['summary']['location']['address']['addressLine'],
        'coordinates': response['data']['propertyInfo']['summary']['location']['coordinates'],
        'description': response['data']['propertyInfo']['summary']['tagline'],
        'images': []
    }

    for i, v in enumerate(response['data']['propertyInfo']['propertyGallery']['images']):
        if i != int(N):
            hotels_info['images'].append(v['image']['url'])
        else:
            break

    return hotels_info


a = get_search_location(city='Los Angeles')
print(a)
