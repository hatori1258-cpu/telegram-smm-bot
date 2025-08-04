import telebot

bot = telebot.TeleBot("YOUR_BOT_TOKEN")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "✅ Welcome to First SMM Provider ✅\n\n🚀 Trusted and Fast SMM Services (Instagram, YouTube, Telegram & more)\n⚡ Instant delivery | Low rates | Real proof below 👇\n\nTo get started, type any keyword like Instagram, YouTube, etc.")

@bot.message_handler(func=lambda message: True)
def reply_all(message):
    bot.send_message(message.chat.id, "Please use the buttons or refer to the tutorial.")

bot.polling()
