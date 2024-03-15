from dotenv import load_dotenv
from scrape_utils import *
from misc_utils import *
import datetime
import pytz
from discord.ext import commands
import os
from discord import *
import discord

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
    current_datetime = datetime.datetime.now(pytz.UTC)
    timestamp_string = current_datetime.strftime("%m_%d_%H")
    output_file_name = f"output_{timestamp_string}.txt"
    
    try:
        with open(output_file_name, 'r') as file:
            file_content = file.read()
        
        embed = Embed(
            color = discord.Colour.dark_purple,
            title=file_content
        )
        await ctx.send(embed)
    except FileNotFoundError:
        print(f'file {output_file_name} was not found!')

disc_token = os.getenv("DISCORD_TOKEN")
print(disc_token)
bot.run(token=disc_token)