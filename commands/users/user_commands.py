from vkbottle.bot import Blueprint, Message
from vkbottle import BaseStateGroup, CtxStorage
from data.keyboards import full_screen_menu, just_menu, more_info
from commands.admins.admin_commands import online_admins
from misc.order import Order, Address

bot = Blueprint("Only users chat command")
ctx = CtxStorage()


@bot.on.private_message(text=['Начать', 'Ку', 'Привет' '/start'])
async def hello(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer("Здравствуйте, {}".format(users_info[0].first_name) + "!" +
                         "\nЗаполните Ваш адрес для будующих заказов или же нажмите \"Меню\" чтобы продолжить.", keyboard=just_menu)


@bot.on.message(text=['Меню', '/menu', '👈🏻 Назад'])
async def hi_handler(message: Message):
    await message.answer("Вы вызвали меню.", keyboard=full_screen_menu)


@bot.on.message(text=['О нас'])
async def hi_handler(message: Message):
    await message.answer("Мы - лучшее кафе на рынке РФ.", keyboard=more_info)


@bot.on.private_message(text=['Связаться', 'Вопрос', 'Помощь'])
async def answer(message: Message):
    user = await bot.api.users.get(message.from_id)
    if not online_admins:
        await message.answer('Ни одного менеджера нет в сети, возможно сегодня не рабочий день.')
    else:
        await message.answer("Хорошо, сейчас я вызову менеджера, пока можете сформулировать свой вопрос.")
        # TODO: поправить ссылку для сообщества
        await bot.api.messages.send(peer_ids=online_admins,
                                    message=f'Пользователь [vk.com/id{user[0].id}|'
                                            f'{user[0].first_name} {user[0].last_name}]'
                                            f' хочет связаться с менеджером!\nОтветить: '
                                            f'vk.com/gim132641953?sel={user[0].id}', random_id=0)


@bot.on.private_message(text='Указать свой адрес')
async def City(message: Message):
    await bot.state_dispenser.set(message.peer_id, Order.CITY)
    return "Введите Ваш город"


@bot.on.private_message(state=Order.CITY)
async def Street(message: Message):
    ctx.set('city', message.text)
    await bot.state_dispenser.set(message.peer_id, Order.STREET)
    return "Улица"


@bot.on.private_message(state=Order.STREET)
async def Home(message: Message):
    ctx.set('street', message.text)
    await bot.state_dispenser.set(message.peer_id, Order.HOME)
    return "Дом"


@bot.on.private_message(state=Order.HOME)
async def Flat(message: Message):
    ctx.set('home', message.text)
    await bot.state_dispenser.set(message.peer_id, Order.FLAT)
    return "Квартира"


@bot.on.private_message(state=Order.FLAT)
async def Doorphone(message: Message):
    ctx.set('flat', message.text)
    await bot.state_dispenser.set(message.peer_id, Order.DOORPHONE)
    return "Домофон"


@bot.on.private_message(state=Order.DOORPHONE)
async def Floor(message: Message):
    ctx.set('doorphone', message.text)
    await bot.state_dispenser.set(message.peer_id, Order.FLOOR)
    return "Этаж"


@bot.on.private_message(state=Order.FLOOR)
async def End(message: Message):
    ctx.set('floor', message.text)
    await message.answer(f'Ваш адрес: ' + ctx.get('city') + ', ' + ctx.get('street') + ', ' + ctx.get('home') + ', ' +
                         ctx.get('flat') + ', ' + ctx.get('doorphone') + ', ' + ctx.get('floor'))
    address: Address = Address(ctx.get('city'), ctx.get('street'), ctx.get('home'), ctx.get('flat'), ctx.get('doorphone'), ctx.get('floor'))
    print(address)
    return "Данные сохранены, если Вы допустили ошибку, перезапишите свой адрес еще раз."
