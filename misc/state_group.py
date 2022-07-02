from vkbottle import BaseStateGroup


class Phone(BaseStateGroup):
    NUMBER = 1
    END = 2


class AddressState(BaseStateGroup):
    CITY = 1
    STREET = 2
    HOME = 3
    FLAT = 4
    DOORPHONE = 5
    FLOOR = 6
    END = 8


class Order(BaseStateGroup):
    DELIVERY = 1
    INFO_DEL = 2
    INFO_SAM = 3
    END = 4
