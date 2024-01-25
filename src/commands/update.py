import csv
import shutil
from tempfile import NamedTemporaryFile

from src.utils import BusyContextManager
from src.config import GlobalConfig
from src.bot import BOT


@BOT.command(name='u')
async def update(ctx, *args):
    if BusyContextManager.is_busy():
        return

    with BusyContextManager():
        if len(args) != 1:
            await ctx.send("🤔 Podaj słowo do poprawy.")
            try:
                m = await BOT.wait_for(
                    'message',
                    check=lambda m: m.author == ctx.author,
                    timeout=GlobalConfig().TIMEOUT  # Timeout set to 10 seconds
                )
                m = m.content
            except TimeoutError:
                await ctx.send("⏰ Nie podałeś słowa do poprawy.")
                return
        else:
            m = args[0]

        tempfile = NamedTemporaryFile(
            mode='w', delete=False, encoding="utf-8", newline=''
        )
        word_found = False
        with open(
                GlobalConfig().DATABASE, 'r', encoding="utf-8", newline=''
                ) as csvfile, tempfile:
            reader = csv.DictReader(csvfile, fieldnames=GlobalConfig().FIELDS)
            writer = csv.DictWriter(tempfile, fieldnames=GlobalConfig().FIELDS)
            for row in reader:
                if row['word'] == m.lower():
                    word_found = True
                    await ctx.send(
                        f"Obecne tłumaczenie: {row['word']}" +
                        f"👉 {row['translation']}"
                    )

                    await ctx.send(
                        "👏 Podaj nowe tłumaczenie: "
                    )
                    try:
                        m = await BOT.wait_for(
                            'message',
                            check=lambda m: m.author == ctx.author,
                            timeout=GlobalConfig().TIMEOUT
                        )
                        m = m.content
                    except TimeoutError:
                        await ctx.send("⏰ Nie podałeś nowego tłumaczenia.")
                        return

                    row['translation'] = m.lower()
                row = {
                    'word': row['word'],
                    'translation': row['translation'],
                    'timestamp': row['timestamp']
                }
                writer.writerow(row)

        shutil.move(tempfile.name, GlobalConfig().DATABASE)

        if word_found:
            await ctx.send("🤗 Słowo poprawione.")
        else:
            await ctx.send("😫 Nie znaleziono słowa.")
