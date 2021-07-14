import os

import discord
from discord.ext import commands
from binance.client import Client, BinanceAPIException
from datetime import datetime


def setup(bot):
    bot.add_cog(CogBinance(bot))


class CogBinance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="getPrice")
    async def get_price(self, ctx, assets):
        BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
        BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
        binanceC = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

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
