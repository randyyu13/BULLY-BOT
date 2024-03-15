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
async def P(ctx):
    try:
        file_content = get_string_from_most_recent_blob('plays-bucket', 'google-credentials.json')
        
        embed = Embed(
            title='Plays of the Hour',
            color = discord.Colour.dark_purple(),
            description=file_content
        )
        await ctx.send(embed=embed)
    except FileNotFoundError:
        print(f'no files in bucket')


disc_token = os.getenv("DISCORD_TOKEN")
print(disc_token)
bot.run(token=disc_token)