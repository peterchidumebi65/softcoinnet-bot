
import telebot
import json
import os
TOKEN = 'AAHXyZ7Odiz2fvs5fq-7ZFR-gCyTRrDGAho'
bot = telebot.TeleBot(TOKEN)
DATA_FILE = 'data.json'
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        users = json.load(f)
else:
    users = {}
def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)
wallets = {
    "BTC": "bc1qg7amlpgxlxz3hvynl57l3dym37cyect0vhxhn8",
    "USDT (TRC20)": "TY9MUw3gPZBnHmCymaeho9AdeowfnvCcPg"
}
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    if user_id not in users:
        users[user_id] = {
            'balance': 0,
            'referrals': [],
            'ref_code': f'ref{user_id}',
            'rewards': 0
        }
        save_data()
    text = (
        "Welcome to *SOFTCOINNET Savings Bot!*"
        "Hello"
        message = """Welcome to SOFTCOINNET Savings Bot!
Commands:
/start - Start the bot
/help - Help info
/save - Save money
/balance - Check your balance
/referral - Get referral link
"""
    "/rewards - View your referral rewards\n"
        message = """Welcome to SOFTCOINNET!
Here are your commands:
/start – Start the bot
/save <amount> – Log your savings
/balance – Check your total saved
/refer – Get your referral link
/rewards – View referral rewards
"""
await message.reply(message) "`/save <amount>` – Log your savings
"
        "`/balance` – View total saved
"
        "`/refer` – Get your referral link
"
        "`/rewards` – View your referral reward"
        "*Wallet Addresses:*
"
       f"BTC: `{wallets['BTC']}`
"
        f"USDT (TRC20): `{wallets['USDT (TRC20)']}`"
    )
    bot.send_message(user_id, text, parse_mode="Markdown")

@bot.message_handler(commands=['save'])
def save(message):
    try:
        amount = int(message.text.split()[1])
        user_id = str(message.from_user.id)
        users[user_id]['balance'] += amount
        save_data()
        bot.send_message(user_id, f"₦{amount} saved! Total: ₦{users[user_id]['balance']}")
    except:
        bot.send_message(message.chat.id, "Usage: /save 500")
@bot.message_handler(commands=['balance'])
def balance(message):
    user_id = str(message.from_user.id)
    total = users.get(user_id, {}).get('balance', 0)
    bot.send_message(user_id, f"Your savings balance: ₦{total}")
@bot.message_handler(commands=['refer'])
def refer(message):
    user_id = str(message.from_user.id)
    ref_code = users[user_id]['ref_code']
    link = f"https://t.me/SOFTCOINNETBot?start={ref_code}"
    bot.send_message(user_id, f"Invite friends with this link:
{link}")
@bot.message_handler(commands=['rewards'])
def rewards(message):
    user_id = str(message.from_user.id)
    reward = users[user_id]['rewards']
    count = len(users[user_id]['referrals'])
    bot.send_message(user_id, f"Referrals: {count}
Reward earned: ₦{reward}")
@bot.message_handler(func=lambda m: m.text.startswith("/start ref"))
def handle_referral(message):
    user_id = str(message.from_user.id)
    ref_code = message.text.split(" ")[1]
    referrer = next((uid for uid, data in users.items() if data['ref_code'] == ref_code), None)
    if referrer and referrer != user_id and user_id not in users[referrer]['referrals']:
        users[referrer]['referrals'].append(user_id)
        users[referrer]['rewards'] += 100
        save_data()
        bot.send_message(int(referrer), "You earned ₦100 for a new referral!")
    start(message)
bot.polling()
