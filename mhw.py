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
import urllib.parse

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

#TOKEN = "827496100:AAEohD9TDG-F6fefu6MTqnuA86ktBdEta94" #mhwdb token
TOKEN = '180665590:AAGEXQVVWTzpou9TBekb8oq59cjz2Fxp_gY' #ascension token

# Enable logging
logging.basicConfig(format='LOG: %(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
database_category = ["ailments", "armor", "armor_sets", "charms", "decorations", "events", "items", "locations", "monsters", "skills", "weapons"]

def search_db(category,name): #search database with arguments given
    name_parse = urllib.parse.quote(name)
    query = 'https://mhw-db.com/' + category + '?q={"name":"' + name_parse + '"}'
    r = requests.get(query)
    result = r.json()
    if len(result) > 0: #if at least 1 result
        if type(result) is list: #if result is list aka more than 1 result
            reply = result[0] #get first result only
        elif type(result) is dict: #if result is dict type
            reply = result
        else:
            print('error in json type')
            return 'invalid'
    else: #no result meaning search failed
        if category == 'decorations':
            check_name = name.split()
            if int(name[-1]) <=4:
                level = int(name[-1])
                reply = search_deco(name,level)
            elif int(name[-1]) >= 5 and check_name[-2] == "Jewel":
                level = -1  # meaning search all jewel type, still cant find
                reply = search_deco(name, level)
            else:
                reply = 'invalid'
        else:
            reply = "invalid"
    return reply

def search_deco(name,level): #search thru deco
    name_list = name.split()
    if 0 < level <= 4:
        level+=1
        name_list[-1] = str(level)
        name = " ".join(name_list)
        reply = search_db('decorations', name)
    elif level == -1:
        level = 1
        name_list[-2] = 'Jewel+'
        name_list[-1] = str(level)
        name = " ".join(name_list)
        reply = search_db('decorations',name)
    else:
        reply = 'invalid'
    return reply


def get_weapon_name(weapon_id):
    query = 'https://mhw-db.com/weapons/' + str(weapon_id)
    r = requests.get(query)
    result = r.json()
    weapon_name = result.get('name')
    return weapon_name

def getassetlink(url):
    link = url.replace("\/","/")
    return link

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello! I am a bot that can output information from your search terms! \nType /help for my commands.')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Press the "/" button on your keyboard to checkout what I am capable of!')

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
    #if user input command with no arguments (monster names) after the command
    if len(context.args) == 0:
        update.message.reply_text("Command syntax is /monsters <monster name>")
        return
    #declaration
    category = 'monsters'
    weakness = []
    ailments = []
    name = " ".join(context.args) #convert arguments from user message into 1 single string
    result = search_db(category, name) #perfrom search on database

    #if database returns result
    if result != "invalid":
        all_weakness = result.get('weaknesses') #grab all weaknesses field into 1 list
        for w in all_weakness:
            if w.get('stars') > 2: #if weakness is more then 2 stars(effective)
                msg = w.get('element') + '(' + str(w.get('stars')) + ' stars)' #append to string for later processing
                weakness.append(msg)

        #get all ailments fields into 1 list
        all_ailments = result.get('ailments')
        for a in all_ailments:
            ailments.append(a.get('name')) #append all ailments name into a list

        #convert all list into string and declare all required fields
        monster_ailments = ", ".join(ailments)
        monster_weakness = ', '.join(weakness)
        description = result.get('description')
        monster_name = result.get('name')

        #declar messages to output
        monster_name_msg = "*Name*: {}".format(monster_name)
        description_msg = "*Description*: {}".format(description)
        weakness_msg = "*Weaknesses*: {}".format(monster_weakness)
        ailments_msg = "*Ailments:* {}".format(monster_ailments)

        #output message
        message = "{} \n{} \n{} \n{}".format(monster_name_msg,description_msg,weakness_msg,ailments_msg)
        update.message.reply_markdown(message, quote=True)
    elif name.startswith("@"):
        return
    else:
        update.message.reply_text("Unable to find this monster! Iceborne data not yet updated.")

