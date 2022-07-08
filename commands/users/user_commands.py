from vkbottle.bot import Blueprint, Message
from vkbottle import CtxStorage
from data.keyboards import full_screen_menu, just_menu, more_info, back_to_start, person_keyboard, \
    input_phone, input_address, delivery_keyboard, full_screen_menu_adm, ask_keyboard, order_keyboard
from data.config import group_id, hight_admin
from misc.state_group import AddressState, Phone, Question, Order
from misc.address import Address
from bot import mysql_connect
from commands.admins.admin_commands import online_admins
import datetime
from commands.admins.admin_commands import get_admins
from misc.big_strings import ban_words, all_commands

bot = Blueprint("users chat command")
ctx = CtxStorage()


def check_ban_word(string):
    for word in ban_words:
        if word in string:
            return True
    return False


def check_all_commands(string):
    for word in all_commands:
        if string == word:
            return False
    return True


def get_banned(user_id: int):
    connection = mysql_connect()
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT banned FROM users WHERE id = {user_id}")
        banned = cursor.fetchone()
        connection.commit()
    if banned[0] == 0:
        return False
    else:
        return True


def check_str(text: str):
    temp = '0123456789.+/=*'
    for value in text:
        if value in temp:
            return False
    return True


@bot.on.private_message(text=['Начать', 'Ку', 'Привет' '/start'])
async def hello(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    connection = mysql_connect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT id FROM users WHERE id = {users_info[0].id}")
    if cursor.fetchone() is None:
        if users_info[0].id in hight_admin:
            name = f'{users_info[0].first_name} {users_info[0].last_name}'
            cursor.execute(f"INSERT INTO `users` (id, name, phone, address, num_orders, status, banned) "
                           f"VALUES ('{users_info[0].id}', '{name}', "
                           f"'Отсутствует', 'Отсутствует', 0, 'admin', 0);")
            connection.commit()
        else:
            name = f'{users_info[0].first_name} {users_info[0].last_name}'
            cursor.execute(f"INSERT INTO `users` (id, name, phone, address, num_orders, status, banned) "
                           f"VALUES ('{users_info[0].id}', '{name}', "
                           f"'Отсутствует', 'Отсутствует', 0, 'user', 0);")
            connection.commit()
    await message.answer("Здравствуйте, {}".format(users_info[0].first_name) + "!" +
                         "\nЗаполните Ваш адрес для будующих заказов или же нажмите \"Меню\" чтобы продолжить.",
                         keyboard=just_menu)


@bot.on.message(text=['Меню', '/menu', '👈🏻 Назад'])
async def hi_handler(message: Message):
    connection = mysql_connect()
    users_info = await bot.api.users.get(message.from_id)
    cursor = connection.cursor()
    cursor.execute(f"SELECT id FROM users WHERE id = {users_info[0].id}")
    if cursor.fetchone() is None:
        await message.answer("Вы еще не зарегистрированы! Пожалуйста, пропишите \"Начать\".", keyboard=back_to_start)
    else:
        if users_info[0].id in get_admins():
            await message.answer("Вы вызвали меню.", keyboard=full_screen_menu_adm)
        else:
            await message.answer("Вы вызвали меню.", keyboard=full_screen_menu)


@bot.on.message(text='О нас')
async def hi_handler(message: Message):
    await message.answer("Мы - лучшее кафе на рынке РФ.", keyboard=more_info)


@bot.on.message(text='Личный кабинет')
async def hi_handler(message: Message):
    await message.answer("Добро пожаловать в личный кабинет!", keyboard=person_keyboard)


@bot.on.message(text='Мой телефон')
async def search_phone(message: Message):
    connection = mysql_connect()
    with connection.cursor() as cursor:
        users_info = await bot.api.users.get(message.from_id)
        cursor.execute(f"SELECT phone FROM users WHERE id = {users_info[0].id}")
        phone = str(cursor.fetchone()[0])
        if phone == 'Отсутствует':
            await message.answer("Вы пока не заполнили свой телефон.", keyboard=input_phone)
        else:
            await message.answer("Ваш номер телефона: " + phone)


@bot.on.message(text='Мой адрес')
async def search_address(message: Message):
    connection = mysql_connect()
    with connection.cursor() as cursor:
        users_info = await bot.api.users.get(message.from_id)
        cursor.execute(f"SELECT address FROM users WHERE id = {users_info[0].id}")
        address = str(cursor.fetchone()[0])
        if address == 'Отсутствует':
            await message.answer("Вы еще не указали свой адрес.", keyboard=input_address)
        else:
            await message.answer("Ваш адрес: " + address)


@bot.on.message(text='Количество заказов')
async def search_orders(message: Message):
    connection = mysql_connect()
    with connection.cursor() as cursor:
        users_info = await bot.api.users.get(message.from_id)
        cursor.execute(f"SELECT num_orders FROM users WHERE id = {users_info[0].id}")
        orders = cursor.fetchone()[0]
        if orders == 0:
            await message.answer("Вы пока не сделали ни единого заказа у нас.")
        else:
            await message.answer("Количество Ваших заказов: " + str(orders))


@bot.on.private_message(text='Указать номер телефона')
async def handler(message: Message):
    await bot.state_dispenser.set(message.peer_id, Phone.NUMBER)
    return "Напишите мне свой номер телефона.\nПример: 89261231212"


@bot.on.private_message(state=Phone.NUMBER)
async def phone_funct(message: Message):
    ctx.set('phone', message.text)
    users_info = await bot.api.users.get(message.from_id)
    if len(ctx.get('phone')) == 11 and str(ctx.get('phone')).isdigit():
        phone = ctx.get('phone')
        if phone[0] == '8':
            new_phone = f'{phone[0]} ({phone[1]}{phone[2]}{phone[3]}) ' \
                        f'{phone[4]}{phone[5]}{phone[6]}-{phone[7]}{phone[8]}-{phone[9]}{phone[10]}'
        elif phone[0] == '7':
            new_phone = f'8 ({phone[1]}{phone[2]}{phone[3]}) ' \
                        f'{phone[4]}{phone[5]}{phone[6]}-{phone[7]}{phone[8]}-{phone[9]}{phone[10]}'
        await message.answer(f'Ваш номер телефона: ' + new_phone)
        connection = mysql_connect()
        with connection.cursor() as cursor:
            update_query = f"UPDATE `users` SET phone = '{new_phone}' WHERE id = '{users_info[0].id}'"
            cursor.execute(update_query)
            connection.commit()
        await bot.state_dispenser.set(message.peer_id, Phone.END)
        return "Номер телефона сохранен, если Вы допустили ошибку, введите команду еще раз."
    else:
        await bot.state_dispenser.set(message.peer_id, Phone.END)
        return "Это не похоже на номер телефона, воспользуйтесь командой еще раз."


@bot.on.private_message(text='Указать свой адрес')
async def city(message: Message):
    await bot.state_dispenser.set(message.peer_id, AddressState.CITY)
    return "Напишите мне свой город."


@bot.on.private_message(state=AddressState.CITY)
async def street(message: Message):
    if check_str(message.text):
        ctx.set('city', message.text)
        await bot.state_dispenser.set(message.peer_id, AddressState.STREET)
        return "Отлично, а теперь улицу."
    else:
        return "Вы ввели недопустимые символы, попробуйте еще раз."


@bot.on.private_message(state=AddressState.STREET)
async def home(message: Message):
    if check_str(message.text):
        ctx.set('street', message.text)
        await bot.state_dispenser.set(message.peer_id, AddressState.HOME)
        return "Введите номер дома (включая корпус или строение)."
    else:
        return "Вы ввели недопустимые символы, попробуйте еще раз."


@bot.on.private_message(state=AddressState.HOME)
async def flat(message: Message):
    ctx.set('home', message.text)
    await bot.state_dispenser.set(message.peer_id, AddressState.FLAT)
    return "Теперь мне нужен номер квартиры."


@bot.on.private_message(state=AddressState.FLAT)
async def doorphone(message: Message):
    ctx.set('flat', message.text)
    await bot.state_dispenser.set(message.peer_id, AddressState.DOORPHONE)
    return "А сейчас укажите код домофона (если кода нет, просто введите квартиру)."


@bot.on.private_message(state=AddressState.DOORPHONE)
async def floor(message: Message):
    ctx.set('doorphone', message.text)
    await bot.state_dispenser.set(message.peer_id, AddressState.FLOOR)
    return "Последний штрих, укажите свой этаж."


@bot.on.private_message(state=AddressState.FLOOR)
async def address_end(message: Message):
    if message.text.isdigit():
        users_info = await bot.api.users.get(message.from_id)
        ctx.set('floor', message.text)
        address: Address = Address(ctx.get('city'), ctx.get('street'), ctx.get('home'), ctx.get('flat'),
                                   ctx.get('doorphone'), ctx.get('floor'))
        await message.answer(f'Ваш адрес: ' + address.to_string())
        connection = mysql_connect()
        with connection.cursor() as cursor:
            update_query = f"UPDATE `users` SET address = '{address.to_string()}' WHERE id = '{users_info[0].id}'"
            cursor.execute(update_query)
            connection.commit()
        await bot.state_dispenser.set(message.peer_id, AddressState.END)
        return "Данные сохранены, если Вы допустили ошибку, перезапишите свой адрес еще раз."
    else:
        return "Вы ввели недопустимые символы, попробуйте еще раз."


@bot.on.private_message(text=['Связаться', 'Вопрос', 'Помощь'])
async def answer(message: Message):
    user = await bot.api.users.get(message.from_id)
    if not get_banned(user[0].id):
        if not online_admins:
            await message.answer('Ни одного менеджера нет в сети, возможно сегодня не рабочий день.')
            await bot.state_dispenser.set(message.peer_id, Question.END)
        else:
            connection = mysql_connect()
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM questions WHERE user_id = {user[0].id} AND completed = {0}")
                ques = cursor.fetchone()
                connection.commit()
            if ques is None:
                await message.answer("Пожалуйста, сформулируйте и напишите свой вопрос.\n"
                                     "Если вы нажали на кнопку случайно, напишите \"Отмена\"")
                await bot.state_dispenser.set(message.peer_id, Question.ASK)
            else:
                await message.answer("Вы уже обращались в службу поддержки, дождитесь ответа на предыдущее обращение.")
                await bot.state_dispenser.set(message.peer_id, Question.END)
    else:
        await message.answer("Вы заблокированы и не можете воспользоваться данной командой.")


@bot.on.private_message(state=Question.ASK)
async def ask(message: Message):
    user = await bot.api.users.get(message.from_id)
    text = message.text
    text_db = text.replace('\n', '; ')
    if text == "Отмена":
        await message.answer("Обращение отменено.")
    elif check_all_commands(text):
        if not text.isdigit():
            if check_ban_word(text):
                await message.answer("Не ругайтесь, сформулируйте проблему корректно.")
            else:
                connection = mysql_connect()
                with connection.cursor() as cursor:
                    last_num = 1
                    cursor.execute(f"SELECT ques_id FROM questions")
                    ids_ques = cursor.fetchall()
                    for row in ids_ques:
                        last_num = row[0] + 1

                    cursor.execute(f"INSERT INTO `questions` (ques_id, user_id, text, completed) "
                                   f"VALUES ('{last_num}', '{user[0].id}', '{text_db}', 0);")
                    connection.commit()

                await message.answer("В скором времени менеджер ответит на ваше обращение.")
                await bot.api.messages.send(peer_ids=online_admins,
                                            message=f'Пользователь [vk.com/id{user[0].id}|'
                                                    f'{user[0].first_name} {user[0].last_name}]'
                                                    f' хочет связаться с менеджером!\nВопрос:\n'
                                                    f'{text}\nОтветить: '
                                                    f'vk.com/gim{group_id}?sel={user[0].id}',
                                            keyboard=ask_keyboard(last_num, user[0].id), random_id=0)
                await bot.state_dispenser.set(message.peer_id, Question.END)
        else:
            await message.answer("Обращение не может состоять только из цифр!")
    else:
        await message.answer("Ваше обращение похоже на текст команды, мы отменим его.")
        await bot.state_dispenser.set(message.peer_id, Question.END)


@bot.on.message(text='Сделать заказ')
async def make_order(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    if not get_banned(users_info[0].id):
        connection = mysql_connect()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT order_id FROM orders WHERE user_id = {users_info[0].id} AND completed = {0}")
            order_info = cursor.fetchone()
            if order_info is None:
                cursor.execute(f"SELECT phone FROM users WHERE id = {users_info[0].id}")
                phone = str(cursor.fetchone()[0])
                if phone == 'Отсутствует':
                    await message.answer("Для заказа необходимо указать номер телефона.", keyboard=input_phone)
                    await bot.state_dispenser.set(message.peer_id, Order.END)
                else:
                    await bot.state_dispenser.set(message.peer_id, Order.DELIVERY)
                    await message.answer("Как Вы собираетесь забирать свой заказ?", keyboard=delivery_keyboard)
            else:
                await message.answer(f'Ваш заказ №{order_info[0]}  еще не обработан менеджером. Пожалуйста, подождите.')
    else:
        await message.answer("Вы заблокированы и не можете воспользоваться данной командой.")


@bot.on.private_message(state=Order.DELIVERY)
async def delivery_info(message: Message):
    msg = message.text
    connection = mysql_connect()
    users_info = await bot.api.users.get(message.from_id)
    if msg == "Доставка":
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT address FROM users WHERE id = {users_info[0].id}")
            address = str(cursor.fetchone()[0])
            if address == 'Отсутствует':
                await message.answer("Для заказа необходимо заполнить адрес доставки.", keyboard=input_address)
                await bot.state_dispenser.set(message.peer_id, Order.END)
            else:
                await bot.state_dispenser.set(message.peer_id, Order.INFO_DEL)
                return "Пожалуйста, напишите свой заказ в формате:\n\n1 пицца\n2 колы"
    elif msg == "Самовывоз":
        await bot.state_dispenser.set(message.peer_id, Order.INFO_SAM)
        return "Пожалуйста, напишите мне свой заказ, я передам его менеджеру."


@bot.on.private_message(state=Order.INFO_DEL)
async def order_info_del(message: Message):
    if not message.text.isdigit():
        if not check_ban_word(message.text):
            if check_all_commands(message.text):
                order = message.text.replace(' \n', '|')
                now_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
                users_info = await bot.api.users.get(message.from_id)
                connection = mysql_connect()
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT address FROM users WHERE id = {users_info[0].id}")
                    address = str(cursor.fetchone()[0])
                    cursor.execute(f"SELECT phone FROM users WHERE id = {users_info[0].id}")
                    phone = str(cursor.fetchone()[0])
                    connection.commit()
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT order_id FROM orders")
                    ids_orders = cursor.fetchall()
                    last_num = 1
                    for row in ids_orders:
                        last_num = row[0] + 1
                    name = users_info[0].first_name + ' ' + users_info[0].last_name
                    cursor.execute(f"INSERT INTO `orders` (order_id, user_id, name, "
                                   f", phone, date, order_list, completed) "
                                   f"VALUES ('{last_num}', '{users_info[0].id}', '{name}',"
                                   f"'{address}', '{phone}', '{now_date}', '{order}', '{0}');")
                    connection.commit()
                    await bot.state_dispenser.set(message.peer_id, Order.END)
                order_str = f"Поступил новый заказ!\n\n№{last_num}\n{now_date}\nОт: {name}\n{address}\n" \
                            f"Тел: {phone}\n{'#' * 20}\n{message.text}\n{'#' * 20}\n\nПерейти к диалогу: " \
                            f"vk.com/gim{group_id}?sel={users_info[0].id}"
                if not online_admins:
                    await bot.api.messages.send(peer_id=hight_admin, message=order_str,
                                                keyboard=order_keyboard(last_num), random_id=0)
                    await bot.api.messages.send(peer_id=hight_admin,
                                                message='❗ Вам пришло это уведомление, '
                                                        'потому что ни одного менеджера нет в сети.',
                                                random_id=0)
                else:
                    await bot.api.messages.send(peer_id=hight_admin, message=order_str,
                                                keyboard=order_keyboard(last_num), random_id=0)
                await message.answer(f"Ваш заказ был оформлен под №{last_num}\nДата: {now_date}\n"
                                     f"Адрес доставки: {address}\n"
                                     f"Тел: {phone}\n{'#' * 20}\n{message.text}\n{'#' * 20}\n\n"
                                     f"В скором времени с Вами свяжется наш менеджер для уточнения информации.")
            else:
                await message.answer("Ваш заказ похож на одну из команд, попробуйте написать заказ еще раз.")
        else:
            await message.answer("Сформулируйте свой заказ адекватно!")
    else:
        await message.answer("Заказ не может состоять только из цифр!")


@bot.on.private_message(state=Order.INFO_SAM)
async def order_info_sam(message: Message):
    if not message.text.isdigit():
        if not check_ban_word(message.text):
            if check_all_commands(message.text):
                order = message.text.replace(' \n', '|')
                now_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
                users_info = await bot.api.users.get(message.from_id)
                connection = mysql_connect()
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT phone FROM users WHERE id = {users_info[0].id}")
                    phone = str(cursor.fetchone()[0])
                    connection.commit()
                with connection.cursor() as cursor:
                    last_num = 1
                    cursor.execute(f"SELECT order_id FROM orders")
                    ids_orders = cursor.fetchall()
                    name = users_info[0].first_name + ' ' + users_info[0].last_name
                    for row in ids_orders:
                        last_num = row[0] + 1
                    cursor.execute(
                        f"INSERT INTO `orders` (order_id, user_id, name, address, phone, date, order_list, completed) "
                        f"VALUES ('{last_num}', '{users_info[0].id}', '{name}',"
                        f"'Самовывоз', '{phone}', '{now_date}', '{order}', '{0}');")
                    connection.commit()
                    await bot.state_dispenser.set(message.peer_id, Order.END)
                order_str = f"Поступил новый заказ!\n\n№{last_num}\n{now_date}\nОт: {name}\nСАМОВЫВОЗ\n" \
                            f"Тел: {phone}\n{'#' * 20}\n{message.text}\n{'#' * 20}\n\nПерейти к диалогу: " \
                            f"vk.com/gim{group_id}?sel={users_info[0].id}"
                if not online_admins:
                    await bot.api.messages.send(peer_id=hight_admin, message=order_str,
                                                keyboard=order_keyboard(last_num), random_id=0)
                    await bot.api.messages.send(peer_id=hight_admin,
                                                message='❗ Вам пришло это уведомление, '
                                                        'потому что ни одного менеджера нет в сети.',
                                                random_id=0)
                else:
                    await bot.api.messages.send(peer_id=hight_admin, message=order_str,
                                                keyboard=order_keyboard(last_num), random_id=0)
                await message.answer(f"Ваш заказ был оформлен под №{last_num}\nДата: {now_date}\n"
                                     f"Тип доставки: Самовывоз\n"
                                     f"Тел: {phone}\n{'#' * 20}\n{message.text}\n{'#' * 20}\n\n"
                                     f"В скором времени с Вами свяжется наш менеджер для уточнения информации.")
            else:
                await message.answer("Ваш заказ похож на одну из команд, попробуйте написать заказ еще раз.")
        else:
            await message.answer("Сформулируйте свой заказ адекватно!")
    else:
        await message.answer("Заказ не может состоять только из цифр!")
