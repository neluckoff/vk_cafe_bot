from environs import Env

"""
Модуль с информацией о сообществе и токене бота
"""

env = Env()
env.read_env()

BOT_TOKEN = env.str("TOKEN")
group_id = env.int("group_id")
hight_admin = [146653997]

"""
Модуль с информацией о базе данных
"""

host = "localhost"
user = env.str("db_user")
password = env.str("db_password")
db_name = "cafe"
