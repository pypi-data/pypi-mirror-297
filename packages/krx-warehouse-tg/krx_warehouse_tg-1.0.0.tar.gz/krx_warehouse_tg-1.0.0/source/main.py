import datetime
import re

import telebot

from buttons import *
from database import *

bot = telebot.TeleBot(token=API_TOKEN)

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    tID = call.message.chat.id
    data = call.data
    if data == 'btn_register':
        bot.edit_message_reply_markup(chat_id=tID,
                                      message_id=call.message.id,
                                      reply_markup=None)
        msg = bot.send_message(chat_id=tID,
                               text="*Enter first and last name with a space*"
                                    "\nExample: John Smith",
                               parse_mode="Markdown")
        bot.register_next_step_handler(msg, inputName)
    elif data == 'btn_boxes_help':
        bot.edit_message_reply_markup(chat_id=tID,
                                      message_id=call.message.id,
                                      reply_markup=None)
        bot.send_message(chat_id=tID,
                         text="Available box sizes:\n"
                              "MINI: 23*17*13 см - items (T-shirt, bag, belt, socks)\n"
                              "SMALL: 36*26*14 см - a pair of shoes\n"
                              "LARGE: 40*29*16 см - a pair of shoes in a box + a few clothes\n"
                              "EXTRA LARGE: 45*34*18 см - two pair of shoes in a box\n"
                              "Y-08: 37*29*28 СМ - two pair of shoes in a box + a few clothes\n"
                              "Y-01: 38*48*30 см - four pair of shoes in a box + a few clothes",
                         reply_markup=main_menu)
    elif data == 'add_new_address':
        bot.edit_message_reply_markup(chat_id=tID,
                                      message_id=call.message.id,
                                      reply_markup=None)
        markup = types.ReplyKeyboardMarkup(row_width=1,
                                           resize_keyboard=True,
                                           one_time_keyboard=True)
        markup.add(types.KeyboardButton(text="Back"))
        msg = bot.send_message(chat_id=tID,
                               text="",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, inputAddress)
    elif data == 'delete_address':
        bot.delete_message(message_id=call.message.id,
                           chat_id=tID)
        addresses = get_addresses(tID)
        markup = types.ReplyKeyboardMarkup(row_width=1,
                                           resize_keyboard=True,
                                           one_time_keyboard=True)
        for index, address in enumerate(addresses):
            markup.add(types.KeyboardButton(text=f"{address[0]}"))
        markup.add(types.KeyboardButton(text="Back"))
        msg = bot.send_message(chat_id=tID,
                               text=f"",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, continue_delete_address)
    elif "pbox" in data:
        picked_size = data.split("_")[-1]
        temp_data[tID] = {}
        temp_data[tID]["pbox"] = picked_size.upper()
        msg = bot.send_message(chat_id=tID,
                               text=f"",
                               parse_mode="Markdown",
                               reply_markup=types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                                                      resize_keyboard=True).add(
                                   types.KeyboardButton(text="Back")))
        bot.register_next_step_handler(msg, load_weight)
    elif data == 'add_new_goods':
        bot.edit_message_reply_markup(chat_id=tID,
                                      message_id=call.message.id,
                                      reply_markup=None)
        msg = bot.send_message(chat_id=tID,
                               text="")
        bot.register_next_step_handler(msg, add_goods_name)
    elif data == 'check_goods':
        bot.edit_message_reply_markup(chat_id=tID,
                                      message_id=call.message.id,
                                      reply_markup=None)
        markup = types.ReplyKeyboardMarkup(row_width=1,
                                           resize_keyboard=True,
                                           one_time_keyboard=True)
        markup.add(types.KeyboardButton(text="Back"))
        msg = bot.send_message(chat_id=tID,
                               text="",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, check_goods_id)
    elif data == 'change_name':
        bot.edit_message_reply_markup(chat_id=tID,
                                      message_id=call.message.id,
                                      reply_markup=None)
        markup = types.ReplyKeyboardMarkup(row_width=1,
                                           resize_keyboard=True,
                                           one_time_keyboard=True)
        markup.add(types.KeyboardButton(text="Back"))
        msg = bot.send_message(chat_id=tID,
                               text="*",
                               reply_markup=markup,
                               parse_mode="Markdown")
        bot.register_next_step_handler(msg, new_name)
    elif data == 'change_email':
        bot.edit_message_reply_markup(chat_id=tID,
                                      message_id=call.message.id,
                                      reply_markup=None)
        markup = types.ReplyKeyboardMarkup(row_width=1,
                                           resize_keyboard=True,
                                           one_time_keyboard=True)
        markup.add(types.KeyboardButton(text="Back"))
        msg = bot.send_message(chat_id=tID,
                               text="",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, new_email)
    elif data == 'delete_profile':
        bot.edit_message_reply_markup(chat_id=tID,
                                      message_id=call.message.id,
                                      reply_markup=None)
        markup = types.ReplyKeyboardMarkup(row_width=1,
                                           resize_keyboard=True,
                                           one_time_keyboard=True)
        markup.add(types.KeyboardButton(text="Back"))
        msg = bot.send_message(chat_id=tID,
                               text="!*",
                               parse_mode="Markdown",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, delete_profile)
    elif data == 'check_orders':
        bot.edit_message_reply_markup(chat_id=tID,
                                      message_id=call.message.id,
                                      reply_markup=None)
        markup = types.ReplyKeyboardMarkup(row_width=1,
                                           resize_keyboard=True,
                                           one_time_keyboard=True)
        markup.add(types.KeyboardButton(text="Back"))
        msg = bot.send_message(chat_id=tID,
                               text="",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, check_order_id)

