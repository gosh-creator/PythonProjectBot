import json
import requests




def get_city_location_key(api_key, city_name):
    """
    получаем ключ от конкретной локации для дальнейшего определения погоды в этой локации
    :param api_key:
    :param city_name:
    :return: int
    """
    r = requests.get(f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey={api_key}&q={city_name}').json()


    with open('weather_of_the_cities.json', 'w') as outfile:
        json.dump(r, outfile, indent=4)


    return r[0]['Key']


def get_forecast_city_by_name(api_key: str, city_name: str, days: int):

    """
    получаем информацию о погоде на 1 день и возвращаем основные параметры
    :param api_key:
    :param city_name:
    :param days
    :return: json
    """
    city_loc_key = get_city_location_key(api_key, city_name)

    if days == 0:

        weather_url = f'http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{city_loc_key}'
        params = {
            "apikey": api_key,
            "details": "true"
        }
        response = requests.get(weather_url, params=params).json()


    elif days == 5:

        try:
            weather_url = f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{city_loc_key}'
            params = {
                "apikey": api_key,
                "details": "true"
            }
            response = requests.get(weather_url, params=params).json()

        except Exception as e:

            print(f"Ошибка при запросе к API: {e}")
            return None


    elif days == 3:

        try:
            weather_url = f'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{city_loc_key}'
            params = {
                "apikey": api_key,
                "details": "true"
            }
            response = requests.get(weather_url, params=params).json()

        except Exception as e:

            print(f"Ошибка при запросе к API: {e}")
            return None

    else:
        return 'no more вариантов'

    with open('weather.json', 'w') as outfile:
        json.dump(response, outfile, indent=4)


    data = {
        'Temperature_Minimum': response['DailyForecasts'][0]['Temperature']['Minimum']['Value'],
        'Temperature_Maximum': response['DailyForecasts'][0]['Temperature']['Maximum']['Value'],
        'RealFeelTemperature': response['DailyForecasts'][0]['RealFeelTemperature']['Minimum']['Value'],
        'Speed_Wind': response['DailyForecasts'][0]['Day']['Wind']['Speed']['Value'],
        'Humidity': response['DailyForecasts'][0]['Night']['RelativeHumidity']['Average'],
        'Rain_Probability': response['DailyForecasts'][0]['Day']['RainProbability'],
    }

    return data

def presentation_of_the_data(data):
    for key, value in data:
        print(f'{key}: {value}\n')

def check_bad_weather(data):
    weather_cool_or_bad = True
    trace = 0
    if data['Temperature_Minimum'] not in (-80, 80) or data['Temperature_Maximum'] not in (-80, 80): return 'Some problems with this data :('


    if data['Temperature_Minimum'] < 0 or data['Temperature_Maximum'] > 30: trace += 1
    if data['SpeedWind'] > 10 and data['SpeedWind'] in (0, 30): trace += 1
    if data['Humidity'] > 0.7 and data['Humidity'] in (0, 1): trace += 1
    if data['Rain_Probability'] > 0 and data['Rain_Probability'] in (0, 1): trace += 1

    if trace > 2: weather_cool_or_bad = False
    return weather_cool_or_bad

