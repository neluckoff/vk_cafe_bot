from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback

full_screen_menu = (
    Keyboard(one_time=False, inline=False)
        .add(Text('Сделать заказ'), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text('О нас'), color=KeyboardButtonColor.PRIMARY)
        .add(Text('Связаться'), color=KeyboardButtonColor.PRIMARY)
).get_json()

just_menu = (
    Keyboard(one_time=False, inline=False)
        .add(Text('Меню'), color=KeyboardButtonColor.PRIMARY)
        .add(Text('Указать свой адрес'), color=KeyboardButtonColor.POSITIVE)
).get_json()

more_info = (
    Keyboard(one_time=False, inline=False)
        .add(Text("Наш адрес"), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Товары"), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("Отзывы"), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Скидки"), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("👈🏻 Назад"), color=KeyboardButtonColor.PRIMARY)
)
