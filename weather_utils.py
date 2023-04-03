import config
import requests
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


API_KEY = config.openweatherAPI
BASE_URL = ""


def draw_temperature_graph(city):
    """Draw temperature graph for specified city

    :param city: Target city
    :returns: Graph picture
    """
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&' \
          f'units=metric&lang=ru'
    response = requests.get(url)
    data = response.json()
    temps = [forecast['main']['temp'] for forecast in data['list'][:8]]
    fig, ax = plt.subplots()
    ax.plot(temps)
    ax.grid()
    ax.set_title(f'Temperature over time in {city}')
    ax.set_xlabel('Time')
    ax.set_ylabel('Temperature (°C)')
    canvas = FigureCanvas(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)
    data = buf.getvalue()
    return data


def get_weather_data(city):
    """Get weather data in specified city

    :param city: Target city
    :returns: Weather data in json format
    """
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&' \
          f'units=metric&lang=ru'
    response = requests.get(url)
    data = response.json()
    return data


#draw_temperature_graph("Moscow")
