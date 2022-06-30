from environs import Env

"""
Модуль с информацией о сообществе и токене бота
"""

env = Env()
env.read_env()

BOT_TOKEN = env.str("TOKEN")
group_id = env.int("group_id")
admin_list = [146653997]

"""
Модуль с информацией о базе данных
"""

host = "localhost"
user = "admin"
password = "1234"
db_name = "users"