@bot.message_handler(commands=['start'])
def command_start(message):
    tID = message.chat.id
    if tID == 1:
        bot.send_message(chat_id=tID,
                         text="",
                         reply_markup=admin_menu)
    else:
        if is_user(tID):
            user_info = get_user(tID)
            bot.send_message(chat_id=tID,
                             text=f"*, {user_info[2]}!*",
                             reply_markup=main_menu,
                             parse_mode="Markdown")
        else:
            markup = telebot.types.InlineKeyboardMarkup(row_width=1)
            markup.add(telebot.types.InlineKeyboardButton(text="", callback_data="btn_register"))
            bot.send_message(chat_id=tID,
                             text="",
                             reply_markup=markup)

def new_name(message):
    data = message.text
    tID = message.chat.id
    if data == "Back":
        bot.send_message(chat_id=tID,
                         text="Main menu",
                         reply_markup=main_menu)
    else:
        data = data.strip().split()
        if len(data) == 2:
            temp_data[tID] = {}
            temp_data[tID]['firstname'] = data[0]
            temp_data[tID]['lastname'] = data[1]
            print(temp_data[tID])
            if change_name(firstname=temp_data[tID]['firstname'],
                           lastname=temp_data[tID]['lastname'],
                           tID=tID):
                bot.send_message(chat_id=tID,
                                 text=f"*{data[0]}!*",
                                 parse_mode="Markdown",
                                 reply_markup=main_menu)
        else:
            msg = bot.send_message(chat_id=tID,
                                   text="**",
                                   parse_mode="Markdown")
            bot.register_next_step_handler(msg, new_name)

def new_email(message):
    tID = message.chat.id
    text = message.text
    if text == "Back":
        bot.send_message(chat_id=tID,
                         text="Main menu",
                         reply_markup=main_menu)
    else:
        if (re.match(email_pattern, text)):
            change_email(text, tID)
            bot.send_message(chat_id=tID,
                             text="*!*",
                             parse_mode="Markdown",
                             reply_markup=main_menu)
        else:
            msg = bot.send_message(chat_id=tID,
                                   text=f"")
            bot.register_next_step_handler(msg, new_email)

def delete_profile(message):
    tID = message.chat.id
    if message.text == "Back":
        bot.send_message(chat_id=tID,
                         text="Main menu",
                         reply_markup=main_menu)
    elif message.text == "":
        delete_user(tID)
        msg = bot.send_message(chat_id=tID,
                               text="")
        command_start(msg)

def check_order_id(message):
    tID = message.chat.id
    id = message.text
    if message.text == "Back":
        bot.send_message(chat_id=tID,
                         text="Main menu",
                         reply_markup=main_menu)
    elif (id.isdigit()):
        status = get_status(tID, id)
        if status:
            if (status != ""):
                bot.send_message(chat_id=tID,
                                 text=f" {id}: {get_status(tID, id)}",
                                 reply_markup=main_menu)
            else:
                bot.send_message(chat_id=tID,
                                 text="",
                                 parse_mode="Markdown",
                                 reply_markup=main_menu)
        else:
            msg = bot.send_message(chat_id=tID,
                                   text="")
            bot.register_next_step_handler(msg, check_order_id)
    else:
        msg = bot.send_message(chat_id=tID,
                               text="")
        bot.register_next_step_handler(msg, check_order_id)

