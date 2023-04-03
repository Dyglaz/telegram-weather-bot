import config
import requests
import matplotlib.pyplot as plt
from datetime import datetime

API_KEY = config.openweatherAPI
BASE_URL = ""

# Function to draw a graph of the temperature over time for a specified city
def draw_temperature_graph(update, context):
    city = context.args[0]
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&' \
          f'units=metric&lang=ru'
    response = requests.get(url)
    data = response.json()
    temps = [forecast['main']['temp'] for forecast in data['list'][:8]]
    graph_name = f"graph-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
    graph_path = "user_graphs/" + graph_name + ".png"
    plt.plot(temps)
    plt.title(f'Temperature over time in {city}')
    plt.xlabel('Time (3 hour intervals)')
    plt.ylabel('Temperature (°C)')
    plt.savefig(graph_path)
    # plt.show()
    plt.close()
    await update.message.reply_photo(graph_path, caption=f"Weather graph in {city}")


# Function to get weather data for a specified city
def get_weather_data(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=11f616aaccfbd3abcdac1210710f9092&' \
          f'units=metric&lang=ru'
    response = requests.get(url)
    data = response.json()
    return data
