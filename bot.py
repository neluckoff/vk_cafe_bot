from vkbottle.bot import Bot
from vkbottle import load_blueprints_from_package
from data.config import BOT_TOKEN, group_id, host, db_name, user, password
import pymysql


if __name__ == "__main__":
    bot = Bot(BOT_TOKEN, group_id)
    bot.labeler.vbml_ignore_case = True

    for bp in load_blueprints_from_package("commands"):
        bp.load(bot)

    # TODO: разобраться с портами
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name
        )
        print("bd connected")
    except Exception as ex:
        print(ex)

    bot.run_forever()
