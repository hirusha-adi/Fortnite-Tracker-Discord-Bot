import json
import os

import discord
import requests
import platform
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont


class Config:
    with open(os.path.join(os.getcwd(), 'config.json')) as _config_file:
        _data = json.load(_config_file)
    TOKEN = _data['TOKEN']
    PREFIX = _data['PREFIX']


client = commands.Bot(command_prefix=Config.PREFIX)


class Base(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.client.remove_command('help')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Python version: {platform.python_version()}')
        print(f'Discord.py API version: {discord.__version__}')
        print(f'Logged in as {self.client.user} | {self.client.user.id}')

    @commands.command()
    async def help(self, ctx):
        description = ""
        description += f'`{Config.PREFIX}help` **->** *Display bot help*'
        description += f'`{Config.PREFIX}fortnite/fn <username>` **->** *Display profile info*'

        embed = discord.Embed(title=f"Help for {self.client.user.name}",
                              description=description,
                              color=0x318ee5)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/858364751511814194/1014142976978604152/unknown.png")
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        embed.set_author(name=str(self.client.user.name),
                         icon_url=str(self.client.user.avatar_url))
        await ctx.send(embed=embed)


class Fortnite(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.base_path = os.getcwd()

    @commands.command(aliases=["fn"])
    async def fortnite(self, ctx, *args):
        loading_message = await ctx.send("Please Wait!...")
        try:
            username = list(args)
            format_player_name = '%20'.join(username)

            try:
                request_url = f'https://fortnite-api.com/v1/stats/br/v2?name={format_player_name}'
                fortnite_response = json.loads(requests.get(
                    request_url, params={'displayName': username}).content)
            except Exception as e:
                try:
                    await loading_message.delete()
                except:
                    pass
                await ctx.send(f"Unable to get information: {e}")
                return

            if fortnite_response['status'] == 200:
                # Images
                fortnite_template_image = Image.open(
                    os.path.join(self.base_path, 'assets', 'fortnite_template.png'))

                # Fonts
                username_font = ImageFont.truetype(
                    os.path.join(self.base_path, 'assets', 'theboldfont.ttf'), 50)
                stats_font = ImageFont.truetype(
                    os.path.join(self.base_path, 'assets', 'theboldfont.ttf'), 40)

                # Positions
                username_position = 135, 163

                # Overall stats
                overall_wins_position = 43, 300
                overall_win_rate_position = 155, 300
                overall_kd_position = 285, 300
                overall_kpm_position = 400, 300
                overall_matches_position = 63, 450
                overall_kills_position = 210, 450
                overall_deaths_position = 350, 450

                # Solo stats
                solo_matches_position = 540, 130
                solo_wins_position = 685, 130
                solo_win_rate_position = 795, 130
                solo_kills_position = 910, 130
                solo_deaths_position = 1050, 130
                solo_kd_position = 1170, 130
                solo_kpm_position = 1270, 130

                # Duo stats
                duo_matches_position = 540, 345
                duo_wins_position = 685, 345
                duo_win_rate_position = 795, 345
                duo_kills_position = 910, 345
                duo_deaths_position = 1050, 345
                duo_kd_position = 1170, 345
                duo_kpm_position = 1270, 345

                # Squad stats
                squad_matches_position = 540, 560
                squad_wins_position = 685, 560
                squad_win_rate_position = 795, 560
                squad_kills_position = 910, 560
                squad_deaths_position = 1050, 560
                squad_kd_position = 1170, 560
                squad_kpm_position = 1270, 560

                # Draws
                draw_on_image = ImageDraw.Draw(fortnite_template_image)

                # Username
                draw_on_image.text(username_position, fortnite_response['data']['account']['name'], 'white',
                                   font=username_font)

                # Overall stats
                if fortnite_response['data']['stats']['all']['overall'] is not None:
                    draw_on_image.text(overall_wins_position,
                                       str(fortnite_response['data']['stats']
                                           ['all']['overall']['wins']),
                                       'white', font=stats_font)
                    draw_on_image.text(overall_win_rate_position,
                                       str(round(
                                           fortnite_response['data']['stats']['all']['overall']['winRate'], 2)),
                                       'white', font=stats_font)
                    draw_on_image.text(overall_kd_position,
                                       str(round(
                                           fortnite_response['data']['stats']['all']['overall']['kd'], 2)),
                                       'white', font=stats_font)
                    draw_on_image.text(overall_kpm_position,
                                       str(round(
                                           fortnite_response['data']['stats']['all']['overall']['killsPerMatch'], 2)),
                                       'white', font=stats_font)
                    draw_on_image.text(overall_matches_position,
                                       str(fortnite_response['data']['stats']
                                           ['all']['overall']['matches']),
                                       'white', font=stats_font)
                    draw_on_image.text(overall_kills_position,
                                       str(fortnite_response['data']['stats']
                                           ['all']['overall']['kills']),
                                       'white', font=stats_font)
                    draw_on_image.text(overall_deaths_position,
                                       str(fortnite_response['data']['stats']
                                           ['all']['overall']['deaths']),
                                       'white', font=stats_font)

                # Solo stats
                if fortnite_response['data']['stats']['all']['solo'] is not None:
                    draw_on_image.text(duo_matches_position,
                                       str(fortnite_response['data']['stats']
                                           ['all']['solo']['matches']),
                                       'white', font=stats_font)
                    draw_on_image.text(duo_wins_position, str(fortnite_response['data']['stats']['all']['solo']['wins']),
                                       'white', font=stats_font)
                    draw_on_image.text(duo_win_rate_position,
                                       str(round(
                                           fortnite_response['data']['stats']['all']['solo']['winRate'], 2)),
                                       'white', font=stats_font)
                    draw_on_image.text(duo_kills_position,
                                       str(fortnite_response['data']
                                           ['stats']['all']['solo']['kills']),
                                       'white', font=stats_font)
                    draw_on_image.text(duo_deaths_position,
                                       str(fortnite_response['data']
                                           ['stats']['all']['solo']['deaths']),
                                       'white', font=stats_font)
                    draw_on_image.text(duo_kd_position,
                                       str(round(
                                           fortnite_response['data']['stats']['all']['solo']['kd'], 2)),
                                       'white', font=stats_font)
                    draw_on_image.text(duo_kpm_position,
                                       str(round(
                                           fortnite_response['data']['stats']['all']['solo']['killsPerMatch'], 2)),
                                       'white', font=stats_font)

                # Duo stats
                if fortnite_response['data']['stats']['all']['duo'] is not None:
                    draw_on_image.text(solo_matches_position,
                                       str(fortnite_response['data']
                                           ['stats']['all']['duo']['matches']),
                                       'white', font=stats_font)
                    draw_on_image.text(solo_wins_position, str(fortnite_response['data']['stats']['all']['duo']['wins']),
                                       'white', font=stats_font)
                    draw_on_image.text(solo_win_rate_position,
                                       str(round(
                                           fortnite_response['data']['stats']['all']['duo']['winRate'], 2)),
                                       'white', font=stats_font)
                    draw_on_image.text(solo_kills_position,
                                       str(fortnite_response['data']
                                           ['stats']['all']['duo']['kills']),
                                       'white', font=stats_font)
                    draw_on_image.text(solo_deaths_position,
                                       str(fortnite_response['data']
                                           ['stats']['all']['duo']['deaths']),
                                       'white', font=stats_font)
                    draw_on_image.text(solo_kd_position,
                                       str(round(
                                           fortnite_response['data']['stats']['all']['duo']['kd'], 2)),
                                       'white', font=stats_font)
                    draw_on_image.text(solo_kpm_position,
                                       str(round(
                                           fortnite_response['data']['stats']['all']['duo']['killsPerMatch'], 2)),
                                       'white', font=stats_font)

                # Squad stats
                if fortnite_response['data']['stats']['all']['squad'] is not None:
                    draw_on_image.text(squad_matches_position,
                                       str(fortnite_response['data']['stats']
                                           ['all']['squad']['matches']),
                                       'white', font=stats_font)
                    draw_on_image.text(squad_wins_position, str(fortnite_response['data']['stats']['all']['squad']['wins']),
                                       'white', font=stats_font)
                    draw_on_image.text(squad_win_rate_position,
                                       str(round(
                                           fortnite_response['data']['stats']['all']['squad']['winRate'], 2)),
                                       'white', font=stats_font)
                    draw_on_image.text(squad_kills_position,
                                       str(fortnite_response['data']
                                           ['stats']['all']['squad']['kills']),
                                       'white', font=stats_font)
                    draw_on_image.text(squad_deaths_position,
                                       str(fortnite_response['data']['stats']
                                           ['all']['squad']['deaths']),
                                       'white', font=stats_font)
                    draw_on_image.text(squad_kd_position,
                                       str(round(
                                           fortnite_response['data']['stats']['all']['squad']['kd'], 2)),
                                       'white', font=stats_font)
                    draw_on_image.text(squad_kpm_position,
                                       str(round(
                                           fortnite_response['data']['stats']['all']['squad']['killsPerMatch'], 2)),
                                       'white', font=stats_font)

                # Save image
                fortnite_template_image.convert(
                    'RGB').save('fortnite.jpg', 'JPEG')

                try:
                    await loading_message.delete()
                except:
                    pass
                await ctx.send(file=discord.File('fortnite.jpg'))

            else:
                try:
                    await loading_message.delete()
                except:
                    pass
                await ctx.send(f":no_entry: **{fortnite_response['error']}**")

        except Exception as e:
            embed3 = discord.Embed(title="ERROR!",
                                   description="An error has occured", color=0x318ee5)
            embed3.set_author(name=str(self.client.user.name),
                              icon_url=str(self.client.user.avatar_url))
            embed3.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/858364751511814194/1014140654848331856/unknown.png")
            embed3.add_field(name="Error:", value=f"{e}", inline=False)
            embed3.set_footer(text=f"Requested by {ctx.author.name}")
            await loading_message.delete()
            await ctx.send(embed=embed3)

        finally:
            try:
                os.remove("fortnite.jpg")
            except:
                os.system("rm -rf fortnite.jpg")


client.add_cog(Base(client))
client.add_cog(Fortnite(client))

client.run(Config.TOKEN)
