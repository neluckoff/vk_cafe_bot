from vkbottle.bot import Bot
from vkbottle import load_blueprints_from_package
from data.config import BOT_TOKEN, group_id, host, db_name, user, password
import pymysql


def mysql_connect():
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name
    )
    return connection


if __name__ == "__main__":
    bot = Bot(BOT_TOKEN, group_id)
    bot.labeler.vbml_ignore_case = True

    for bp in load_blueprints_from_package("commands"):
        bp.load(bot)

    try:
        connection = mysql_connect()
        print("Database has been connected")

        cursor = connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                   id int AUTO_INCREMENT,
                   name varchar(32),
                   phone varchar(32),
                   address varchar(500),
                   num_orders int(15),
                   status varchar(32),
                   banned BOOLEAN,
                   PRIMARY KEY(id)
               )""")
        connection.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
                    order_id int AUTO_INCREMENT,
                    user_id int,
                    name varchar(80),
                    address varchar(500),
                    phone varchar(32),
                    date varchar(32),
                    order_list varchar(1000),
                    completed BOOLEAN, 
                    PRIMARY KEY(order_id)
                       )""")
        connection.commit()

    except Exception as ex:
        print(ex)

    bot.run_forever()
