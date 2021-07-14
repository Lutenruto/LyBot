import discord
from discord.ext import commands
import asyncio
import random


def setup(bot):
    bot.add_cog(CogOther(bot))


class CogOther(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Transforme ce que vous dite en caractère "style chinois"
    @commands.command(name="chinese")
    async def chinese(self, ctx, *text):
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
    @commands.command(name="cuisiner")
    async def cook(self, ctx):
        await ctx.send("Envoyez le plat que vous voulez cuisiner")

        def check_message(msg):
            return msg.author == ctx.message.author and ctx.message.channel == msg.channel

        try:
            recette = await self.bot.wait_for("message", timeout=10, check=check_message)
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
            reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=check_emoji)
            if reaction.emoji == "✅":
                await ctx.send("La recette a démarré.")
            else:
                await ctx.send("La recette a bien été annulé.")
        except:
            await ctx.send("La recette a bien été annulé.")

    # Jeu de la roulette qui donne au hasard une "punition" au perdant
    @commands.command(name="roulette")
    async def roulette(self, ctx):
        await ctx.send("La roulette commencera dans 10 secondes. Envoyez \"moi\" dans ce channel pour y participer.")
        players = []

        def check(message):
            return message.channel == ctx.message.channel and message.author not in players and message.content == "moi"

        try:
            while True:
                participation = await self.bot.wait_for('message', timeout=10, check=check)
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
    @commands.command(name="infoServ")
    async def server_info(self, ctx):
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

    # Dis bonjour
    @commands.command(name="bonjour")
    async def say_hello(self, ctx):
        server_name = ctx.guild.name
        message_fr = f"Bonjour jeune *Padawan* ! Savais-tu que tu te trouvais dans le serveur *{server_name}*, c'est d'ailleurs un super serveur puisque **JE** suis dedans."
        message_en = f"Hello young *Padawan*! Did you know that you were in the *{server_name}* server, it's a great server because **I**'m in it."
        await ctx.send(message_fr)

    @commands.command(name="say")
    async def repeat(self, ctx, *text):
        await ctx.send(" ".join(text))

    # Compte le nombre de message dans le channel
    @commands.command(name="count")
    async def message_count(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        count = 0
        async for _ in channel.history(limit=None):
            count += 1
        await ctx.send(f"There were {count + 1} messages in {channel.mention}")
