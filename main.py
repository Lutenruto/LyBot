import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import random
import youtube_dl
from binance.client import Client, BinanceAPIException
from datetime import datetime, date
import re
import requests

load_dotenv(dotenv_path="config")

default_intents = discord.Intents.default()
default_intents.members = True  # Vous devez activer les intents dans les paramètres du Bot
bot = commands.Bot(command_prefix="!", intents=default_intents, description="Bot de Lutenruto")

musics = {}
ytdl = youtube_dl.YoutubeDL()

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')

binanceC = Client(BINANCE_API_KEY, BINANCE_API_SECRET)


@bot.command(name="getPrice")
async def get_price(ctx, assets):
    assets = assets.upper()
    assets2 = assets.split("/")

    try:
        assets_details = binanceC.get_ticker(symbol=f"{assets2[0] + assets2[1]}")
        embed = discord.Embed(title=f"Current price of {assets}", description="", url="https://github.com/Lutenruto/Lybot",
                              color=0xf7c318)
        embed.set_thumbnail(url="https://nsa40.casimages.com/img/2021/07/07/210707102651269549.png")
        embed.add_field(name="\u200b", value=""
                                             f"**CURRENT:** {format(float(assets_details['lastPrice']), '.2f')}\n"
                                             f"**OPEN:** {format(float(assets_details['openPrice']), '.2f')}\n\n"
                                             f"**PERCENTAGE CHANGE:** {format(float(assets_details['priceChangePercent']), '.2f')}\n\n"
                                             f"**HIGH:** {format(float(assets_details['highPrice']), '.2f')}\n"
                                             f"**LOW:** {format(float(assets_details['lowPrice']), '.2f')}\n\n"
                                             f"**{assets2[0]} VOLUME:** {format(float(assets_details['volume']), '.2f')}\n"
                                             f"**{assets2[1]} VOLUME:** {format(float(assets_details['quoteVolume']), '.2f')}\n"
                                             f"\u200b"
                        , inline=False)

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        embed.set_footer(text=dt_string)

        await ctx.send(embed=embed)
    except BinanceAPIException as e:
        await ctx.send("Oops, I think this combination is not available.")
        return


def good_channel(ctx):
    return ctx.message.channel.id == 864688813003112448


async def covid_traitment(ctx, app_count, nom_labo, address_labo, next_rdv, url, vt):
    if app_count > 0:

        embed = discord.Embed(title="Doses disponibles...", description="", url="https://github.com/Lutenruto/", color=0x24D2B5)
        embed.set_author(name=ctx.author.name,
                         icon_url=ctx.author.avatar_url,
                         url="https://github.com/Lutenruto/")
        embed.set_thumbnail(url="https://nsa40.casimages.com/img/2021/07/14/210714035657987298.png")
        embed.add_field(name="Voici le résultat des recherches",
                        value=f"A {nom_labo}, à l'adresse : https://www.google.com/maps/search/{address_labo.replace(' ', '+')}\n"
                              f"il y a {app_count} créneaux disponibles.\n"
                              f"Le prochain rdv est disponible le : {next_rdv}\n"
                              f"Voici l'url : {url}\n"
                              f"Type de vaccin : {vt}\n"
                        , inline=False)

        embed.set_footer(text="Pour plus d'information, contacter Lutenruto")

        await ctx.send(embed=embed)


@bot.command(name="rdvCovid")
@commands.check(good_channel)
async def rdv_covid(ctx, department, *, vac_type=""):
    cp = ""
    vac_present = False
    vaccines = ["AstraZeneca", "Janssen", "Pfizer-BioNTech", "Moderna", "CureVac"]
    if len(vac_type) > 0:
        for vac in vaccines:
            if vac_type in vac:
                vac_present = True
                vac_type = vac

    lesJours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    if len(department) > 2:
        cp = department
        department = department[0] + department[1]

    r = requests.get(f"https://vitemadose.gitlab.io/vitemadose/{department}.json")
    centres_disponibles = r.json().get("centres_disponibles", [])

    for centre in centres_disponibles:
        url = centre.get("url")
        app_count = centre.get("appointment_count", [])
        nom_labo = centre.get("nom", [])
        address_labo = centre.get("metadata", []).get("address", [])
        code_postal = centre.get("location", []).get("cp", [])
        vaccine_type = centre.get("vaccine_type", [])

        prochain_rdv = centre.get("prochain_rdv", [])
        dt = re.split("[T.-]", prochain_rdv)
        dt = (dt[2] + "/" + dt[1] + "/" + dt[0] + " " + dt[3]).split("+")[0]
        dto = datetime.strptime(dt, "%d/%m/%Y %H:%M:%S")
        next_rdv = dto.strftime(f"{lesJours[date.weekday(dto)]} %d %B à %H:%M")

        if len(cp) > 0 and len(cp) == 2:
            if code_postal != cp:
                continue
            if vac_present:
                for vac_t in vaccine_type:
                    if vac_t != vac_type:
                        continue
                    await covid_traitment(ctx, app_count, nom_labo, address_labo, next_rdv, url, vac_t)
            else:
                await covid_traitment(ctx, app_count, nom_labo, address_labo, next_rdv, url, vaccine_type)
        else:
            if vac_present:
                for vac_t in vaccine_type:
                    if vac_t != vac_type:
                        continue
                    await covid_traitment(ctx, app_count, nom_labo, address_labo, next_rdv, url, vac_t)
            else:
                await covid_traitment(ctx, app_count, nom_labo, address_labo, next_rdv, url, vaccine_type)


