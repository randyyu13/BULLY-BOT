from dotenv import load_dotenv
from scrape_utils import *
from misc_utils import *
import datetime
import pytz
from discord.ext import commands
import os
from discord import *
import discord
from gcp_proxy import *

load_dotenv()
# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

bot = commands.Bot(command_prefix='$', intents=intents)

def file_exists(filename):
    return os.path.isfile(filename)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Command to make the bot say hello world
@bot.command()
async def p(ctx):
    try:
        blob = get_most_recent_blob('plays-bucket', 'google-credentials.json')
        
        embed = Embed(
            color = discord.Colour.dark_purple(),
            description=blob.download_as_text()
        )
        embed.set_author(name="Plays of the Hour", icon_url='https://s3.us-west-1.amazonaws.com/redwood-labs/showpage/uploads/images/e9c2fa72-aee2-4782-9d90-e7113cad3424.png')
        embed.set_footer(text = f'Last updated {int((datetime.datetime.now(pytz.UTC) - blob.time_created).total_seconds() / 60)} minutes ago')
        await ctx.send(embed=embed)
    except FileNotFoundError:
        print(f'no files in bucket')


disc_token = os.getenv("DISCORD_TOKEN")
print(disc_token)
bot.run(token=disc_token)