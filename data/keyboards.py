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

full_screen_menu_adm = (
    Keyboard(one_time=False, inline=False)
    .add(Text('Сделать заказ'), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text('О нас'), color=KeyboardButtonColor.PRIMARY)
    .add(Text('Связаться'), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('Личный кабинет'), color=KeyboardButtonColor.SECONDARY)
    .add(Text('Начать работу'), color=KeyboardButtonColor.POSITIVE)
).get_json()

just_menu = (
    Keyboard(one_time=False, inline=False)
    .add(Text('Меню'), color=KeyboardButtonColor.PRIMARY)
    .add(Text('Указать свой адрес'), color=KeyboardButtonColor.POSITIVE)
).get_json()

more_info = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Наш адрес"), color=KeyboardButtonColor.PRIMARY)
    .add((Callback("Наше меню", {"cmd": "cafe_menu"})), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add((Callback("Отзывы", {"cmd": "reviews"})), color=KeyboardButtonColor.PRIMARY)
    .add((Callback("Скидки", {"cmd": "sales"})), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("👈🏻 Назад"), color=KeyboardButtonColor.NEGATIVE)
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

input_all = (
    Keyboard(inline=True)
    .add(Text('Указать номер телефона'), color=KeyboardButtonColor.PRIMARY)
    .add(Text('Указать свой адрес'), color=KeyboardButtonColor.PRIMARY)
).get_json()

delivery_keyboard = (
    Keyboard(inline=True)
    .add(Text('Доставка'), color=KeyboardButtonColor.POSITIVE)
    .add(Text('Самовывоз'), color=KeyboardButtonColor.POSITIVE)
).get_json()

admin_keyboard = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Заказы"), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("Принять"), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Информация"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Отклонить"), color=KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text("Разбанить"), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Клиент"), color=KeyboardButtonColor.SECONDARY)
    .add(Text("Забанить"), color=KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text("Памятка"), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Завершить работу"), color=KeyboardButtonColor.NEGATIVE)

).get_json()


def ask_keyboard(id_ques, id_user):
    k = (Keyboard(inline=True)
         .add(Text(f'Обработать {id_ques}'), color=KeyboardButtonColor.PRIMARY)
         .add(Text(f'Клиент {id_user}'), color=KeyboardButtonColor.SECONDARY)
         ).get_json()
    return k


def order_keyboard(id_order):
    k = (Keyboard(inline=True)
         .add(Text(f'Принять {id_order}'), color=KeyboardButtonColor.POSITIVE)
         .add(Text(f'Отклонить {id_order}'), color=KeyboardButtonColor.NEGATIVE)
         ).get_json()
    return k