class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]


@bot.command(name="leave")
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []


@bot.command(name="resume")
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()


@bot.command(name="pause")
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()


@bot.command(name="skip")
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()


def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
                                                                 , before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def nextS(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=nextS)


@bot.command(name="play")
async def play(ctx, url):
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"Je lance : {video.url}")
        play_song(client, musics[ctx.guild], video)


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


# Affiche les commandes que tout le monde peut faire
@bot.command(name="commands")
async def command_display(ctx):
    embed = discord.Embed(title="**Commandes**", description="", url="https://github.com/Lutenruto/Lybot", color=0x24D2B5)
    embed.set_author(name="Lutenruto",
                     icon_url="https://images-ext-2.discordapp.net/external/KdtU2ZNPyhoGKUCGwo6UQ_6h66wSEE0orYHP0UrpdAs/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/427165420735430657/a_6507de124459a18a4ac9ee24a798f586.gif",
                     url="https://github.com/Lutenruto/")
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/2277-command-block.png")
    embed.add_field(name="Voici la liste des commandes",
                    value=""
                          "**!count** => To count the number of messages in the channel\n"
                          "**!bonjour** => Hello from the bot\n"
                          "**!say** => Repeats what you write after this command\n"
                          "**!chinese** => Repeats in Chinese style character, what you write after this command\n"
                          "**!cuisiner** => Fill in the order form and follow the instructions\n"
                          "**!roulette** => Allows you to participate in a roulette game where you have a win at the end (ban, kick, ...)\n"
                          "**!infoServ** => Shows basic server information\n"
                          "**!rdvCovid** => Displays appointments according to your criteria\n"
                          "```example : "
                          "!rdvCovid 75 Pfizer\n"
                          "!rdvCovid 75005 Astra\n"
                          "Type of vaccin : AstraZeneca, Janssen,\nPfizer-BioNTech, Moderna, CureVac"
                          "```"
                          "**!getPrice** => Retrieve asset information from Binance\n"
                          "```example : !getPrice btc/usdt```"
                          "---------------------------------------------------------------"
                    , inline=False)
    embed.add_field(name="Commandes musique",
                    value=""
                          "**!play** => Starts the music or queues the music you want\n"
                          "```!play https://www.youtube.com/watch?v=QUrojMQPWQc```"
                          "**!pause** => Pause the current music\n"
                          "**!resume** => Plays the current music\n"
                          "**!skip** => Plays the next music in the queue\n"
                          "**!leave** => Leaves the bot, from the voice channel\n"
                          "---------------------------------------------------------------"
                    , inline=False)

    embed.set_footer(text="Pour plus d'information, contacter Lutenruto")

    await ctx.send(embed=embed)


# Affiche les commandes que seuls les admins peuvent faire
@bot.command(name="commandsAdmin")
async def commandAdmin(ctx):
    embed = discord.Embed(title="**Commandes d'Admin**", description="", url="https://github.com/Lutenruto/Lybot", color=0xC70039)
    embed.set_author(name="Lutenruto",
                     icon_url="https://images-ext-2.discordapp.net/external/KdtU2ZNPyhoGKUCGwo6UQ_6h66wSEE0orYHP0UrpdAs/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/427165420735430657/a_6507de124459a18a4ac9ee24a798f586.gif",
                     url="https://github.com/Lutenruto/")
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/1314-infinity-admin-power.gif")
    embed.add_field(name="Voici la liste des commandes",
                    value=""
                          "**!del** => To delete a number of messages\n"
                          "```example : !del 5```\n"
                          "**!getInfo** => Display information about the server based on one of these arguments :\n"
                          "```\n"
                          "memberCount\n"
                          "numberOfChannel\n"
                          "name```\n"
                          "**!bansId** => Displays the list of user ids banned from the server\n"
                          "**!ban** => Allows you to ban a user by identifying him or her and with the possibility of entering a reason\n"
                          "```example : !ban @titou because it's boring```\n"
                          "**!unban** => Allows you to unban a user by identifying them with their nickname and # with the possibility of entering a reason\n"
                          "```example : !unban Titou#4523 Error```\n"
                          "**!kick** => Allows you to kick out a person by identifying them with the possibility of entering a reason\n"
                          "```example : !kick @titou```\n"
                          "**!mute** => Allows you to add the Muted role to an user\n"
                          "```example : !mute @titou Because it's funny !```\n"
                          "**!unmute** => Allows you to remove the Muted role to an user\n"
                          "```example : !unmute @titou Because he's cool !```\n"
                    , inline=False)
    embed.set_footer(text="Pour plus d'information, contacter Lutenruto")

    await ctx.send(embed=embed)


