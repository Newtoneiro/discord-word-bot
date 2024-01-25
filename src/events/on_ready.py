import os
from src.bot import BOT


@BOT.event
async def on_ready():
    print(f'{BOT.user} has connected to Discord!')
    channel = BOT.get_channel(int(os.environ['CHANNEL_ID']))
    await channel.send("🖐 Dobry dzień, jestem botem tłumaczącym.")
