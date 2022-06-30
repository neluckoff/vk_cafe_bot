from misc.address import Address


class User:
    def __init__(self, id: int, name: str, surname: str, address: Address):
        self.id = id
        self.name = name
        self.surname = surname
        self.address = address

    def get_name(self):
        return self.name

    def get_surname(self):
        return self.surname

    def get_id(self):
        return self.id

    def get_address(self):
        return self.address.to_string()
