import os
from src.bot_manager import BOT
from dotenv import load_dotenv
from src.config import GlobalConfig


if __name__ == "__main__":
    load_dotenv()
    GlobalConfig().init_database(os.environ['DATABASE'])
    print(GlobalConfig().DATABASE)
    if not os.environ['DATABASE']:
        print("DATABASE environment variable not set.")
        exit(1)

    BOT.run(token=os.environ['BOT_TOKEN'])
