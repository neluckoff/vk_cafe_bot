import pandas as pd
import os
from vkbottle import PhotoMessageUploader, DocMessagesUploader
from vkbottle.bot import Blueprint, Message

from bot import mysql_connect, group_id
from data.big_strings import admin_memo
from data.config import hight_admin
from data.keyboards import admin_keyboard, full_screen_menu_adm

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


def check_id_in_db(user_id: int):
    connection = mysql_connect()
    list_users = []
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT id FROM users')
        users = cursor.fetchall()
        for row in users:
            list_users.append(row[0])
        connection.commit()
    if user_id in list_users:
        return True
    else:
        return False


@bot.on.message(text="Начать работу")
async def hi_admin(message: Message):
    admin_list = get_admins()
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in admin_list:
        if users_info[0].id in online_admins:
            await message.answer('Вы уже начали рабочий день.', keyboard=admin_keyboard)
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
            await message.answer('Вы завершили рабочий день.', keyboard=full_screen_menu_adm)
        else:
            await message.answer('Вы не приступали к работе.', keyboard=full_screen_menu_adm)


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
                if check_id_in_db(int(args)):
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
                    return "Пользователь с таким ID не зарегестрирован."
            else:
                photo_upd = PhotoMessageUploader(bot.api)
                photo = await photo_upd.upload("assets/help_search_id.png")
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
                if check_id_in_db(int(args)):
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT banned FROM users WHERE id = {int(args)}")
                        user_db = cursor.fetchone()
                        ban = user_db[0]
                        if ban == 0:
                            cursor.execute(f"UPDATE `users` SET banned = '{1}' WHERE id = {int(args)}")
                            await message.answer(f"Пользователь [vk.com/id{args}] был заблокирован в боте.")
                            await bot.api.messages.send(peer_id=int(args),
                                                        message="[❗] Вам был ограничен доступ в "
                                                                "боте за плохое поведение.",
                                                        random_id=0)
                        else:
                            await message.answer(f"Пользователь [vk.com/id{args}] уже заблокирован в боте.")
                        connection.commit()
                else:
                    return "Пользователь с таким ID не зарегестрирован."
            else:
                photo_upd = PhotoMessageUploader(bot.api)
                photo = await photo_upd.upload("assets/help_search_id.png")
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
                if check_id_in_db(int(args)):
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
                    return "Пользователь с таким ID не зарегестрирован."
            else:
                photo_upd = PhotoMessageUploader(bot.api)
                photo = await photo_upd.upload("assets/help_search_id.png")
                await message.answer(f'Пожалуйста, введите ID пользователя.\nЗайдите в переписку группы с пользователем'
                                     f' и скопируйте ID, как это показано на фотографии.', attachment=photo)
                await bot.api.messages.send(peer_id=int(args),
                                            message="[❗] Вам вернули полный доступ в боте. Больше не нарушайте!",
                                            random_id=0)
        else:
            await message.answer("Вы не указали ID пользователя.\nКоманда помощи: Разбан помощь")


@bot.on.message(text=['Админ', 'Сделать админом', 'Сделать админом <args>', 'Админ <args>'])
async def completed_order(message: Message, args=None):
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in hight_admin:
        if args is not None:
            connection = mysql_connect()
            if str(args).isdigit():
                if check_id_in_db(int(args)):
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT status FROM users WHERE id = {int(args)}")
                        user_db = cursor.fetchone()
                        if user_db[0] == "user":
                            cursor.execute(f"UPDATE `users` SET status = 'admin' WHERE id = {int(args)}")
                            await message.answer(f'Пользователь [vk.com/id{args}] стал администратором.')
                        else:
                            await message.answer(f'Пользователь [vk.com/id{args}] уже является администратором.')
                        connection.commit()
                else:
                    return "Пользователь с таким ID не зарегестрирован."
            else:
                photo_upd = PhotoMessageUploader(bot.api)
                photo = await photo_upd.upload("assets/help_search_id.png")
                await message.answer(f'Пожалуйста, введите ID пользователя.\nЗайдите в переписку группы с пользователем'
                                     f' и скопируйте ID, как это показано на фотографии.', attachment=photo)
        else:
            await message.answer("Вы не указали ID пользователя.")


@bot.on.message(text=['Памятка'])
async def completed_order(message: Message):
    admin_list = get_admins()
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in admin_list:
        await message.answer(admin_memo)


@bot.on.message(text=['Скачать таблицу заказов'])
async def completed_order(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in hight_admin:
        connection = mysql_connect()
        id_order = []
        id_user = []
        name = []
        address = []
        phone = []
        date = []
        order = []
        await message.answer("Начинаю создание таблицы...")
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM orders")
            all_orders = cursor.fetchall()
            for row in all_orders:
                id_order.append(row[0])
                id_user.append(row[1])
                name.append(row[2])
                address.append(row[3])
                phone.append(row[4])
                date.append(row[5])
                order.append(str(row[6]).replace('|', '; '))
        connection.commit()
    df = pd.DataFrame({'№': id_order, 'ID клиента': id_user, 'Имя': name, 'Адресс': address,
                       'Телефон': phone, 'Дата': date, 'Заказ': order})
    df.to_excel('./assets/order_table.xlsx', sheet_name='Таблица заказов', index=False)
    doc_upd = DocMessagesUploader(bot.api)
    doc = await doc_upd.upload("Таблица заказов.xlsx", "assets/order_table.xlsx", peer_id=message.peer_id)
    await message.answer(f'Таблица сгенерирована.', attachment=doc)
    os.remove("./assets/order_table.xlsx")
    print('The order table has been created')


@bot.on.message(text=['Скачать таблицу пользователей'])
async def completed_order(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in hight_admin:
        connection = mysql_connect()
        user_id = []
        name = []
        phone = []
        address = []
        num_orders = []
        status = []
        banned = []
        await message.answer("Начинаю создание таблицы...")
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users")
            all_users = cursor.fetchall()
            for row in all_users:
                user_id.append(row[0])
                name.append(row[1])
                if row[2] == 'empty':
                    phone.append('Отсутствует')
                else:
                    phone.append(row[2])
                if row[3] == 'empty':
                    address.append('Отсутствует')
                else:
                    address.append(row[3])
                num_orders.append(row[4])
                status.append(row[5])
                if row[6] == 0:
                    banned.append("Нет")
                else:
                    banned.append("Да")
        connection.commit()
    df = pd.DataFrame({'ID': user_id, 'Имя': name, 'Адресс': address, 'Телефон': phone, 'Кол-во заказов': num_orders,
                       'Статус': status, 'Забанен': banned})
    df.to_excel('./assets/user_table.xlsx', sheet_name='Таблица пользователей', index=False)
    doc_upd = DocMessagesUploader(bot.api)
    doc = await doc_upd.upload("Таблица пользователей.xlsx", "assets/user_table.xlsx", peer_id=message.peer_id)
    await message.answer(f'Таблица сгенерирована.', attachment=doc)
    os.remove("./assets/user_table.xlsx")
    print('[+] The user table has been created')
