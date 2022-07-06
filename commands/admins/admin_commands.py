from vkbottle.bot import Blueprint, Message
from bot import mysql_connect, group_id
from vkbottle import PhotoMessageUploader
from data.keyboards import admin_keyboard, full_screen_menu

bot = Blueprint("Admin")
online_admins = []


def get_admins():
    connection = mysql_connect()
    list_admins = []
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id FROM users WHERE status = 'admin'")
        admins = cursor.fetchall()
        for row in admins:
            list_admins.append(row[0])
        connection.commit()
    return list_admins


@bot.on.message(text="Начать работу")
async def hi_admin(message: Message):
    admin_list = get_admins()
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in admin_list:
        if users_info[0].id in online_admins:
            await message.answer('Вы уже начали рабочий день.')
        else:
            online_admins.append(users_info[0].id)
            await message.answer('Вы приступили к работе.', keyboard=admin_keyboard)


@bot.on.message(text="Завершить работу")
async def bye_admin(message: Message):
    admin_list = get_admins()
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in admin_list:
        if users_info[0].id in online_admins:
            online_admins.remove(users_info[0].id)
            await message.answer('Вы завершили рабочий день.', keyboard=full_screen_menu)
        else:
            await message.answer('Вы не приступали к работе.')


@bot.on.message(text="Заказы")
async def orders_list(message: Message):
    admin_list = get_admins()
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in admin_list:
        connection = mysql_connect()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT order_id FROM orders WHERE completed = {0}")
            ids_orders = cursor.fetchall()
            orders = []
            for row in ids_orders:
                orders.append(row[0])
            connection.commit()
        if not orders:
            await message.answer('Список необработанных заказов пуст.')
        else:
            str = "Количество непринятых заказов:\n" + ('#' * 20) + '\n'
            abc = len(orders)
            for row in orders:
                if row == orders[abc - 1]:
                    str += f"Заказ №{row}"
                else:
                    str += f"Заказ №{row}\n"
            await message.answer(str + '\n' + ('#' * 20))
            return "Не забудьте обработать заказ: Принять(Отклонить) НОМЕР"


@bot.on.message(text=['Принять', 'Принять <args>'])
async def completed_order(message: Message, args=None):
    admin_list = get_admins()
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in admin_list:
        if args is not None:
            if str(args).isdigit():
                connection = mysql_connect()
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT order_id FROM orders WHERE completed = {0}")
                    ids_orders = cursor.fetchall()
                    orders = []
                    for row in ids_orders:
                        orders.append(row[0])
                    connection.commit()
                if int(args) in orders:
                    connection = mysql_connect()
                    with connection.cursor() as cursor:
                        update_query = f"UPDATE `orders` SET completed = '{1}' WHERE order_id = '{int(args)}'"
                        cursor.execute(update_query)
                        connection.commit()
                        cursor.execute(f"SELECT user_id FROM orders WHERE order_id = '{int(args)}'")
                        id_order_owner = cursor.fetchone()[0]
                        cursor.execute(f"SELECT num_orders FROM users WHERE id = '{id_order_owner}'")
                        orders_num = int(cursor.fetchone()[0]) + 1
                        update_new = f"UPDATE `users` SET num_orders = '{orders_num}' WHERE id = '{id_order_owner}'"
                        cursor.execute(update_new)
                        connection.commit()
                    await message.answer(f'Заказ №{int(args)} принят.')
                    await bot.api.messages.send(peer_id=id_order_owner,
                                                message=f'Ваш заказ №{int(args)} принят. '
                                                        f'Менеджер свяжется с Вами когда заказ будет готов.',
                                                random_id=0)
                else:
                    return "Заказ с таким номером уже обработан или не существует!"
            else:
                return "Вы ввели не число."
        else:
            await message.answer('Для принятия заказа напишите: Принять НОМЕР')


@bot.on.message(text=['Отклонить', 'Отклонить <args>'])
async def completed_order(message: Message, args=None):
    admin_list = get_admins()
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in admin_list:
        if args is not None:
            if str(args).isdigit():
                connection = mysql_connect()
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT order_id FROM orders WHERE completed = {0}")
                    ids_orders = cursor.fetchall()
                    orders = []
                    for row in ids_orders:
                        orders.append(row[0])
                    connection.commit()
                if int(args) in orders:
                    connection = mysql_connect()
                    with connection.cursor() as cursor:
                        update_query = f"UPDATE `orders` SET completed = '{2}' WHERE order_id = '{int(args)}'"
                        cursor.execute(update_query)
                        connection.commit()
                        cursor.execute(f"SELECT user_id FROM orders WHERE order_id = '{int(args)}'")
                        id_order_owner = cursor.fetchone()[0]
                        connection.commit()
                    await message.answer(f'Вы отклонили заказ №{int(args)}.')
                    await bot.api.messages.send(peer_id=id_order_owner,
                                                message=f'Ваш заказ №{int(args)} был отклонен менеджером.',
                                                random_id=0)
                else:
                    return "Заказ с таким номером уже обработан или не существует!"
            else:
                return "Вы ввели не число."
        else:
            await message.answer('Для отклонения заказа напишите: Отклонить НОМЕР')


