from vkbottle.bot import Blueprint, Message
from data.config import admin_list
from bot import mysql_connect, group_id

bot = Blueprint("Admin")
online_admins = []


@bot.on.message(text="Начать работу")
async def hi_admin(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in admin_list:
        if users_info[0].id in online_admins:
            await message.answer('Вы уже начали рабочий день.')
        else:
            online_admins.append(users_info[0].id)
            await message.answer('Вы приступили к работе.')


@bot.on.message(text="Завершить работу")
async def bye_admin(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in admin_list:
        if users_info[0].id in online_admins:
            online_admins.remove(users_info[0].id)
            await message.answer('Вы завершили рабочий день.')
        else:
            await message.answer('Вы не приступали к работе.')


@bot.on.message(text="Заказы")
async def orders_list(message: Message):
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
            await message.answer('Для принятия заказа напишите: Отклонить НОМЕР')


@bot.on.message(text=['Инфо', 'Информация', 'Инфо <args>', 'Инфомация <args>'])
async def completed_order(message: Message, args=None):
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
            return "Вы забыли указать номер заказа."