def check_goods_id(message):
    tID = message.chat.id
    id = message.text
    if message.text == "Back":
        bot.send_message(chat_id=tID,
                         text="Main menu",
                         reply_markup=main_menu)
    elif (id.isdigit()):
        status = get_status(tID, id)
        if status:
            if (status == ""):
                bot.send_message(chat_id=tID,
                                 text=f" {id}: {get_status(tID, id)}",
                                 reply_markup=main_menu)
            else:
                bot.send_message(chat_id=tID,
                                 text="",
                                 parse_mode="Markdown",
                                 reply_markup=main_menu)
        else:
            msg = bot.send_message(chat_id=tID,
                                   text="")
            bot.register_next_step_handler(msg, check_goods_id)
    else:
        msg = bot.send_message(chat_id=tID,
                               text="")
        bot.register_next_step_handler(msg, check_goods_id)

def continue_delete_address(message):
    tID = message.chat.id
    if message.text == "Back":
        bot.send_message(chat_id=tID,
                         text=f'Main menu',
                         reply_markup=main_menu)
    else:
        if delete_address(message.text, message.chat.id):
            bot.send_message(chat_id=tID,
                             text=f' *"{message.text}" !*',
                             reply_markup=main_menu,
                             parse_mode="Markdown")
        else:
            bot.send_message(chat_id=tID,
                             text=f'**',
                             reply_markup=main_menu,
                             parse_mode="Markdown")

def send_addresses(tID):
    addresses = get_addresses(tID)
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    if addresses:
        response = "**\n\n" + "\n".join(
            [f"{index + 1}. {address[0]}" for index, address in enumerate(addresses)])
        markup.row(telebot.types.InlineKeyboardButton(text="", callback_data="add_new_address"),
                   telebot.types.InlineKeyboardButton(text="", callback_data="delete_address"))
    else:
        response = ""
        markup.add(telebot.types.InlineKeyboardButton(text="", callback_data="add_new_address"))
    bot.send_message(chat_id=tID,
                     text=response,
                     reply_markup=markup,
                     parse_mode="Markdown")

def inputName(message):
    tID = message.chat.id
    data = message.text.strip().split()
    if len(data) == 2:
        temp_data[tID] = {}
        temp_data[tID]['firstname'] = data[0]
        temp_data[tID]['lastname'] = data[1]
        msg = bot.send_message(chat_id=tID,
                               text=f"*",
                               parse_mode="Markdown")
        bot.register_next_step_handler(msg, inputEmail)
    else:
        msg = bot.send_message(chat_id=tID,
                               text="**",
                               parse_mode="Markdown")
        bot.register_next_step_handler(msg, inputName)

def inputEmail(message):
    tID = message.chat.id
    data = message.text.strip()
    if re.match(email_pattern, data):
        if reg_user(tID=tID,
                    lastname=temp_data[tID]['lastname'],
                    firstname=temp_data[tID]['firstname'],
                    email=data):
            bot.send_message(chat_id=tID,
                             text="*!*",
                             parse_mode="Markdown",
                             reply_markup=main_menu)
        else:
            markup = telebot.types.InlineKeyboardMarkup(row_width=1)
            markup.add(telebot.types.InlineKeyboardButton(text="", callback_data="btn_register"))
            bot.send_message(chat_id=tID,
                             text="**",
                             parse_mode="Markdown",
                             reply_markup=markup)
    else:
        msg = bot.send_message(chat_id=tID,
                               text=f"**",
                               parse_mode="Markdown")
        bot.register_next_step_handler(msg, inputEmail)

def inputAddress(message):
    tID = message.chat.id
    address = message.text
    if (address == "Back"):
        bot.send_message(chat_id=tID,
                         text=f'Main menu',
                         reply_markup=main_menu)
    else:
        if re.match(address_pattern, address):
            reg_address(tID, address)
            bot.send_message(chat_id=tID,
                             text="*!*",
                             parse_mode="Markdown",
                             reply_markup=main_menu)
        else:
            msg = bot.send_message(chat_id=tID,
                                   text="")
            bot.register_next_step_handler(msg, inputAddress)

