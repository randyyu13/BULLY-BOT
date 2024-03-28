from dotenv import load_dotenv
from scrape_utils import *
from misc_utils import *
import datetime
import pytz
from discord.ext import commands, tasks
import os
from discord import *
from gcp_proxy import *
import json

load_dotenv()
intents=Intents().all()
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    look_for_update.start()
    # look_for_twitter_update.start()

@bot.command()
async def p(ctx):
    await ctx.send("any updates are now provided automatically")

@tasks.loop(minutes=5)
async def look_for_update():
    value_lines_blob = get_most_recent_blob('plays-bucket', 'google-credentials.json')
    tweet_blobs = get_all_blobs('tweets-bucket-1', 'google-credentials.json')

    minutes_since_update = int((datetime.datetime.now(pytz.UTC) - value_lines_blob.time_created).total_seconds() / 60)
    if(minutes_since_update < 5):
        print(minutes_since_update)
        await post_most_recent_lines(value_lines_blob, minutes_since_update)

    for tweet_blob in tweet_blobs:
        minutes_since_update = int((datetime.datetime.now(pytz.UTC) - tweet_blob.time_created).total_seconds() / 60)
        print(minutes_since_update)
        if(minutes_since_update < 5):
            await post_most_recent_tweets(tweet_blob, minutes_since_update)

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
        channel = utils.get(curr_guild.channels, name="sports-betting-bot")
        if(contains_lock(all_lines)):
            try:
                role = utils.get(curr_guild.roles,name="gamblers")
                await channel.send(f'{role.mention}')
            except:
                print("role not found")
        else:
            print("does not contain lock")
        await channel.send(embed=embed)

async def post_most_recent_tweets(blob, minutes):
    tweets_json = json.loads(blob.download_as_text())
    all_tweet_maps = unpackage_tweets_json(tweets_json)
    for tweet_map in all_tweet_maps:
        if(is_player_prop(tweet_map['content'])):
            embed = Embed(
                color = Colour.blue(),
                description=tweet_map['content']
            )
            embed.set_author(name=tweet_map['capper_name'])
            embed.set_footer(text = f'Last updated {minutes} minutes ago. This feature is in testing')
            for curr_guild in bot.guilds:
                # sports betting channel
                try:
                    channel = utils.get(curr_guild.channels, name="tweet-test")
                    await channel.send(embed=embed)
                except:
                    print('channel tweet-test not found')

disc_token = os.getenv("DISCORD_TOKEN")
bot.run(token=disc_token)