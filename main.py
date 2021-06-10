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


@bot.event
async def on_member_join(member):
    general_channel: discord.TextChannel = bot.get_channel(852227347800784917)
    await general_channel.send(content=f"Bienvenue sur le Serveur {member.display_name}.")


@bot.event
async def on_message(message):
    general_channel: discord.TextChannel = bot.get_channel(message.channel.id)
    if message.content.lower() == "ping":
        await general_channel.send(content=f"pong")
    await bot.process_commands(message)


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


@bot.command(name="commands")
async def command_display(ctx):
    await ctx.send(
        "**!count** => To count the number of messages in the channel\n"
        "**!infoServ** => Shows basic server information\n"
        "**!bonjour** => Hello from the bot\n"
        "**!say** => Repeats what you write after this command\n"
        "**!chinese** => Repeats in Chinese style character, what you write after this command\n"
        "**!cuisiner** => Fill in the order form and follow the instructions\n"
        "**!del** => To delete a number of messages``` example : !del 5```"
        "**!getInfo** => Display information about the server based on one of these arguments :``` memberCount\n numberOfChannel\n name```"
        "**!bansId** => Displays the list of user ids banned from the server\n"
        "**!ban** => Allows you to ban a user by identifying him or her and with the possibility of entering a reason``` example : !ban @titou because it's boring```"
        "**!unban** => Allows you to unban a user by identifying them with their nickname and # with the possibility of entering a reason``` example : !unban Titou#4523 Error```"
        "**!kick** => Allows you to kick out a person by identifying them with the possibility of entering a reason``` example : !kick @titou```"
        "")


@bot.command(name="chinese")
async def chinese(ctx, *text):
    chinese_char = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
    chinese_text = []
    ref = ""
    for word in text:
        for char in word:
            if char.isalpha():
                if 65 <= ord(char) <= 90:
                    ref = "A"
                if 97 <= ord(char) <= 122:
                    ref = "a"
                index = ord(char) - ord(ref)
                transformed = chinese_char[index]
                chinese_text.append(transformed)
            else:
                chinese_text.append(char)
        chinese_text.append("  ")
    await ctx.send("".join(chinese_text))


@bot.command(name="cuisiner")
async def cook(ctx):
    await ctx.send("Envoyez le plat que vous voulez cuisiner")

    def check_message(msg):
        return msg.author == ctx.message.author and ctx.message.channel == msg.channel

    try:
        recette = await bot.wait_for("message", timeout=10, check=check_message)
    except:
        return

    message = await ctx.send(f"La préparation de {recette.content} va commencer. Veuillez valider en réagissant avec ✅. Sinon réagissez avec ❌.")
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    # ✅
    # ❌

    def check_emoji(reaction, user):
        return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=10, check=check_emoji)
        if reaction.emoji == "✅":
            await ctx.send("La recette a démarré")
        else:
            await ctx.send("La recette a bien été annulé")
    except:
        await ctx.send("La recette a bien été annulé")


@bot.command(name="infoServ")
async def server_info(ctx):
    server = ctx.guild
    number_of_text_channels = len(server.text_channels)
    number_of_voice_channels = len(server.voice_channels)
    server_description = server.description
    if server_description is None:
        server_description = "**vide**"
    number_of_person = server.member_count
    server_name = server.name
    message = f"Le serveur **{server_name}** contient *{number_of_person}* personnes. \n" \
              f"La description du serveur est *{server_description}*. \n" \
              f"Ce serveur possède {number_of_text_channels} salons de texte ainsi que {number_of_voice_channels} salons vocaux."
    await ctx.send(message)


@bot.command(name="getInfo")
async def server_info(ctx, info):
    server = ctx.guild
    if info == "memberCount":
        await ctx.send(server.member_count)
    elif info == "numberOfChannel":
        await ctx.send(len(server.voice_channels) + len(server.text_channels))
    elif info == "name":
        await ctx.send(server.name)
    else:
        await ctx.send("Etrange... je ne connais pas cela")


@bot.command(name="bonjour")
async def say_hello(ctx):
    server_name = ctx.guild.name
    message_fr = f"Bonjour jeune *Padawan* ! Savais-tu que tu te trouvais dans le serveur *{server_name}*, c'est d'ailleurs un super serveur puisque **JE** suis dedans."
    message_en = f"Hello young *Padawan*! Did you know that you were in the *{server_name}* server, it's a great server because **I**'m in it."
    await ctx.send(message_fr)


@bot.command(name="say")
async def repeat(ctx, *text):
    await ctx.send(" ".join(text))


@bot.command(name="bansId")
@commands.has_permissions(manage_messages=True)
async def bans_id(ctx):
    ids = []
    bans = await ctx.guild.bans()
    for i in bans:
        ids.append(str(i.user.id))
    await ctx.send("La liste des id utilisateurs bannis du serveur est :")
    if len(ids) < 1:
        await ctx.send("Vide")
    else:
        await ctx.send("\n".join(ids))


@bot.command(name="ban")
@commands.has_permissions(manage_messages=True)
async def ban(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason=reason)
    await ctx.send(f"{user} a été ban pour la raison suivante : {reason}.")


@bot.command(name="unban")
@commands.has_permissions(manage_messages=True)
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    user_name, user_id = user.split("#")
    banned_users = await ctx.guild.bans()
    for i in banned_users:
        if i.user.name == user_name and i.user.discriminator == user_id:
            await ctx.guild.unban(i.user, reason=reason)
            await ctx.send(f"{user} a été unban.")
            return
    await ctx.send(f"L'utilisateur {user} n'est pas dans la liste de bans.")


@bot.command(name="kick")
@commands.has_permissions(manage_messages=True)
async def kick(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason=reason)
    await ctx.send(f"{user} a été kick.")


@bot.command(name="count")
async def message_count(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    count = 0
    async for _ in channel.history(limit=None):
        count += 1
    await ctx.send(f"There were {count + 1} messages in {channel.mention}")
    # await ctx.send("There were {} messages in {}".format(count + 1, channel.mention))


def good_channel(ctx):
    return ctx.message.channel.id == 852291128484298802


@bot.command(name="del")
@commands.has_permissions(manage_messages=True)
# @commands.check(good_channel)
async def delete(ctx, number: int, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    count = 0

    if type(number) == int:
        async for _ in channel.history(limit=None):
            count += 1

        if (count - number + 1) < 0:
            messages = await ctx.channel.history(limit=count).flatten()

            for each_message in messages:
                await each_message.delete()

            await channel.send(content="There were {} messages in {} deleted".format(count, channel.mention), delete_after=5)
        else:
            messages = await ctx.channel.history(limit=number + 1).flatten()

            for each_message in messages:
                await each_message.delete()

            await channel.send(content="There were {} messages in {} deleted".format(number + 1, channel.mention), delete_after=5)
    else:
        await channel.send(content="You must enter a number")


# @delete.error
# async def delete_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send("You must be enter a number (example : !del 5)")


bot.run(os.getenv("TOKEN"))
