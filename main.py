import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Get credentials from environment variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

# Weather fetch function
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description'].capitalize()
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        return f"Weather in {city.title()}:\nTemperature: {temp}°C\nCondition: {desc}\nHumidity: {humidity}%\nWind Speed: {wind} m/s"
    else:
        return "City not found. Please try again."

# Command handler
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        city = " ".join(context.args)
        weather_info = get_weather(city)
        await update.message.reply_text(weather_info)
    else:
        await update.message.reply_text("Usage: /weather cityname")

# Bot initialization
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("weather", weather))
    print("Bot is running...")
    app.run_polling()