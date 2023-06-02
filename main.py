import requests
import datetime
from pprint import pprint
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(f"Приветствую Вас, {message.from_user.username}!\n"
                        "Этот бот может помочь вам узнать погоду в определённом городе или стране.\n"
                        "Вы можете написать /help, чтобы просмотреть доступные команды.")


@dp.message_handler(commands=["help"])
async def start_command(message: types.Message):
    await message.reply("Для получение прогноза погоды введите название города или страны."
                        "/draw_temp - get a temperature graph in specified city\n"
                        "/get_weather - get current weather in specified city")


@dp.message_handler()
async def get_weather_command(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        url = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units"
            f"=metric&lang=ru")
        data = url.json()
        # pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Иконку погоды не удалось определить"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                            f"Локация: {city}\nТемпература: {cur_weather} C°\n"
                            f"{wd}\n"
                            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
                            f"Продолжительность дня: {length_of_the_day}\n\n"
                            f"Хорошего Вам дня!")

    except:
        await message.reply("\U00002620 Проверьте правильность записи названия города \U00002620")


if __name__ == "__main__":
    executor.start_polling(dp)

# async def start(update: Update, context) -> None:
#     """Sends a message when the command /start is issued."""
#     user = update.effective_user
#     await update.message.reply_text(
#         f"Hi, {user.username}!\n"
#         "This bot can help you to know weather in your city\n"
#         "You can write /help to see available commands"
#     )
#
#
# async def help_command(update: Update, context) -> None:
#     """Sends a message when the command /help is issued."""
#     text = "This bot provides functions for getting weather forecast" \
#            "in you city." \
#            "/draw_temp - get a temperature graph in specified city\n" \
#            "/get_weather - get current weather in specified city"
#     await update.message.reply_text(text)


# def draw_temperature_graph(city):
#     """Нарисовать график температуры для указанного города
#      (параметр: Целевой город, возвращает: Графическое изображение)"""
#
#     url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&' \
#           f'units=metric&lang=ru'
#     response = requests.get(url)
#     data = response.json()
#     temps = [forecast['main']['temp'] for forecast in data['list'][:8]]
#     fig, ax = plt.subplots()
#     ax.plot(temps)
#     ax.grid()
#     ax.set_title(f'Temperature over time in {city}')
#     ax.set_xlabel('Time')
#     ax.set_ylabel('Temperature (°C)')
#     canvas = FigureCanvas(fig)
#     buf = io.BytesIO()
#     canvas.print_png(buf)
#     data = buf.getvalue()
#     return data