@bot.on.message(text=['Инфо', 'Информация', 'Инфо <args>', 'Инфомация <args>'])
async def completed_order(message: Message, args=None):
    admin_list = get_admins()
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in admin_list:
        if args is not None:
            if str(args).isdigit():
                connection = mysql_connect()
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT order_id FROM orders")
                    ids_orders = cursor.fetchall()
                    orders = []
                    for row in ids_orders:
                        orders.append(row[0])
                        connection.commit()
                if int(args) in orders:
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT * FROM orders WHERE order_id = '{int(args)}'")
                        order_info = cursor.fetchone()
                        connection.commit()
                    info = str(order_info[6]).replace("|", "\n")
                    await message.answer(f'Информация о заказе №{order_info[0]}:\n\n'
                                         f'{order_info[5]}\n'
                                         f'От: {order_info[2]}\nАдрес: {order_info[3]}\n'
                                         f'Тел: {order_info[4]}\n\n{"#" * 20}\n{info}\n{"#" * 20}\n\n'
                                         f'Диалог: vk.com/gim{group_id}?sel={order_info[1]}')
                else:
                    return "Такого заказа не существует."
            else:
                return "Вы ввели не число!"
        else:
            return "Вы забыли указать номер заказа. (Информация помощь)"


@bot.on.message(text=['Анкета', 'Клиент', 'Анкета <args>', 'Клиент <args>'])
async def completed_order(message: Message, args=None):
    admin_list = get_admins()
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in admin_list:
        if args is not None:
            connection = mysql_connect()
            if str(args).isdigit():
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM users WHERE id = {int(args)}")
                    user_db = cursor.fetchone()
                    connection.commit()
                if not user_db:
                    await message.answer("Пользователь с таким ID не зарегистрирован.")
                else:
                    name = user_db[1]
                    id_db = user_db[0]
                    if user_db[2] == 'empty':
                        phone = 'отсутствует'
                    else:
                        phone = user_db[2]
                    if user_db[3] == 'empty':
                        address = 'отсутствует'
                    else:
                        address = user_db[3]
                    num_orders = user_db[4]
                    if int(user_db[6]) == 0:
                        banned = 'нет'
                    else:
                        banned = 'да'
                    await message.answer(f'Информация о пользователе\n\nИмя: {name}\n'
                                         f'Личный ID: {id_db}\nКол-во заказов: {num_orders}\n'
                                         f'Тел: {phone}\nАдрес: {address}\nЗабанен: {banned}')
            else:
                photo_upd = PhotoMessageUploader(bot.api)
                photo = await photo_upd.upload("drawable/help_search_id.png")
                await message.answer(f'Пожалуйста, введите ID пользователя.\nЗайдите в переписку группы с пользователем'
                                     f' и скопируйте ID, как это показано на фотографии.', attachment=photo)
        else:
            await message.answer("Вы не указали ID пользователя.\nМожете прописать: Анкета помощь")


@bot.on.message(text=['Забанить', 'Бан', 'Забанить <args>', 'Бан <args>'])
async def completed_order(message: Message, args=None):
    admin_list = get_admins()
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in admin_list:
        if args is not None:
            connection = mysql_connect()
            if str(args).isdigit():
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT banned FROM users WHERE id = {int(args)}")
                    user_db = cursor.fetchone()
                    ban = user_db[0]
                    if ban == 0:
                        cursor.execute(f"UPDATE `users` SET banned = '{1}' WHERE id = {int(args)}")
                        await message.answer(f"Пользователь [vk.com/id{args}] был заблокирован в боте.")
                    else:
                        await message.answer(f"Пользователь [vk.com/id{args}] уже заблокирован в боте.")
                    connection.commit()
            else:
                photo_upd = PhotoMessageUploader(bot.api)
                photo = await photo_upd.upload("drawable/help_search_id.png")
                await message.answer(f'Пожалуйста, введите ID пользователя.\nЗайдите в переписку группы с пользователем'
                                     f' и скопируйте ID, как это показано на фотографии.', attachment=photo)
        else:
            await message.answer("Вы не указали ID пользователя.\nКоманда помощи: Бан помощь")


@bot.on.message(text=['Разбанить', 'Разбан', 'Разбанить <args>', 'Разбан <args>'])
async def completed_order(message: Message, args=None):
    admin_list = get_admins()
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in admin_list:
        if args is not None:
            connection = mysql_connect()
            if str(args).isdigit():
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT banned FROM users WHERE id = {int(args)}")
                    user_db = cursor.fetchone()
                    ban = user_db[0]
                    if ban == 1:
                        cursor.execute(f"UPDATE `users` SET banned = '{0}' WHERE id = {int(args)}")
                        await message.answer(f"Пользователь [vk.com/id{args}] был разблокирован в боте.")
                    else:
                        await message.answer(f"Пользователь [vk.com/id{args}] не заблокирован в боте.")
                    connection.commit()
            else:
                photo_upd = PhotoMessageUploader(bot.api)
                photo = await photo_upd.upload("drawable/help_search_id.png")
                await message.answer(f'Пожалуйста, введите ID пользователя.\nЗайдите в переписку группы с пользователем'
                                     f' и скопируйте ID, как это показано на фотографии.', attachment=photo)
        else:
            await message.answer("Вы не указали ID пользователя.\nКоманда помощи: Разбан помощь")
