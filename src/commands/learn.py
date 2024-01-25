import csv
from unidecode import unidecode
from random import choice

from src.utils import BusyContextManager
from src.config import GlobalConfig
from src.bot import BOT


@BOT.command(name='l')
async def learn(ctx, *args):
    def answers_compare(expected: str, answer: str):
        return unidecode(answer.lower()) == unidecode(expected.lower())

    if BusyContextManager.is_busy():
        return

    with BusyContextManager():
        if len(args) != 1:
            await ctx.send("🤔 Podaj ilość słów:")
            try:
                m = await BOT.wait_for(
                    'message',
                    check=lambda m: m.author == ctx.author,
                    timeout=GlobalConfig().TIMEOUT
                )
                if not m.content.isdigit() or int(m.content) < 1:
                    raise ValueError
                args = m.content.split()
                if len(args) != 1:
                    raise ValueError
            except ValueError:
                await ctx.send("🤡 Podaj poprawną liczbę")
                return
            except TimeoutError:
                await ctx.send("⏰ Nie podałeś ilości słów do nauki.")
                return

        wrong_words = []
        selected_words = []

        with open(GlobalConfig().DATABASE, 'r', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            all_words = [row for row in reader]

        no_words = min(int(args[0]), len(all_words))
        for nr in range(1, no_words + 1):
            word = choice(all_words)
            while word in selected_words and \
                    len(selected_words) < len(all_words):
                word = choice(all_words)
            selected_words.append(word)

            await ctx.send(f"👉 {nr}: {word[0]}")
            try:
                m = await BOT.wait_for(
                    'message',
                    check=lambda m: m.author == ctx.author,
                    timeout=GlobalConfig().TIMEOUT
                )
                if answers_compare(word[1], m.content):
                    await ctx.send("✅ Dobrze.")
                else:
                    wrong_words.append(word)
                    await ctx.send(f"❌ Źle. Poprawna odpowiedź: {word[1]}")
            except TimeoutError:
                await ctx.send("⏰ Koniec czasu")
                wrong_words.append(word)

        if wrong_words:
            await ctx.send("😫 Poprawmy słowa, które były źle:")

        wrong_answers = 0
        while wrong_words:
            if wrong_answers >= GlobalConfig().MAX_WRONG_ANSWERS:
                await ctx.send("🤡 Za dużo błędnych odpowiedzi. Koniec nauki.")
                return
            word = choice(wrong_words)
            await ctx.send(f"👉 {word[0]}:")
            try:
                m = await BOT.wait_for(
                    'message',
                    check=lambda m: m.author == ctx.author,
                    timeout=GlobalConfig().TIMEOUT
                )
            except TimeoutError:
                await ctx.send("⏰ Koniec czasu")
                wrong_answers += 1
                continue

            if answers_compare(word[1], m.content):
                await ctx.send("✅ Dobrze.")
                wrong_words.remove(word)
            else:
                await ctx.send(f"❌ Źle. Poprawna odpowiedź: {word[1]}")
                wrong_answers += 1

        await ctx.send("🤗 Koniec nauki.")
