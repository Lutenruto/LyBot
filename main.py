import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

default_intents = discord.Intents.default()
default_intents.members = True  # Vous devez activer les intents dans les paramètres du Bot
bot = commands.Bot(command_prefix="!", intents=default_intents, description="Bot de Lutenruto")


@bot.event
async def on_ready():
    print("Le bot est connecté.")


# Petit message lorsqu'un membre rejoins le serveur
@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(852227347800784917)
    embed = discord.Embed(title="**Bienvenue !**", description="", url="https://github.com/Lutenruto/Lybot",
                          color=0x407294)
    embed.set_author(name=member.display_name,
                     icon_url=member.avatar_url,
                     url="https://github.com/Lutenruto/")
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/6721_AB_welcome.png")
    embed.add_field(name=f"Accueillons à bras ouvert",
                    value=""
                          f"{member.mention} !\n"
                          "Bienvenue dans ce magnifique serveur 😁\n"
                          "---------------------------------------------------------------"
                    , inline=False)

    embed.set_footer(text="Pour plus d'information, contacter Lutenruto")

    await channel.send(embed=embed)


# Petit message lorsqu'un membre du serveur part
@bot.event
async def on_member_remove(member):
    banned_users = await member.guild.bans()
    for i in banned_users:
        if i.user.discriminator == member.discriminator:
            return
    channel = member.guild.get_channel(852227347800784917)
    embed = discord.Embed(title="**Au revoir !**", description="", url="https://github.com/Lutenruto/Lybot",
                          color=0x008080)
    embed.set_author(name=member.display_name,
                     icon_url=member.avatar_url,
                     url="https://github.com/Lutenruto/")
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/7242_bye_bean.png")
    embed.add_field(name="En cette belle journée nous déplorons la perte d'un membre bien aimé,",
                    value=""
                          f"{member.mention}\n"
                          "---------------------------------------------------------------"
                    , inline=False)

    embed.set_footer(text="Pour plus d'information, contacter Lutenruto")

    await channel.send(embed=embed)


@bot.event
async def on_message(message):
    general_channel: discord.TextChannel = bot.get_channel(message.channel.id)
    if message.content.lower() == "ping":
        await general_channel.send(content=f"pong")
    await bot.process_commands(message)


# Gère les erreurs
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Mmmmmmmmh, I think this command does not exist. :thinking:")
        # await ctx.send("This command do not exist.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("One argument is missing.")
    elif isinstance(error, commands.MissingPermissions):
        messages = await ctx.channel.history(limit=1).flatten()
        for each_message in messages:
            await each_message.delete()
        await ctx.send(f"You do not have the permission to run this command. {ctx.message.author.mention}", delete_after=10)
    elif isinstance(error, commands.CheckFailure):
        messages = await ctx.channel.history(limit=1).flatten()
        for each_message in messages:
            await each_message.delete()
        await ctx.send(f"Oops, you can't use this command. {ctx.message.author.mention}", delete_after=10)
    elif isinstance(error.original, discord.Forbidden):
        await ctx.send("Oops, I don't have the required permissions to run this command.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Oops, I don't have the required permissions to run this command.")
    else:
        print(error)


@bot.command(name="load")
@commands.has_permissions(manage_messages=True)
async def load(ctx, name=None):
    if name:
        bot.load_extension(f'Cogs.{name}')


@bot.command(name="unload")
@commands.has_permissions(manage_messages=True)
async def unload(ctx, name=None):
    if name:
        bot.unload_extension(f'Cogs.{name}')


@bot.command(name="reload")
@commands.has_permissions(manage_messages=True)
async def reload(ctx, name=None):
    if name:
        try:
            bot.reload_extension(f'Cogs.{name}')
        except:
            bot.load_extension(f'Cogs.{name}')


@bot.command(name="loadAll")
@commands.has_permissions(manage_messages=True)
async def loadAll(ctx):
    try:
        for fileCog in os.listdir("./Cogs"):
            if fileCog.endswith(".py"):
                bot.load_extension(f'Cogs.{fileCog[:-3]}')
    except:
        for fileCog in os.listdir("./Cogs"):
            if fileCog.endswith(".py"):
                bot.reload_extension(f'Cogs.{fileCog[:-3]}')


bot.run(os.getenv("TOKEN"))
