from vkbottle.bot import Blueprint, Message
from vkbottle import CtxStorage
from data.keyboards import full_screen_menu, just_menu, more_info, back_to_start, person_keyboard, \
    input_phone, input_address
from data.config import group_id
from commands.admins.admin_commands import online_admins
from misc.order import Order
from misc.address import Address
from bot import mysql_connect

bot = Blueprint("Only users chat command")
ctx = CtxStorage()


@bot.on.private_message(text=['Начать', 'Ку', 'Привет' '/start'])
async def hello(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    connection = mysql_connect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT id FROM users WHERE id = {users_info[0].id}")
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO `users` (id, name, surname, phone, address, num_orders) "
                       f"VALUES ('{users_info[0].id}', '{users_info[0].first_name}', "
                       f"'{users_info[0].last_name}', 'empty', 'empty', 0);")
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
        if phone == 'empty':
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
        if address == 'empty':
            await message.answer("Вы еще не указали свой адрес.", keyboard=input_address)
        else:
            await message.answer("Ваш адрес: " + address)


@bot.on.private_message(text=['Связаться', 'Вопрос', 'Помощь'])
async def answer(message: Message):
    user = await bot.api.users.get(message.from_id)
    if not online_admins:
        await message.answer('Ни одного менеджера нет в сети, возможно сегодня не рабочий день.')
    else:
        await message.answer("Хорошо, сейчас я вызову менеджера, пока можете сформулировать свой вопрос.")
        await bot.api.messages.send(peer_ids=online_admins,
                                    message=f'Пользователь [vk.com/id{user[0].id}|'
                                            f'{user[0].first_name} {user[0].last_name}]'
                                            f' хочет связаться с менеджером!\nОтветить: '
                                            f'vk.com/gim{group_id}?sel={user[0].id}', random_id=0)


@bot.on.private_message(text='Указать номер телефона')
async def hi_handler(message: Message):
    await bot.state_dispenser.set(message.peer_id, Order.PHONE)
    return "Напишите мне свой номер телефона.\nПример: 89261231212"


@bot.on.private_message(state=Order.PHONE)
async def Phone(message: Message):
    #TODO: regex красивый вывод номера телефона
    ctx.set('phone', message.text)
    users_info = await bot.api.users.get(message.from_id)
    if len(ctx.get('phone')) >= 11:
        if str(ctx.get('phone')).isdigit():
            await message.answer(f'Ваш номер телефона: ' + ctx.get('phone'))
            connection = mysql_connect()
            with connection.cursor() as cursor:
                update_query = f"UPDATE `users` SET phone = '{ctx.get('phone')}' WHERE id = '{users_info[0].id}'"
                cursor.execute(update_query)
                connection.commit()
            return "Номер телефона сохранен, если Вы допустили ошибку, введите команду еще раз."
    else:
        return "Это не похоже на номер телефона, воспользуйтесь командой еще раз."


@bot.on.private_message(text='Указать свой адрес')
async def City(message: Message):
    await bot.state_dispenser.set(message.peer_id, Order.CITY)
    return "Напишите мне свой город."


@bot.on.private_message(state=Order.CITY)
async def Street(message: Message):
    ctx.set('city', message.text)
    await bot.state_dispenser.set(message.peer_id, Order.STREET)
    return "Отлично, а теперь улицу."


@bot.on.private_message(state=Order.STREET)
async def Home(message: Message):
    ctx.set('street', message.text)
    await bot.state_dispenser.set(message.peer_id, Order.HOME)
    return "Введите номер дома (включая корпус или строение)."


@bot.on.private_message(state=Order.HOME)
async def Flat(message: Message):
    ctx.set('home', message.text)
    await bot.state_dispenser.set(message.peer_id, Order.FLAT)
    return "Теперь мне нужен номер квартиры."


@bot.on.private_message(state=Order.FLAT)
async def Doorphone(message: Message):
    ctx.set('flat', message.text)
    await bot.state_dispenser.set(message.peer_id, Order.DOORPHONE)
    return "А сейчас укажите код домофона (если кода нет, просто введите квартиру)."


@bot.on.private_message(state=Order.DOORPHONE)
async def Floor(message: Message):
    ctx.set('doorphone', message.text)
    await bot.state_dispenser.set(message.peer_id, Order.FLOOR)
    return "Последний штрих, укажите свой этаж."


@bot.on.private_message(state=Order.FLOOR)
async def End(message: Message):
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
    return "Данные сохранены, если Вы допустили ошибку, перезапишите свой адрес еще раз."
