from vkbottle import BaseStateGroup


class Order(BaseStateGroup):
    CITY = 1
    STREET = 2
    HOME = 3
    FLAT = 4
    DOORPHONE = 5
    FLOOR = 6
    PHONE = 7
    END = 8


class OrderInfo:
    def __init__(self, user_id, order_id, date, order_list, status):
        self.user_id = user_id
        self.order_id = order_id
        self.date = date
        self.order_list = order_list
        self.status = status

    def set_status(self, status):
        self.status = status

    def status_received(self):
        self.status = True

