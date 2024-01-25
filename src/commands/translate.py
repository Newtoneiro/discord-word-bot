from googletrans import Translator

from src.utils import BusyContextManager
from src.config import GlobalConfig
from src.bot import BOT


@BOT.command(name='t')
async def translate(ctx, *args):
    if BusyContextManager.is_busy():
        return

    with BusyContextManager():
        if len(args) == 0:
            await ctx.send("🤔 Podaj słowo / słowa do przetłumaczenia.")
            try:
                m = await BOT.wait_for(
                    'message',
                    check=lambda m: m.author == ctx.author,
                    timeout=GlobalConfig().TIMEOUT  # Timeout set to 10 seconds
                )
                args = m.content.split()
            except TimeoutError:
                await ctx.send(
                    "⏰ Nie podałeś słowa / słów do przetłumaczenia."
                )
                return

        for arg in args:
            translation = Translator().translate(arg.lower(), dest='pl')
            await ctx.send(f"👉 {arg} -> {translation.text}")