def load_weight(message):
    tID = message.chat.id
    if message.text == "Back":
        bot.send_message(chat_id=tID,
                         text="Main menu",
                         reply_markup=main_menu)
    else:
        try:
            cur_weight = float(message.text.strip().replace(",", "."))
            calcShippingPrice(tID=tID,
                              weight=cur_weight)
        except Exception:
            msg = bot.send_message(chat_id=tID,
                                   text="",
                                   reply_markup=types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                                                          resize_keyboard=True).add(
                                       types.KeyboardButton(text="Back")))
            bot.register_next_step_handler(msg, load_weight)

def calcShippingPrice(tID, weight):
    vol_price = round(500 * boxes_measurements[temp_data[tID]["pbox"]], 2)
    china = round(700 * float(weight), 2)
    rus = round(510 * float(weight), 2)
    allsum = round(vol_price + china + rus, 2)
    bot.send_message(chat_id=tID,
                     text=f": {allsum} \n"
                          f" {vol_price} \n"
                          f": {china} \n"
                          f": {rus} ",
                     reply_markup=main_menu)

def add_goods_name(message):
    name = message.text
    tID = message.chat.id
    msg = bot.send_message(chat_id=tID,
                           text="")
    bot.register_next_step_handler(msg, add_price, name)

def add_price(message, name):
    price = message.text
    tID = message.chat.id
    try:
        float_price = float(price.replace(',', '.'))
        id = int(f"{tID}{datetime.datetime.now().year}{datetime.datetime.now().hour}{datetime.datetime.now().day}")
        create_goods(id, tID, name, float_price)
        bot.send_message(message.chat.id, f": {id}",
                         reply_markup=main_menu)
    except ValueError:
        msg = bot.send_message(message.chat.id, "")
        bot.register_next_step_handler(msg, add_price, name)

@bot.message_handler(content_types=['text'])
def buttons_handler(message):
    text = message.text
    tID = message.chat.id
    if text == btn_help.text:
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        markup.add(telebot.types.InlineKeyboardButton(text="", callback_data="btn_boxes_help"))
        bot.send_message(tID,
                         text="",
                         reply_markup=markup)
    elif text == btn_calculator.text:
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        for a in range(0, len(box_names) - 1, 2):
            markup.row(types.InlineKeyboardButton(text=f"{box_names[a].upper()}",
                                                  callback_data=f"pbox_{box_names[a]}"),
                       types.InlineKeyboardButton(text=f"{box_names[a + 1].upper()}",
                                                  callback_data=f"pbox_{box_names[a + 1]}"))
        markup.add(telebot.types.InlineKeyboardButton(text=" размеры", callback_data="btn_boxes_help"))
        bot.send_message(tID,
                         text="*",
                         reply_markup=markup,
                         parse_mode="Markdown")
    elif text == btn_addresses.text:
        send_addresses(tID)
    elif text == btn_goods.text:
        addresses = get_addresses(tID)
        goods = get_all_goods(tID)
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        resp1 = f"Here you can add items that should be arriving at our warehouse soon. As soon as we receive them, you can arrange delivery.\n\n{goods}"

        if addresses:
            markup.add(telebot.types.InlineKeyboardButton(text="Add new product", callback_data="add_new_goods"),
                       telebot.types.InlineKeyboardButton(text="Check order status", callback_data="check_goods"))
            response = "What you want to do?"
        else:
            markup.add(telebot.types.InlineKeyboardButton(text="Add new address", callback_data="add_new_address"))
            response = "To create a product, you need to add at least one address"
        bot.send_message(tID, resp1 + response,
                         reply_markup=markup)
    elif text == btn_profile.text:
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        markup.add(telebot.types.InlineKeyboardButton(text="Change name", callback_data="change_name"),
                   telebot.types.InlineKeyboardButton(text="Change email", callback_data="change_email"),
                   telebot.types.InlineKeyboardButton(text="Delete profile", callback_data="delete_profile"))
        bot.send_message(tID,
                         text=f"*Account data*\n\n"
                              f"Name: *{get_user(tID)[1]} {get_user(tID)[2]}*\n"
                              f"E-mail: *{get_user(tID)[3]}*\n"
                              f"Profile ID: *{get_user(tID)[0]}*",
                         parse_mode="Markdown",
                         reply_markup=markup)
    elif text == btn_deliveries.text:
        orders = get_all_orders(tID)
        resp = f"Here you can view your items that have already arrived at the warehouse or we have shipped them to you\n\n" \
               f"{orders}"
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        markup.add(telebot.types.InlineKeyboardButton(text="Check order status", callback_data="check_orders"))
        bot.send_message(tID,
                         text=resp,
                         reply_markup=markup)

bot.infinity_polling(skip_pending=True)
