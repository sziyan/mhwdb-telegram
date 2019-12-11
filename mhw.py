#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
database_category = ["ailments", "armor", "armor_sets", "charms", "decorations", "events", "items", "locations", "monsters", "skills", "weapons"]

def search_db(category,name):
    #'https://mhw-db.com/events?q={"platform":"console"}'
    query = 'https://mhw-db.com/' + category + '?q={"name":"' + name + '"}'
    r = requests.get(query)
    if len(r.json()) > 0:
        reply = r.json()[0]
    else:
        reply = "invalid"
    return reply

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello! I am a bot that can output information from your search terms! \nType /help for my commands.')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('My available commands are: \n /monsters <monster name> - Search for monster')

def search(update, context):
    valid = False
    category = context.args[0]
    name = context.args[1]
    for u in database_category:
        if u == category:
            valid = True
    if valid is True:
        result = search_db(category, name)
        update.message.reply_text(result)

def monsters(update, context):
    if len(context.args) == 0:
        update.message.reply_text("Please input monster name to search.")
    category = 'monsters'
    name = " ".join(context.args)
    weakness = []
    ailments = []
    result = search_db(category, name)

    if result != "invalid":
        all_weakness = result.get('weaknesses')
        for w in all_weakness:
            if w.get('stars') > 2:
                weakness.append(w.get('element'))

        all_ailments = result.get('ailments')
        for a in all_ailments:
            ailments.append(a.get('name'))

        monster_ailments = ",".join(ailments)
        monster_weakness = ','.join(weakness)
        description = result.get('description')
        monster_name = result.get('name')

        monster_name_msg = "*Name*: {}".format(monster_name)
        description_msg = "*Description*: {}".format(description)
        weakness_msg = "*Weaknesses*: {}".format(monster_weakness)
        ailments_msg = "*Ailments:* {}".format(monster_ailments)

        message = "{} \n{} \n{} \n{}".format(monster_name_msg,description_msg,weakness_msg,ailments_msg)
        update.message.reply_markdown(message, quote=True)
    elif name.startswith("@"):
        return
    else:
        update.message.reply_text("Unable to find this monster! Iceborne data not yet updated.")

# def echo(update, context):
#     """Echo the user message."""
#     update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("827496100:AAEohD9TDG-F6fefu6MTqnuA86ktBdEta94", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(CommandHandler("monsters", monsters))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()