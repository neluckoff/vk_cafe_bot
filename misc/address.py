class Address:

    def __init__(self, city, street, home, flat, doorphone, floor):
        self.city = city
        self.street = street
        self.home = home
        self.flat = flat
        self.doorphone = doorphone
        self.floor = floor

    def to_string(self):
        string = 'г. ' + self.city + ', ' + self.street + \
                 ' ' + self.home + ', кв. ' + self.flat + \
                 ', этаж ' + self.floor + ', домофон ' + self.doorphone
        return string