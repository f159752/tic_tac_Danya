import telebot, config, skynet, chat
from telebot import types
# from skynet import field, side, cpt, counter, level, curr
bot = telebot.TeleBot(config.TOKEN)
x = u'\U0000274C'
o = u'\U00002B55'
e = u'\U00002B1C'
# user = chat.User("", skynet.field, skynet.cpt, skynet.side, skynet.level, skynet.counter)

IDs={}
fields = {}
cpts = {}
sides = {}
counters = {}
levels = {}

# field = [['-', '-', '-'],
#          ['-', '-', '-'],
#          ['-', '-', '-']]
# cpt = ""
# curr = ""
# side = ""
# level = 0
# counter = 0

def clear(id):
    field = [['-', '-', '-'],
             ['-', '-', '-'],
             ['-', '-', '-']]
    cpt = ""
    curr = ""
    side = ""
    level = 0
    counter = 0
    IDs[id] = id
    fields[id] = field
    cpts[id] = cpt
    sides[id] = side
    counters[id] = counter
    levels[id] = level

def draw_field(f):
    # Отрисовка пользователю
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(f)):
        btns = []
        for j in range(len(f[i])):
            index = str(i) + ";" + str(j)
            if (f[i][j] == '-'):
                callback_button = types.InlineKeyboardButton(text=e, callback_data="i" + index)
            elif (f[i][j] == 'x'):
                callback_button = types.InlineKeyboardButton(text=x, callback_data="i" + index)
            else:
                callback_button = types.InlineKeyboardButton(text=o, callback_data="i" + index)
            btns.append(callback_button)
        keyboard.add(btns[0], btns[1], btns[2])
    return keyboard
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Бібіп, я Telegram бот")

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "/start - Бібіб, /help - Хабах")
    print(message.text)

@bot.message_handler(commands=["new_game"])
def help(message):
    clear(message.chat.id)
    #
    # skynet.field = [['-', '-', '-'],
    #          ['-', '-', '-'],
    #          ['-', '-', '-']]
    # skynet.cpt = ""
    # skynet.side = ""
    # skynet.level = 0
    # skynet.counter = 0
    keyboard = types.InlineKeyboardMarkup()
    clb1 = types.InlineKeyboardButton(text="Junior", callback_data="l1")
    clb2 = types.InlineKeyboardButton(text="Middle", callback_data="l2")
    clb3 = types.InlineKeyboardButton(text="Senior", callback_data="l3")
    keyboard.add(clb1, clb2, clb3)
    bot.send_message(IDs[message.chat.id], text="Choose difficulty level:", reply_markup=keyboard)
    # print(message.text)

@bot.message_handler(commands=["list"])
def help(message):
    bot.send_message(message.chat.id, IDs)
    print(message.text)
    print(IDs)

