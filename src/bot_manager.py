import csv
import os
from googletrans import Translator
from time import time
from discord.ext import commands
import discord
from random import choice

from src.config import DATABASE, COMMAND_PREFIX, \
                       TIMEOUT, MAX_WRONG_ANSWERS


BOT = commands.Bot(
    command_prefix=COMMAND_PREFIX,
    intents=discord.Intents.all()
)
translator = Translator()


@BOT.event
async def on_ready():
    print(f'{BOT.user} has connected to Discord!')
    channel = BOT.get_channel(int(os.environ['CHANNEL_ID']))
    await channel.send("🖐 Dobry dzień, jestem botem tłumaczącym.")


@BOT.command(name='t')
async def translate(ctx, *args):
    if len(args) == 0:
        await ctx.send("🤔 Podaj słowo / słowa do przetłumaczenia.")
        try:
            m = await BOT.wait_for(
                'message',
                check=lambda m: m.author == ctx.author,
                timeout=TIMEOUT  # Timeout set to 10 seconds
            )
            args = m.content.split()
        except TimeoutError:
            await ctx.send("⏰ Nie podałeś słowa / słów do przetłumaczenia.")
            return

    for arg in args:
        translation = translator.translate(arg.lower(), dest='pl')
        await ctx.send(f"👉 {arg} -> {translation.text}")


@BOT.command(name='a')
async def add_to_dictionary(ctx, *args):
    if len(args) == 0:
        await ctx.send("🤔 Podaj słowo / słowa do przetłumaczenia i dodania.")
        try:
            m = await BOT.wait_for(
                'message',
                check=lambda m: m.author == ctx.author,
                timeout=TIMEOUT
            )
            args = m.content.split()
        except TimeoutError:
            await ctx.send("⏰ Nie podałeś słowa / słów do przetłumaczenia.")
            return

    with open(DATABASE, 'a+', encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for word in args:
            translation = translator.translate(word.lower(), dest='pl')
            await ctx.send(f"👉 {word} -> {translation.text.lower()}")
            writer.writerow([word, translation.text.lower(), time()])

    await ctx.send("😙 Słowa dodane do słownika.")


@BOT.command(name='l')
async def learn(ctx, *args):
    if len(args) == 0:
        await ctx.send("🤔 Podaj ilość słów:")
        try:
            m = await BOT.wait_for(
                'message',
                check=lambda m: m.author == ctx.author,
                timeout=TIMEOUT
            )
            args = m.content.split()
        except TimeoutError:
            await ctx.send("⏰ Nie podałeś ilości słów do nauki.")
            return

    wrong_words = []
    selected_words = []

    with open(DATABASE, 'r', encoding="utf-8") as csvfile:
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
                timeout=TIMEOUT
            )
            if word[1] == m.content.lower():
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
        if wrong_answers >= MAX_WRONG_ANSWERS:
            await ctx.send("🤡 Za dużo błędnych odpowiedzi. Koniec nauki.")
            return
        word = choice(wrong_words)
        await ctx.send(f"👉 {word[0]}:")
        try:
            m = await BOT.wait_for(
                'message',
                check=lambda m: m.author == ctx.author,
                timeout=TIMEOUT
            )
        except TimeoutError:
            await ctx.send("⏰ Koniec czasu")
            wrong_answers += 1
            continue

        if word[1] == m.content.lower():
            await ctx.send("✅ Dobrze.")
            wrong_words.remove(word)
        else:
            await ctx.send(f"❌ Źle. Poprawna odpowiedź: {word[1]}")
            wrong_answers += 1

    await ctx.send("🤗 Koniec nauki.")
