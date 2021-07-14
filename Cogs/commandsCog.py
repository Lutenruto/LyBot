import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(CogDispCommands(bot))


class CogDispCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Affiche les commandes que tout le monde peut faire
    @commands.command(name="commands")
    async def command_display(self, ctx):
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
                              "**!pair** => Allows you to check if your ID is even and that you have the necessary rights on this discord\n"
                              "**!infoServ** => Shows basic server information\n"
                              "**!rdvCovid** => Displays appointments according to your criteria\n"
                              "```example : "
                              "!rdvCovid 75 Pfizer\n"
                              "!rdvCovid 75005 Astra\n"
                              "Type of vaccin : AstraZeneca, Janssen,\nPfizer-BioNTech, Moderna, CureVac, ARNm"
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
    @commands.command(name="commandsAdmin")
    async def commandAdmin(self, ctx):
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
        embed.add_field(name="Cog Commands",
                        value=""
                              "**!load** => Loads a cog file where there are features\n"
                              "```example : !load myCogFile```\n"
                              "**!unload** => Unloads a cog file where there are features\n"
                              "```example : !unload myCogFile```\n"
                              "**!reload** => Reloads a cog file where there are features\n"
                              "```example : !reload myCogFile```\n"
                              "**!loadAll** => Loads all cogs files where there are features\n"
                              "```example : !loadAll```\n"
                        , inline=False)

        embed.set_footer(text="Pour plus d'information, contacter Lutenruto")

        await ctx.send(embed=embed)