@bot.message_handler(content_types=["text"])
def any_msg(message):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(3):
        btns = []
        for j in range(3):
            index = str(i) + ";" + str(j)
            callback_button = types.InlineKeyboardButton(text=e, callback_data="i" + index)
            btns.append(callback_button)
        keyboard.add(btns[0], btns[1], btns[2])
    # keyboard.add(callback_button)
    bot.send_message(message.chat.id, text="Bukovka", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if (call.data[0] == "l"):#Модификатор уровня сложности
            levels[call.message.chat.id] = int(call.data[1:])
            keyboard = types.InlineKeyboardMarkup()
            clb1 = types.InlineKeyboardButton(text=x, callback_data="sx")
            clb2 = types.InlineKeyboardButton(text=o, callback_data="s0")
            keyboard.add(clb1, clb2)
            bot.edit_message_text(text="Choose your side", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
        elif (call.data[0] == "s"):#Первоначальное создание поля
            sides[call.message.chat.id] = call.data[1:]
            if (sides[call.message.chat.id] == "x"):
                cpts[call.message.chat.id] = "0"
            elif (sides[call.message.chat.id] == "0"):
                cpts[call.message.chat.id] = "x"
                # Now AI move
                if (levels[call.message.chat.id] == 1):
                    skynet.jun(fields[call.message.chat.id], cpts[call.message.chat.id])
                elif (levels[call.message.chat.id] == 2):
                    lucky = skynet.random.choice([1, 2])
                    if (lucky == 1):
                        skynet.jun(fields[call.message.chat.id], cpts[call.message.chat.id])
                    else:
                        skynet.sen(fields[call.message.chat.id], cpts[call.message.chat.id],
                                   sides[call.message.chat.id], counters[call.message.chat.id])
                elif (levels[call.message.chat.id] == 3):
                    skynet.sen(fields[call.message.chat.id], cpts[call.message.chat.id], sides[call.message.chat.id],
                               counters[call.message.chat.id])
                counters[call.message.chat.id] += 1
            # Отрисовка пользователю
            keyboard = draw_field(fields[call.message.chat.id])
            bot.edit_message_text(text="You will play as " + sides[call.message.chat.id] + ", get ready!",chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=keyboard)
        elif (call.data[0] == "i"):
            crds = str.split(call.data[1:], ';')
            if (fields[call.message.chat.id][int(crds[0])][int(crds[1])] != '-'):
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Нельзя ставить туда, где уже поставлено!")
                print(call.data)
            else:
                # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=x)
                # Human move
                fields[call.message.chat.id][int(crds[0])][int(crds[1])] = sides[call.message.chat.id]
                counters[call.message.chat.id] += 1
                res = skynet.is_win(fields[call.message.chat.id])
                if (res[0] == True):
                    print(counters[call.message.chat.id])
                    keyboard = types.InlineKeyboardMarkup()
                    clb1 = types.InlineKeyboardButton(text="Hell yeah!", callback_data="ny")
                    clb2 = types.InlineKeyboardButton(text="No, I`m scared", callback_data="nn")
                    keyboard.add(clb1, clb2)
                    text = ""
                    for i in range(len(fields[call.message.chat.id])):
                        for j in range(len(fields[call.message.chat.id][i])):
                            if (fields[call.message.chat.id][i][j] == '-'):
                                text += e + " "
                            elif (fields[call.message.chat.id][i][j] == 'x'):
                                text += x + " "
                            else:
                                text += o + " "
                        text += "\n"
                    text += "You are crazy ass muthafucka! Do you want a rematch?"
                    bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                                          message_id=call.message.message_id, reply_markup=keyboard)
                elif (counters[call.message.chat.id] == 9):
                    print(counters[call.message.chat.id])
                    keyboard = types.InlineKeyboardMarkup()
                    clb1 = types.InlineKeyboardButton(text="Hell yeah!", callback_data="ny")
                    clb2 = types.InlineKeyboardButton(text="No, I`m scared", callback_data="nn")
                    keyboard.add(clb1, clb2)
                    text = ""
                    for i in range (len(fields[call.message.chat.id])):
                        for j in range(len(fields[call.message.chat.id][i])):
                            if (fields[call.message.chat.id][i][j] == '-'):
                                text += e + " "
                            elif (fields[call.message.chat.id][i][j] == 'x'):
                                text += x + " "
                            else:
                                text += o + " "
                        text += "\n"
                    text += "It`s draw! Do you want a rematch?"
                    bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                                          message_id=call.message.message_id, reply_markup=keyboard)
                else:
                    # Now AI move
                    if (levels[call.message.chat.id] == 1):
                        skynet.jun(fields[call.message.chat.id], cpts[call.message.chat.id])
                    elif (levels[call.message.chat.id] == 2):
                        lucky = skynet.random.choice([1, 2])
                        if (lucky == 1):
                            skynet.jun(fields[call.message.chat.id], cpts[call.message.chat.id])
                        else:
                            skynet.sen(fields[call.message.chat.id], cpts[call.message.chat.id], sides[call.message.chat.id], counters[call.message.chat.id])
                    elif (levels[call.message.chat.id] == 3):
                        skynet.sen(fields[call.message.chat.id], cpts[call.message.chat.id],
                                   sides[call.message.chat.id], counters[call.message.chat.id])
                    counters[call.message.chat.id] += 1
                    res = skynet.is_win(fields[call.message.chat.id])
                    if (res[0] == True):
                        keyboard = types.InlineKeyboardMarkup()
                        clb1 = types.InlineKeyboardButton(text="Hell yeah!", callback_data="ny")
                        clb2 = types.InlineKeyboardButton(text="No, I`m scared", callback_data="nn")
                        keyboard.add(clb1, clb2)
                        text = ""
                        for i in range(len(fields[call.message.chat.id])):
                            for j in range(len(fields[call.message.chat.id][i])):
                                if (fields[call.message.chat.id][i][j] == '-'):
                                    text += e + " "
                                elif (fields[call.message.chat.id][i][j] == 'x'):
                                    text += x + " "
                                else:
                                    text += o + " "
                            text += "\n"
                        text += "Oh, what`s happen? You lose! Do you want a rematch?"
                        bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                                              message_id=call.message.message_id, reply_markup=keyboard)
                    elif (counters[call.message.chat.id] == 9):
                        keyboard = types.InlineKeyboardMarkup()
                        clb1 = types.InlineKeyboardButton(text="Hell yeah!", callback_data="ny")
                        clb2 = types.InlineKeyboardButton(text="No, I`m scared", callback_data="nn")
                        keyboard.add(clb1, clb2)
                        text = ""
                        for i in range(len(fields[call.message.chat.id])):
                            for j in range(len(fields[call.message.chat.id][i])):
                                if (fields[call.message.chat.id][i][j] == '-'):
                                    text += e + " "
                                elif (fields[call.message.chat.id][i][j] == 'x'):
                                    text += x + " "
                                else:
                                    text += o + " "
                            text += "\n"
                        text += "It`s draw! Do you want a rematch?"
                        bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                                              message_id=call.message.message_id, reply_markup=keyboard)
                    else:
                        # Отрисовка пользователю
                        keyboard = draw_field(fields[call.message.chat.id])
                        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                      message_id=call.message.message_id, reply_markup=keyboard)
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=call.data)
                        print(call.data)
        elif (call.data[0] == "n"):
            answer = call.data[1:]
            if (answer == "y"):
                keyboard = types.InlineKeyboardMarkup()
                clb1 = types.InlineKeyboardButton(text="Junior", callback_data="l1")
                clb2 = types.InlineKeyboardButton(text="Middle", callback_data="l2")
                clb3 = types.InlineKeyboardButton(text="Senior", callback_data="l3")
                keyboard.add(clb1, clb2, clb3)
                clear(call.message.chat.id)
                bot.edit_message_text(text="Choose difficulty level:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
            else:
                bot.edit_message_text(text="Chao-cacao", chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)

if __name__ == "__main__":
    bot.polling()