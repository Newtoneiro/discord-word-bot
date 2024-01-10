import os
from src.bot_manager import BOT
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    BOT.run(token=os.environ['BOT_TOKEN'])
