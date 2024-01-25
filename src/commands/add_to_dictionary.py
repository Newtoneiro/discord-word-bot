import csv
from googletrans import Translator
from time import time

from src.utils import BusyContextManager
from src.config import GlobalConfig
from src.bot import BOT


@BOT.command(name='a')
async def add_to_dictionary(ctx, *args):
    if BusyContextManager.is_busy():
        return

    with BusyContextManager():
        if len(args) == 0:
            await ctx.send(
                "🤔 Podaj słowo / słowa do przetłumaczenia i dodania."
            )
            try:
                m = await BOT.wait_for(
                    'message',
                    check=lambda m: m.author == ctx.author,
                    timeout=GlobalConfig().TIMEOUT
                )
                args = m.content.split()
            except TimeoutError:
                await ctx.send(
                    "⏰ Nie podałeś słowa / słów do przetłumaczenia."
                )
                return

        with open(
                GlobalConfig().DATABASE, 'a+', encoding="utf-8", newline=''
                ) as csvfile:
            writer = csv.writer(csvfile)
            for word in args:
                translation = Translator().translate(word.lower(), dest='pl')
                await ctx.send(f"👉 {word} -> {translation.text.lower()}")
                writer.writerow([word, translation.text.lower(), time()])

        await ctx.send("😙 Słowa dodane do słownika.")
