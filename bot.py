import telebot
from telebot import types

API_TOKEN = 'YOUR_BOT_TOKEN'

bot = telebot.TeleBot(API_TOKEN)

# In-memory storage (use a real DB for production)
users = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {'balance': 0, 'referrals': []}
    msg = (
        "Welcome to SOFTCOINNET Savings Bot!"

"
        "Commands:
"
        "`/save <amount>` – Log your savings
"
        "`/balance` – View total saved
"
        "`/refer` – Get your referral code
"
        "`/rewards` – See rewards from referrals
"
    )
    bot.send_message(user_id, msg, parse_mode="Markdown")

@bot.message_handler(commands=['save'])
def save_amount(message):
    try:
        amount = int(message.text.split()[1])
        user_id = message.from_user.id
        users[user_id]['balance'] += amount
        bot.send_message(user_id, f"₦{amount} saved! Total: ₦{users[user_id]['balance']}")
    except:
        bot.send_message(message.chat.id, "Usage: /save 500")

@bot.message_handler(commands=['balance'])
def check_balance(message):
    user_id = message.from_user.id
    total = users.get(user_id, {}).get('balance', 0)
    bot.send_message(user_id, f"Your current savings: ₦{total}")

@bot.message_handler(commands=['refer'])
def refer_user(message):
    user_id = message.from_user.id
    referral_link = f"https://t.me/YOUR_BOT_USERNAME?start={user_id}"
    bot.send_message(user_id, f"Your referral link:
{referral_link}")

@bot.message_handler(commands=['rewards'])
def check_rewards(message):
    user_id = message.from_user.id
    referrals = users.get(user_id, {}).get('referrals', [])
    bot.send_message(user_id, f"You have {len(referrals)} referrals.")

print("Bot is running...")
bot.polling()
