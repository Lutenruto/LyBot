import discord
from discord.ext import commands
from datetime import datetime, date
import re
import requests


def setup(bot):
    bot.add_cog(CogCovid(bot))


async def covid_traitment(ctx, app_count, nom_labo, address_labo, next_rdv, url, vt):
    if app_count > 0:
        embed = discord.Embed(title="Doses disponibles...", description="", url="https://github.com/Lutenruto/", color=0xc03537)
        embed.set_author(name=ctx.author.name,
                         icon_url=ctx.author.avatar_url,
                         url="https://github.com/Lutenruto/")
        embed.set_thumbnail(url="https://nsa40.casimages.com/img/2021/07/14/210714035657987298.png")
        embed.add_field(name=f"{nom_labo}",
                        value=f"Adresse : https://www.google.com/maps/search/{address_labo.replace(' ', '+')}\n"
                              f"Il y a **{app_count}** créneaux disponibles.\n"
                              f"Le prochain rdv est disponible le : **{next_rdv}**\n"
                              f"URL : {url}\n"
                              f"Type de vaccin : **{vt}**\n"
                        , inline=False)

        embed.set_footer(text="Pour plus d'information, contacter Lutenruto")

        await ctx.send(embed=embed)


def good_channel(ctx):
    return ctx.message.channel.id == 864688091125383168


class CogCovid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rdvCovid")
    @commands.check(good_channel)
    async def rdv_covid(self, ctx, department, *, vac_type=""):
        cp = ""
        vac_present = False
        vaccines = ["AstraZeneca", "Janssen", "Pfizer-BioNTech", "Moderna", "CureVac", "ARNm"]
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
            try:
                code_postal = centre.get("location", []).get("cp", [])
            except:
                code_postal = cp
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