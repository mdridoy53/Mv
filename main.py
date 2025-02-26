import telebot
import random
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import time

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = '7720695132:AAFg6E_Bh3OXs6aqhOPGVee3X9UoiqwD9qQ'
bot = telebot.TeleBot(BOT_TOKEN)

# Replace with your admin user ID(s)
ADMIN_USER_IDS = [7987662357]  # Replace with your admin user ID

# In-memory user data (replace with a database for persistence)
user_data = {}
tasks = {
    "1": {"link": "https://t.me/+h5cW8Gja49JkNWU1", "credits": 2, "description": "Join Channel"},
    "2": {"link": "https://www.effectiveratecpm.com/f7hrpvm2?key=fb69a6ec1f987419560a7f5abcb1f8a3", "credits": 5, "description": "Ads Click"},
    "3": {"link": "https://t.me/addlist/nOI9FC_EOxBlNGFl", "credits": 9, "description": "Add List"},
}

daily_claim_credits = 10  # Example daily claim amount
last_daily_claim = {}  # Store last claim time for each user

# Keyboard functions

def create_main_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add("Add 👤 Account", "💌 Invite", "Add Balance", "Complete All Tasks", "Buy Proxy", "Daily Claim", "/premium")
    return keyboard

def create_task_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    for task_id, task_info in tasks.items():
        keyboard.add(InlineKeyboardButton(f"Task {task_id}: {task_info['description']} (Earn {task_info['credits']} credits)", callback_data=f"task_{task_id}"))
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
        bot.send_message(user_id, "Checking, please wait for 20 seconds...")
        time.sleep(20)  # Simulate 20 seconds waiting
        total_credits = 0
        for task_id, task_info in tasks.items():
            if task_id not in user_data[user_id]["tasks_completed"]:
                total_credits += task_info["credits"]
                user_data[user_id]["tasks_completed"].add(task_id)
        user_data[user_id]["credits"] += total_credits
        bot.send_message(user_id, f"You completed all tasks and earned {total_credits} credits! Your total balance is: {user_data[user_id]['credits']} credits.")

@bot.message_handler(func=lambda message: message.text == "Buy Proxy")
def buy_proxy(message):
    user_id = check_user(message)
    bot.send_message(user_id, "Select a proxy:", reply_markup=create_task_keyboard())

@bot.message_handler(func=lambda message: message.text == "Show Tasks")
def show_tasks(message):
    user_id = check_user(message)
    bot.send_message(user_id, "Choose a task:", reply_markup=create_task_keyboard())

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

@bot.callback_query_handler(func=lambda call: call.data.startswith("task_"))
def handle_task(call):
    user_id = call.from_user.id
    task_id = call.data.split("_")[1]
    if task_id not in user_data[user_id]["tasks_completed"]:
        task_info = tasks.get(task_id)
        if task_info:
            user_data[user_id]["credits"] += task_info["credits"]
            user_data[user_id]["tasks_completed"].add(task_id)
            bot.send_message(user_id, f"You have completed the task '{task_info['description']}' and earned {task_info['credits']} credits!")
            bot.send_message(user_id, f"Your current balance is {user_data[user_id]['credits']} credits.")
        else:
            bot.send_message(user_id, "Task not found.")
    else:
        bot.send_message(user_id, "You have already completed this task.")
    bot.answer_callback_query(call.id)

@bot.message_handler(commands=['show_users'])
def show_users(message):
    user_id = message.from_user.id
    if user_id in ADMIN_USER_IDS:
        user_list = "\n".join([str(uid) for uid in user_data.keys()])
        bot.send_message(user_id, f"Users: \n{user_list}")
    else:
        bot.send_message(user_id, "You are not authorized to use this command.")

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
