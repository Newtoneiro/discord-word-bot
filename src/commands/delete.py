import shutil
from dataclass_csv import DataclassReader, DataclassWriter
from tempfile import NamedTemporaryFile

from src.utils import BusyContextManager, Word
from src.config import GlobalConfig
from src.bot import BOT


@BOT.command(name='d')
async def delete(ctx, *args):
    if BusyContextManager.is_busy():
        return

    with BusyContextManager():
        if len(args) != 1:
            await ctx.send("🤔 Podaj słowo do usunięcia.")
            try:
                m = await BOT.wait_for(
                    'message',
                    check=lambda m: m.author == ctx.author,
                    timeout=GlobalConfig().TIMEOUT  # Timeout set to 10 seconds
                )
                m = m.content
            except TimeoutError:
                await ctx.send("⏰ Nie podałeś słowa do usunięcia.")
                return
        else:
            m = args[0]

        tempfile = NamedTemporaryFile(
            mode='w', delete=False, encoding="utf-8", newline=''
        )
        word_found = False
        words_to_save = []
        with open(
                GlobalConfig().DATABASE, 'r', encoding="utf-8", newline=''
                ) as csvfile, tempfile:
            reader = DataclassReader(csvfile, Word)
            for word in reader:
                if word.word_eng == m.lower():
                    word_found = True
                    continue
                words_to_save.append(word)

            DataclassWriter(
                tempfile,
                words_to_save,
                Word
            ).write()
        shutil.move(tempfile.name, GlobalConfig().DATABASE)

        if word_found:
            await ctx.send("🤗 Słowo usunięte.")
        else:
            await ctx.send("😫 Nie znaleziono słowa.")
