from . import config
from . import weather_utils
from telegram import Update
from telegram.ext import Application, CommandHandler

TELEGRAM_TOKEN = config.telegramBotToken


async def start(update: Update, context) -> None:
    """Sends a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hi, {user.username}!\n"
        "This bot can help you to know weather in your city\n"
        "You can write /help to see available commands"
    )


async def help_command(update: Update, context) -> None:
    """Sends a message when the command /help is issued."""
    text = "This bot provides functions for getting weather forecast" \
           "in you city." \
           "/draw_temp - get a temperature graph in specified city\n" \
           "/get_weather - get current weather in specified city"
    await update.message.reply_text(text)


async def send_weather_data(update, context):
    """Sends a message with weather when the /get_weather command is issued"""
    if len(context.args) == 0:
        await update.message.reply_text("Specify the city")
    city = context.args[0]
    data = weather_utils.get_weather_data(city)
    weather = data['weather'][0]['description']
    temp = data['main']['temp']
    await update.message.reply_text(f'The weather in {city} is {weather} with a temperature of {temp}°C.')


async def get_temperature_graph(update, context):
    """Sends a temperature graph when the /get_graph command is issued"""
    if len(context.args) == 0:
        await update.message.reply_text("Specify the city")
    city = context.args[0]
    graph_path = weather_utils.draw_temperature_graph(city)
    await update.message.reply_photo(graph_path, caption=f"Weather graph in {city}")


def main() -> None:
    """Main function to start the bot"""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("get_weather", send_weather_data))
    application.add_handler(CommandHandler("get_graph", get_temperature_graph))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
