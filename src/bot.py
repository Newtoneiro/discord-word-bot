from discord.ext import commands
import discord

from src.config import GlobalConfig


BOT = commands.Bot(
    command_prefix=GlobalConfig().COMMAND_PREFIX,
    intents=discord.Intents.all()
)

# flake8: noqa
from src.events import *
from src.commands import *
