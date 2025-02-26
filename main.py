import telebot
import random
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = '7913586877:AAERsnpgde4yGphlpEZqjmo53kFKWoaEVVg'
bot = telebot.TeleBot(BOT_TOKEN)

# Replace with your admin user ID(s)
ADMIN_USER_IDS = [7987662357]  # Replace with your admin user ID

# In-memory user data (replace with a database for persistence)
user_data = {}
proxy_data = {
    "1": {
        "IP": "188.245.189.170",
        "Port": "44366",
        "User": "DAvzDk",
        "Password": "0e7y53",
        "Country": "USA",
        "Price": 2,  # Price in credits
    }
}
tasks = {
    "1": {"link": "https://t.me/+h5cW8Gja49JkNWU1", "credits": 2, "description": "Join Channel"},
    "2": {"link": "https://www.effectiveratecpm.com/f7hrpvm2?key=fb69a6ec1f987419560a7f5abcb1f8a3", "credits": 5, "description": "Ads Click"},
    "3": {"link": "https://t.me/addlist/nOI9FC_EOxBlNGFl", "credits": 9, "description": "Add List"},
}

daily_claim_credits = 10  # Example daily claim amount
last_daily_claim = {}  # Store last claim time for each user

# State for adding new proxies
proxy_add_state = {}

# Keyboard functions

def create_main_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add("Add 👤 Account", "💌 Invite", "Add Balance", "Complete All Tasks", "Buy Proxy", "Daily Claim", "/premium")
    return keyboard

def create_proxy_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    for proxy_id in proxy_data:
        keyboard.add(telebot.types.InlineKeyboardButton(f"Proxy {proxy_id}", callback_data=f"buy_proxy_{proxy_id}"))
    return keyboard

def check_user(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"credits": 0, "tasks_completed": set(), "premium": False}
    return user_id

# Bot commands

@bot.message_handler(commands=['start'])
def start(message):
    user_id = check_user(message)
    bot.send_message(user_id, "Welcome To Socks Proxy Bot\nEnjoy free Proxy Premium Proxy", reply_markup=create_main_keyboard())

@bot.message_handler(commands=['premium'])
def premium(message):
    user_id = check_user(message)
    if user_data[user_id]["premium"]:
        bot.send_message(user_id, "You are already a Premium User.")
    else:
        bot.send_message(user_id, "You are not a Premium User. Contact admin to get premium access.")

@bot.message_handler(func=lambda message: message.text == "Complete All Tasks")
def complete_all_tasks(message):
    user_id = check_user(message)
    if len(tasks) == len(user_data[user_id]["tasks_completed"]):
        bot.send_message(user_id, "You have already completed all tasks!")
    else:
        total_credits = 0
        for task_id, task_info in tasks.items():
            if task_id not in user_data[user_id]["tasks_completed"]:
                total_credits += task_info["credits"]
                user_data[user_id]["tasks_completed"].add(task_id)
        user_data[user_id]["credits"] += total_credits
        bot.send_message(user_id, f"You Task Joine Now = https://t.me/+h5cW8Gja49JkNWU1 completed all tasks and earned {total_credits} credits! Your total balance is: {user_data[user_id]['credits']} credits.")

@bot.message_handler(func=lambda message: message.text == "Buy Proxy")
def buy_proxy(message):
    user_id = check_user(message)
    bot.send_message(user_id, "Select a proxy:", reply_markup=create_proxy_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_proxy_"))
def buy_proxy_callback(call):
    user_id = call.from_user.id
    proxy_id = call.data.split("_")[2]
    if proxy_id in proxy_data:
        proxy = proxy_data[proxy_id]
        if user_data[user_id]["credits"] >= proxy["Price"]:
            user_data[user_id]["credits"] -= proxy["Price"]
            proxy_info = f"Proxy Information:\nIP: {proxy['IP']}\nPort: {proxy['Port']}\nUser: {proxy['User']}\nPassword: {proxy['Password']}\nCountry: {proxy['Country']}"
            bot.send_message(user_id, proxy_info)
            bot.send_message(user_id, f"You bought Proxy {proxy_id} for {proxy['Price']} credits. Your balance is now: {user_data[user_id]['credits']} credits.")
        else:
            bot.send_message(user_id, "Insufficient credits.")
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: message.text == "Add Balance")
def add_balance(message):
    user_id = check_user(message)
    bot.send_message(user_id, "Please contact @darkkkjht to add balance.")  # Replace with your admin's username

