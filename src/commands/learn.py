from unidecode import unidecode
from random import choices, choice
from dataclass_csv import DataclassReader, DataclassWriter

from src.utils import BusyContextManager, Word, get_word_weight
from src.config import GlobalConfig
from src.bot import BOT


def unique_choices(population: list, weights: list, k: int) -> list:
    """
    Returns a list of unique elements chosen from the population.
    """
    selected_words = set()

    while len(selected_words) < k:
        chosen_word = choices(population, weights)[0]
        selected_words.add(chosen_word)

    return list(selected_words)


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

        with open(GlobalConfig().DATABASE, 'r', encoding="utf-8") as csvfile:
            reader = DataclassReader(csvfile, Word)
            all_words = [row for row in reader]

        no_words = min(int(args[0]), len(all_words))

        selected_words = unique_choices(
            all_words,
            [get_word_weight(w) for w in all_words],
            no_words,
        )
        wrong_words = []
        all_words = [w for w in all_words if w not in selected_words]

        for nr, word in enumerate(list(selected_words), start=1):
            await ctx.send(f"👉 {nr}: {word.word_eng}")
            try:
                m = await BOT.wait_for(
                    'message',
                    check=lambda m: m.author == ctx.author,
                    timeout=GlobalConfig().TIMEOUT
                )
                if answers_compare(word.word_pl, m.content):
                    await ctx.send("✅ Dobrze.")
                    word.no_correct += 1
                else:
                    wrong_words.append(word)
                    await ctx.send(
                        f"❌ Źle. Poprawna odpowiedź: {word.word_pl}"
                    )
                    word.no_wrong += 1
            except TimeoutError:
                await ctx.send("⏰ Koniec czasu")
                wrong_words.append(word)

        if wrong_words:
            await ctx.send("😫 Poprawmy słowa, które były źle:")

            wrong_answers = 0
            while wrong_words:
                if wrong_answers >= GlobalConfig().MAX_WRONG_ANSWERS:
                    await ctx.send(
                        "🤡 Za dużo błędnych odpowiedzi. Koniec nauki."
                    )
                    return
                word = choice(wrong_words)
                await ctx.send(f"👉 {word.word_eng}:")
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

                if answers_compare(word.word_pl, m.content):
                    await ctx.send("✅ Dobrze.")
                    wrong_words.remove(word)
                    word.no_correct += 1
                else:
                    await ctx.send(
                        f"❌ Źle. Poprawna odpowiedź: {word.word_pl}"
                    )
                    wrong_answers += 1
                    word.no_wrong += 1

        all_words.extend(selected_words)
        all_words.sort(key=lambda w: w.timestamp, reverse=True)

        with open(
                GlobalConfig().DATABASE, 'w', encoding="utf-8", newline=''
                ) as csvfile:
            DataclassWriter(
                csvfile,
                all_words,
                Word
            ).write()

        await ctx.send("🤗 Koniec nauki.")
