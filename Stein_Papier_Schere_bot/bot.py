import random
import time
import telebot
from telebot import types

# Your Telegram Bot API token
TOKEN = "7335497577:AAFRvjli9ZKQFnn2OCh-x_Hx5pOUbBV7Bps"
bot = telebot.TeleBot(TOKEN)

# Game options in German
OPTIONS = ['Stein', 'Schere', 'Papier']
IMAGES = {
    'Stein': 'images/rock.png',  # Rock image
    'Schere': 'images/scissors.png',  # Scissors image
    'Papier': 'images/paper.png'  # Paper image
}

# Game rules: what beats what
RULES = {
    'Stein': 'Schere',  # Rock beats Scissors
    'Schere': 'Papier',  # Scissors beat Paper
    'Papier': 'Stein'  # Paper beats Rock
}


# Start command handler
@bot.message_handler(commands=['start'])
def start(message):
    """
    Sends a greeting message and displays game options using buttons.
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Stein')
    btn2 = types.KeyboardButton('Schere')
    btn3 = types.KeyboardButton('Papier')
    markup.add(btn1, btn2, btn3)
    bot.send_message(
        message.chat.id,
        "Hallo! Lass uns 'Schere, Stein, Papier' spielen. Wähle deine Option:",
        reply_markup=markup
    )


# Game logic handler
@bot.message_handler(func=lambda message: message.text in OPTIONS)
def play_game(message):
    """
    Handles the game logic. Compares the user's choice with the bot's random choice.
    """
    user_choice = message.text

    # Добавляем задержку для имитации обдумывания выбора ботом
    time.sleep(random.uniform(1, 3))

    # Используем более сложный рандом
    bot_choice = random.choices(
        population=OPTIONS,
        weights=[0.33, 0.33, 0.34],  # Почти равные шансы
        k=1
    )[0]

    # Send the bot's choice as an image
    with open(IMAGES[bot_choice], 'rb') as photo:
        bot.send_photo(
            message.chat.id,
            photo,
            caption=f"Ich habe gewählt: {bot_choice}"
        )

    # Determine the result
    if user_choice == bot_choice:
        result = 'Unentschieden'
    elif RULES[user_choice] == bot_choice:
        result = 'Du hast gewonnen'
    else:
        result = 'Du hast verloren'

    # Send the result as text instead of an image
    bot.send_message(
        message.chat.id,
        f"{result}!"
    )

    # Ask if the user wants to play again
    bot.send_message(
        message.chat.id,
        "Möchtest du noch einmal spielen? Wähle: Stein, Schere oder Papier."
    )


# Main entry point
if __name__ == '__main__':
    """
    Starts the bot and keeps it running indefinitely.
    """
    bot.polling(none_stop=True)