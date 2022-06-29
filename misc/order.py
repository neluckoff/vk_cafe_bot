from vkbottle import CtxStorage, BaseStateGroup


class Order(BaseStateGroup):
    CITY = 1
    STREET = 2
    HOME = 3
    FLAT = 4
    DOORPHONE = 5
    FLOOR = 6
    END = 7


class Address:

    def __init__(self, city, street, home, flat, doorphone, floor):
        self.city = city
        self.street = street
        self.home = home
        self.flat = flat
        self.doorphone = doorphone
        self.floor = floor
