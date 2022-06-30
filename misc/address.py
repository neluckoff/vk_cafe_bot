class Address:

    def __init__(self, city, street, home, flat, doorphone, floor):
        self.city = city
        self.street = street
        self.home = home
        self.flat = flat
        self.doorphone = doorphone
        self.floor = floor

    def to_string(self):
        string = 'Город: ' + self.city + '\nУлица: ' + self.street + \
                 '\nДом: ' + self.home + '\nКвартира: ' + self.flat + \
                 '\nЭтаж ' + self.floor + '\nДомофон: ' + self.doorphone
        return string