def weapons(update, context):
    # if user input command with no arguments (weapons names) after the command
    if len(context.args) == 0:
        update.message.reply_text("Command syntax is /weapons <weapon name>")
        return
    # declaration
    category = 'weapons'
    slots = []
    mats = []
    elements = []
    name = " ".join(context.args)  # convert arguments from user message into 1 single string
    result = search_db(category, name)  # perform search on database

    if result != "invalid": #if result is valid
        weapon_name = result.get('name')
        weapon_type = result.get('type')
        weapon_rarity = result.get('rarity')
        weapon_attack = result.get('attack')
        weapon_display = weapon_attack.get('display')
        previous_weapon = ""

        crafting = result.get('crafting') #get all variables in crafting json
        craftable = crafting.get('craftable')
        next_weapon = []
        raw_asset_link = result.get('assets').get('image')
        asset_link = getassetlink(raw_asset_link) #output asset link in http readable format
        if craftable is False: #weapon can only be upgraded
            upgrade_mats = crafting.get('upgradeMaterials')
            for m in upgrade_mats: #get a list of all the mats required
                quantity = str(m.get('quantity'))
                mat_name = m.get('item').get('name')
                mat_msg = mat_name + ' x' + quantity + ' '
                mats.append(mat_msg)
        elif craftable is True: #weapon can be crafted
            crafting_mats = crafting.get('craftingMaterials')
            for m in crafting_mats: #get a list of all the mats required
                quantity = str(m.get('quantity'))
                mat_name = m.get('item').get('name')
                mat_msg = mat_name + ' x' + quantity
                mats.append(mat_msg)
        if crafting.get('previous') != 'null': #weapon has a prior weapon that it is upgraded from
            weapon_id = crafting.get('previous')
            previous_weapon = get_weapon_name(weapon_id) #get weapon id and output weapon name
        if (len(crafting.get('branches')) > 0): #has upgrade tree
            for weapon_id in crafting.get('branches'):
                next_weapon_name = get_weapon_name(weapon_id)
                next_weapon.append(next_weapon_name)
        if result.get('elements'): #if weapon has element
            for e in result.get('elements'):
                element_type = e.get('type')
                damage = e.get('damage')
                element_msg = "{}({})".format(element_type,damage)
                elements.append(element_msg)
        if (len(result.get('slots')) > 0 ): #weapon has decoration slots
            listofslots = result.get('slots')
            for i in range(0,len(listofslots)):
                slots.append(str(listofslots[i].get('rank')))

        elements_msg = ",".join(elements)
        mats_msg = ", ".join(mats)
        slots_msg = ", ".join(slots)
        next_weapon_msg = ", ".join(next_weapon)
        #message = "*Name:* {} \n *Type:* {} \n *Rarity:* {} \n <*Attack:* {} \n *Element:* {} \n *Mats:* {}".format(weapon_name,weapon_type,weapon_rarity,weapon_display,elements_msg,mats_msg)
        message = "<b>Type:</b> {} \n<b>Rarity:</b> {} \n<b>Slots:</b> {} \n<b>Previous:</b> {} \n<b>Next:</b> {} \n<b>Attack:</b> {} \n<b>Element:</b> {} \n<b>Materials:</b> {}".format(weapon_type,weapon_rarity,slots_msg,previous_weapon,next_weapon_msg, weapon_display,elements_msg,mats_msg)
        update.message.reply_html("<b>Name:</b> <a href='{}'>{}</a> \n{}".format(asset_link,weapon_name,message))
    elif name.startswith("@"):
        return
    else:
        update.message.reply_text("Unable to find this weapons! Iceborne data not yet updated.")

def items(update,context):
    # if user input command with no arguments (item names) after the command
    if len(context.args) == 0:
        update.message.reply_text("Command syntax is /items <item name>")
        return
    # declaration
    category = 'items'
    name = " ".join(context.args)  # convert arguments from user message into 1 single string
    result = search_db(category, name)  # perform search on database

    if result != 'invalid':
        name = result.get('name')
        description = result.get('description')
        rarity = result.get('rarity')
        carry = result.get('carryLimit')
        value = result.get('value')
        message = "*Name:* {} \n*Description:* {} \n*Rarity:* {} \n*Carry Limit:* {} \n*Value:* {}".format(name,description,rarity,carry,value)
        update.message.reply_markdown(message)
    else:
        update.message.reply_text("Unable to find item. Iceborne data not yet updated.")

def deco(update,context):
    # if user input command with no arguments (decoration names) after the command
    if len(context.args) == 0:
        update.message.reply_text("Command syntax is /deco <decoration name>")
        return
    skills = []
    category = 'decorations'
    name = " ".join(context.args)
    name = name.lower()
    if (name.find("jewel") >= 0) or (name.find("jewel+")>=0): #search terms have jewel in it.
        if name[-1].isdigit():
            name = name
        else:
            name = name + " 1"
    else: #search terms have no jewel in it
        name_list = name.split()
        if name_list[-1].isdigit():
            name_list.insert(-1,"Jewel")
        else:
            name_list.append("Jewel")
            name_list.append("1")
        name = " ".join(name_list)
    result = search_db(category,name)
    if result != 'invalid':
        deco_name = result.get('name')
        rarity = result.get('rarity')
        slots = result.get('slot')
        list_of_skills = result.get('skills')
        for s in list_of_skills:
            skill_name = s.get('skillName')
            skill_level = s.get('level')
            skill_message = "{}(lv. {})".format(skill_name,skill_level)
            skills.append(skill_message)
        skills_msg = ", ".join(skills)
        update.message.reply_markdown("*Decoration:* {} \n*Rarity:* {} \n*Slots:* {} \n*Skills:* {}".format(deco_name,rarity,slots,skills_msg))
    else:
        update.message.reply_text("Unable to find decoration. Iceborne data not yet updated.")

def skills(update,context):
    if len(context.args) == 0:
        update.message.reply_text("Command syntax is /items <item name>")
        return

    # declaration
    category = 'skills'
    name = " ".join(context.args)  # convert arguments from user message into 1 single string
    result = search_db(category, name)
    rank_details = []
    if result != 'invalid':
        skill_name = result.get('name')
        description = result.get('description')
        ranks = result.get('ranks')
        for r in ranks:
            level = r.get('level')
            description = r.get('description')
            rank_details.append("Level: {} \nDescription: {}".format(level, description))

        #convert to messsage
        rank_details_message = "\n".join(rank_details)
        message = "*Name:* {} \n*Description:* {} \n*Ranks:* \n{}".format(skill_name,description,rank_details_message)
        update.message.reply_markdown(message)
    else:
        update.message.reply_text("Unable to find decoration. Iceborne data not yet updated.")


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
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(CommandHandler("monsters", monsters))
    dp.add_handler(CommandHandler('weapons', weapons))
    dp.add_handler(CommandHandler('items', items))
    dp.add_handler(CommandHandler('deco', deco))
    dp.add_handler(CommandHandler('skills', skills))

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