from dataclass_csv import DataclassWriter
from googletrans import Translator
from time import time

from src.utils import BusyContextManager, Word
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
                    "⏰ Nie podałeś słowa / słów do przetłumaczenia i dodania."
                )
                return

        with open(
                GlobalConfig().DATABASE, 'a+', encoding="utf-8", newline=''
                ) as csvfile:
            words_to_write = []
            for word in args:
                translation = Translator().translate(word.lower(), dest='pl')
                await ctx.send(f"👉 {word} -> {translation.text.lower()}")
                words_to_write.append(
                    Word(
                        word_eng=word.lower(),
                        word_pl=translation.text.lower(),
                        timestamp=time(),
                        no_correct=0,
                        no_wrong=0
                    )
                )
            writer = DataclassWriter(csvfile, words_to_write, Word)
            writer.write(skip_header=True)

        await ctx.send("😙 Słowa dodane do słownika.")
