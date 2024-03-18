from dotenv import load_dotenv
from scrape_utils import *
from misc_utils import *
import datetime
import pytz
from discord.ext import commands, tasks
import os
from discord import *
from gcp_proxy import *

load_dotenv()
# STEP 1: BOT SETUP
intents=Intents().all()

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    look_for_update.start()

@bot.command()
async def p(ctx):
    await ctx.send("any updates are now provided automatically")

@tasks.loop(minutes=5)
async def look_for_update():
    blob = get_most_recent_blob('plays-bucket', 'google-credentials.json')
    minutes_since_update = int((datetime.datetime.now(pytz.UTC) - blob.time_created).total_seconds() / 60)
    print(minutes_since_update)
    if(minutes_since_update < 5):
        await post_most_recent_lines(blob, minutes_since_update)

async def post_most_recent_lines(blob, minutes):
    all_lines = blob.download_as_text()
    embed = Embed(
        color = Colour.dark_purple(),
        description=all_lines
    )
    embed.set_author(name="Plays of the Hour", icon_url='https://s3.us-west-1.amazonaws.com/redwood-labs/showpage/uploads/images/e9c2fa72-aee2-4782-9d90-e7113cad3424.png')
    embed.set_footer(text = f'Last updated {minutes} minutes ago')
    for curr_guild in bot.guilds:
        # sports betting channel
        channel = utils.get(curr_guild.channels, name="sports-betting")
        if(contains_lock(all_lines)):
            try:
                role = utils.get(curr_guild.roles,name="gamblers")
                await channel.send(f'{role.mention}')
            except:
                print("role not found")
        else:
            print("does not contain lock")
        await channel.send(embed=embed)

disc_token = os.getenv("DISCORD_TOKEN")
bot.run(token=disc_token)