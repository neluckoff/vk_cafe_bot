from vkbottle.bot import Blueprint, Message
from data.config import admin_list

bot = Blueprint("Admin")
online_admins = []


@bot.on.message(text="Начать работу")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in admin_list:
        if users_info[0].id in online_admins:
            await message.answer('Вы уже начали рабочий день.')
        else:
            online_admins.append(users_info[0].id)
            await message.answer('Вы приступили к работе.')


@bot.on.message(text="Завершить работу")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    if users_info[0].id in admin_list:
        if users_info[0].id in online_admins:
            online_admins.remove(users_info[0].id)
            await message.answer('Вы завершили рабочий день.')
        else:
            await message.answer('Вы не приступали к работе.')
