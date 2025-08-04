from telebot import TeleBot, types
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("8398204788:AAHXVQQAOwcFymprH1-Vv8x-eQN4tJGSBe4")
CHANNEL_USERNAME = "@First_smm_provider"
ADMIN_USERNAME = "@Sharik_pathan"

bot = TeleBot(BOT_TOKEN)

# In-memory user data (reset on bot restart)
user_data = {}  # user_id: {"points": int, "referred_by": int, "referrals": []}

# Generate referral link
def get_referral_link(user_id):
    return f"https://t.me/{bot.get_me().username}?start={user_id}"

# Check channel join (simulated)
def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    args = message.text.split()

    if user_id not in user_data:
        user_data[user_id] = {"points": 0, "referred_by": None, "referrals": []}

    # Handle referral
    if len(args) > 1:
        ref_id = int(args[1])
        if ref_id != user_id and user_data[user_id]["referred_by"] is None:
            user_data[user_id]["referred_by"] = ref_id
            user_data[ref_id]["referrals"].append(user_id)
            user_data[ref_id]["points"] += 15

    if not is_user_in_channel(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}", callback_data="check_join"))
        bot.send_message(user_id, "🚨 Please join our channel to continue:", reply_markup=markup)
        return

    send_main_menu(user_id)

def send_main_menu(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📦 How to Order", url="https://t.me/First_smm_provider/8"),
        types.InlineKeyboardButton("💰 Add Funds - PhonePe", url="https://t.me/First_smm_provider/33"),
        types.InlineKeyboardButton("💳 Add Funds - Others", url="https://t.me/First_smm_provider/34")
    )
    markup.add(types.InlineKeyboardButton("👤 Account", callback_data="account"))
    bot.send_message(user_id, "👋 Welcome to First SMM Provider!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id

    if call.data == "account":
        points = user_data.get(user_id, {}).get("points", 0)
        ref_link = get_referral_link(user_id)

        msg = f"👤 Your Account\n\n💎 Points: {points}\n🔗 Referral Link: {ref_link}"

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📤 Drop Members (350 pts)", callback_data="drop"))
        markup.add(types.InlineKeyboardButton("💸 Buy Points", url=f"https://t.me/{ADMIN_USERNAME[1:]}"))
        markup.add(types.InlineKeyboardButton("➕ More Services", url="https://t.me/First_smm_provider"))
        markup.add(types.InlineKeyboardButton("🤖 Buy this Bot", url=f"https://t.me/{ADMIN_USERNAME[1:]}"))
        bot.edit_message_text(msg, user_id, call.message.message_id, reply_markup=markup)

    elif call.data == "drop":
        if user_data[user_id]["points"] >= 350:
            user_data[user_id]["points"] -= 350
            bot.answer_callback_query(call.id, "✅ Members dropped successfully!")
            bot.send_message(user_id, "🎯 Your drop request has been received!")
        else:
            bot.answer_callback_query(call.id, "❌ Not enough points!")

print("🤖 Bot is running...")
bot.infinity_polling()




