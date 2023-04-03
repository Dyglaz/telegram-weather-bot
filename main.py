from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hi, {user.username}!\n"
        "This bot can help you to know weather in your city\n"
        "You can write /help to see available commands"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    text = "This bot provides functions for getting weather forecast" \
           "in you city." \
           "/draw_temp - get a temperature graph in specified city\n" \
           "/get_weather - get current weather in specified city"
    await update.message.reply_text(text)


# Function to send weather data to the user
async def send_weather_data(update, context):
    city = context.args[0]
    data = get_weather_data(city)
    weather = data['weather'][0]['description']
    temp = data['main']['temp']
    await update.message.reply_text(f'The weather in {city} is {weather} with a temperature of {temp}°C.')


# Function to draw a graph of the temperature over time for a specified city
async def draw_temperature_graph(update, context):
    city = context.args[0]
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=11f616aaccfbd3abcdac1210710f9092&' \
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


async def get_weather_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6035452843:AAHNewpow39j7ccTc9uqEvXXUFAvUG4ZFRI").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_weather", send_weather_data))
    application.add_handler(CommandHandler("draw_temp", draw_temperature_graph))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e. message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
