from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback

full_screen_menu = (
    Keyboard(one_time=False, inline=False)
        .add(Text('Сделать заказ'), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text('О нас'), color=KeyboardButtonColor.PRIMARY)
        .add(Text('Связаться'), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text('Личный кабинет'), color=KeyboardButtonColor.SECONDARY)
).get_json()

just_menu = (
    Keyboard(one_time=False, inline=False)
        .add(Text('Меню'), color=KeyboardButtonColor.PRIMARY)
        .add(Text('Указать свой адрес'), color=KeyboardButtonColor.POSITIVE)
).get_json()

more_info = (
    Keyboard(one_time=False, inline=False)
        .add(Text("Наш адрес"), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Наше меню"), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("Отзывы"), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Скидки"), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("👈🏻 Назад"), color=KeyboardButtonColor.PRIMARY)
).get_json()

back_to_start = (
    Keyboard(inline=True)
        .add(Text('Начать'), color=KeyboardButtonColor.PRIMARY)
).get_json()

person_keyboard = (
    Keyboard(one_time=False, inline=False)
        .add(Text("Мой телефон"), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Мой адрес"), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("👈🏻 Назад"), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Количество заказов"), color=KeyboardButtonColor.PRIMARY)
).get_json()

input_phone = (
    Keyboard(inline=True)
        .add(Text('Указать номер телефона'), color=KeyboardButtonColor.PRIMARY)
).get_json()

input_address = (
    Keyboard(inline=True)
        .add(Text('Указать свой адрес'), color=KeyboardButtonColor.PRIMARY)
).get_json()