@bot.message_handler(func=lambda message: message.text == "Daily Claim")
def daily_claim(message):
    user_id = check_user(message)
    now = datetime.datetime.now()
    if user_id in last_daily_claim:
        time_diff = now - last_daily_claim[user_id]
        if time_diff.total_seconds() < 86400:  # 86400 seconds = 24 hours
            remaining_time = 86400 - time_diff.total_seconds()
            hours = int(remaining_time // 3600)
            minutes = int((remaining_time % 3600) // 60)
            seconds = int(remaining_time % 60)
            bot.send_message(user_id, f"You can claim again in {hours} hours, {minutes} minutes, and {seconds} seconds.")
            return

    user_data[user_id]["credits"] += daily_claim_credits
    last_daily_claim[user_id] = now
    bot.send_message(user_id, f"You claimed {daily_claim_credits} credits! Your balance is now: {user_data[user_id]['credits']} credits.")

@bot.message_handler(func=lambda message: message.text == "✅ Update Channels")
def invite(message):
    user_id = check_user(message)
    bot.send_message(user_id, "Joine Update Channels: https://t.me/dar3658")  # Replace with your referral link logic

@bot.message_handler(func=lambda message: message.text == "Add 👤 Account")
def add_account(message):
    user_id = check_user(message)
    bot.send_message(user_id, "Please contact @darkkkjht to add an account.")  # Replace with your admin's username

@bot.message_handler(commands=['new'])
def new_proxy_command(message):
    user_id = message.from_user.id
    if user_id in ADMIN_USER_IDS:
        proxy_add_state[user_id] = {}  # Initialize state for this user
        bot.send_message(user_id, "Enter the proxy IP:")
    else:
        bot.send_message(user_id, "You are not authorized to use this command.")

@bot.message_handler(func=lambda message: message.from_user.id in proxy_add_state)
def process_new_proxy_info(message):
    user_id = message.from_user.id
    if "IP" not in proxy_add_state[user_id]:
        proxy_add_state[user_id]["IP"] = message.text
        bot.send_message(user_id, "Enter the proxy Port:")
    elif "Port" not in proxy_add_state[user_id]:
        proxy_add_state[user_id]["Port"] = message.text
        bot.send_message(user_id, "Enter the proxy Username:")
    elif "User" not in proxy_add_state[user_id]:
        proxy_add_state[user_id]["User"] = message.text
        bot.send_message(user_id, "Enter the proxy Password:")
    elif "Password" not in proxy_add_state[user_id]:
        proxy_add_state[user_id]["Password"] = message.text
        bot.send_message(user_id, "Enter the proxy Country:")
    elif "Country" not in proxy_add_state[user_id]:
        proxy_add_state[user_id]["Country"] = message.text
        bot.send_message(user_id, "Enter the proxy Price (in credits):")
    elif "Price" not in proxy_add_state[user_id]:
        try:
            proxy_add_state[user_id]["Price"] = int(message.text)
            # Add the new proxy to proxy_data
            new_proxy_id = str(len(proxy_data) + 1)  # Simple ID generation
            proxy_data[new_proxy_id] = proxy_add_state[user_id]
            bot.send_message(user_id, f"Proxy added successfully with ID: {new_proxy_id}")
            del proxy_add_state[user_id]  # Clear the state
        except ValueError:
            bot.send_message(user_id, "Invalid price. Please enter a number.")

# Admin Commands

@bot.message_handler(commands=['show_users'])
def show_users(message):
    user_id = message.from_user.id
    if user_id in ADMIN_USER_IDS:
        user_list = "\n".join([str(uid) for uid in user_data.keys()])
        bot.send_message(user_id, f"Users: \n{user_list}")
    else:
        bot.send_message(user_id, "You are not authorized to use this command.")

@bot.message_handler(commands=['show_notifications'])
def show_notifications(message):
    user_id = message.from_user.id
    if user_id in ADMIN_USER_IDS:
        bot.send_message(user_id, "Enter the message to send to all users:")
        bot.register_next_step_handler(message, send_notification)
    else:
        bot.send_message(user_id, "You are not authorized to use this command.")

def send_notification(message):
    notification_text = message.text
    for user_id in user_data.keys():
        bot.send_message(user_id, notification_text)
    bot.send_message(message.from_user.id, "Notification sent to all users.")

@bot.message_handler(commands=['show_total_users'])
def show_total_users(message):
    user_id = message.from_user.id
    if user_id in ADMIN_USER_IDS:
        total_users = len(user_data)
        bot.send_message(user_id, f"Total bot users: {total_users}")
    else:
        bot.send_message(user_id, "You are not authorized to use this command.")

# Main loop to start the bot
def main():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()
