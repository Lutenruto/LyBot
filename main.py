import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

default_intents = discord.Intents.default()
default_intents.members = True  # Vous devez activer les intents dans les paramètres du Bot
bot = commands.Bot(command_prefix="!", intents=default_intents, description="Bot")


@bot.event
async def on_ready():
    print("Le bot est connecté.")


bot.run(os.getenv("TOKEN"))