# Dis bonjour
@bot.command(name="bonjour")
async def say_hello(ctx):
    server_name = ctx.guild.name
    message_fr = f"Bonjour jeune *Padawan* ! Savais-tu que tu te trouvais dans le serveur *{server_name}*, c'est d'ailleurs un super serveur puisque **JE** suis dedans."
    message_en = f"Hello young *Padawan*! Did you know that you were in the *{server_name}* server, it's a great server because **I**'m in it."
    await ctx.send(message_fr)


@bot.command(name="say")
async def repeat(ctx, *text):
    await ctx.send(" ".join(text))


# Transforme ce que vous dite en caractère "style chinois"
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


# Interaction avec le bot qui nous prépare un plat fictif
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
            await ctx.send("La recette a démarré.")
        else:
            await ctx.send("La recette a bien été annulé.")
    except:
        await ctx.send("La recette a bien été annulé.")


# Jeu de la roulette qui donne au hasard une "punition" au perdant
@bot.command(name="roulette")
async def roulette(ctx):
    await ctx.send("La roulette commencera dans 10 secondes. Envoyez \"moi\" dans ce channel pour y participer.")
    players = []

    def check(message):
        return message.channel == ctx.message.channel and message.author not in players and message.content == "moi"

    try:
        while True:
            participation = await bot.wait_for('message', timeout=10, check=check)
            players.append(participation.author)
            print("Nouveau participant : ")  # Log Console
            print(participation)  # Log Console
            await ctx.send(f"**{participation.author.name}** participe au tirage ! Le tirage commence dans 10 secondes")
    except:  # Timeout
        print("Demarrage du tirrage")  # Log Console

    gagner = ["ban", "kick", "rôle personnel", "mute", "gage"]

    await ctx.send("Le tirage va commencer dans 3...")
    await asyncio.sleep(1)
    await ctx.send("2")
    await asyncio.sleep(1)
    await ctx.send("1")
    await asyncio.sleep(1)
    loser = random.choice(players)
    price = random.choice(gagner)
    await ctx.send(f"La personne qui a gagnée un {price} est ...")
    await asyncio.sleep(1)
    await ctx.send(f"**{loser.name}** !")


# Donne quelques infos sur le serveur
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


# Donne les infos du serveur
@bot.command(name="getInfo")
@commands.has_permissions(manage_messages=True)
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


# Compte le nombre de message dans le channel
@bot.command(name="count")
async def message_count(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    count = 0
    async for _ in channel.history(limit=None):
        count += 1
    await ctx.send(f"There were {count + 1} messages in {channel.mention}")


async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name="Muted",
                                            permissions=discord.Permissions(
                                                send_messages=False,
                                                speak=False),
                                            reason="Creation du rôle Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages=False, speak=False)
    return mutedRole


async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    return await createMutedRole(ctx)


@bot.command(name="mute")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} a été mute !")


@bot.command(name="unmute")
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} a été unmute !")


@bot.command(name="bansId")
@commands.has_permissions(ban_members=True)
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


funFact = ["L'eau mouille",
           "Le feu brule",
           "Lorsque vous volez, vous ne touchez pas le sol",
           "Winter is coming", "Mon créateur est Titouan",
           "Il n'est pas possible d'aller dans l'espace en restant sur terre",
           "La terre est ronde",
           "La moitié de 2 est 1",
           "7 est un nombre heureux",
           "Les allemands viennent d'allemagne",
           "Le coronavirus est un virus se répandant en Europe, en avez vous entendu parler ?",
           "J'apparais 2 fois dans l'année, a la fin du matin et au début de la nuit, qui suis-je ?",
           "Le plus grand complot de l'humanité est",
           "Pourquoi lisez vous ca ?"]


@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.User, *, reason="Aucune raison n'a été donné"):
    await ctx.guild.ban(user, reason=reason)
    embed = discord.Embed(title="**Banissement**", description="Un modérateur a frappé !", url="https://github.com/Lutenruto/Lybot", color=0xCE453E)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/BanHammer.png")
    embed.add_field(name="Membre banni", value=user.name, inline=True)
    embed.add_field(name="Raison", value=reason, inline=True)
    embed.set_footer(text=random.choice(funFact))

    await ctx.send(embed=embed)


@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    user_name, user_id = user.split("#")
    banned_users = await ctx.guild.bans()
    for i in banned_users:
        if i.user.name == user_name and i.user.discriminator == user_id:
            await ctx.guild.unban(i.user, reason=reason)
            await ctx.send(f"{user} a été unban.")
            return
    # Ici on sait que l'utilisateur n'a pas été trouvé
    await ctx.send(f"L'utilisateur {user} n'est pas dans la liste de bans.")


@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason=reason)
    await ctx.send(f"{user} a été kick.")


@bot.command(name="del")
@commands.has_permissions(manage_messages=True)
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


bot.run(os.getenv("TOKEN"))
