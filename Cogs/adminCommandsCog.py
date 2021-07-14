import discord
from discord.ext import commands
import random


def setup(bot):
    bot.add_cog(CogAdminCommands(bot))


def isPair(ctx):
    return ctx.message.author.id % 2 == 0


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


class CogAdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Donne les infos du serveur
    @commands.command(name="getInfo")
    @commands.has_permissions(manage_messages=True)
    async def server_info(self, ctx, info):
        server = ctx.guild
        if info == "memberCount":
            await ctx.send(server.member_count)
        elif info == "numberOfChannel":
            await ctx.send(len(server.voice_channels) + len(server.text_channels))
        elif info == "name":
            await ctx.send(server.name)
        else:
            await ctx.send("Etrange... je ne connais pas cela")

    @commands.command(name="pair")
    @commands.check(isPair)
    @commands.has_permissions(manage_messages=True)
    async def pair(self, ctx):
        await ctx.send("Vous remplissez toute les conditions !")

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
        mutedRole = await getMutedRole(ctx)
        await member.add_roles(mutedRole, reason=reason)
        await ctx.send(f"{member.mention} a été mute !")

    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
        mutedRole = await getMutedRole(ctx)
        await member.remove_roles(mutedRole, reason=reason)
        await ctx.send(f"{member.mention} a été unmute !")

    @commands.command(name="bansId")
    @commands.has_permissions(ban_members=True)
    async def bans_id(self, ctx):
        ids = []
        bans = await ctx.guild.bans()
        for i in bans:
            ids.append(str(i.user.id))
        await ctx.send("La liste des id utilisateurs bannis du serveur est :")
        if len(ids) < 1:
            await ctx.send("Vide")
        else:
            await ctx.send("\n".join(ids))

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User, *, reason="Aucune raison n'a été donné"):

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

        await ctx.guild.ban(user, reason=reason)
        embed = discord.Embed(title="**Banissement**", description="Un modérateur a frappé !", url="https://github.com/Lutenruto/Lybot", color=0xCE453E)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://emoji.gg/assets/emoji/BanHammer.png")
        embed.add_field(name="Membre banni", value=user.name, inline=True)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.set_footer(text=random.choice(funFact))

        await ctx.send(embed=embed)

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user, *reason):
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

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.User, *reason):
        reason = " ".join(reason)
        await ctx.guild.kick(user, reason=reason)
        await ctx.send(f"{user} a été kick.")

    @commands.command(name="del")
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, number: int, channel: discord.TextChannel = None):
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
