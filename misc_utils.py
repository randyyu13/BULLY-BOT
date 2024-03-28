from gcp_proxy import *
from datetime import datetime
import pytz
import os
from openai import OpenAI

GPT_QUESTION = 'If the following text is a single player prop for a future game in the context of sports betting, respond with the prop itself. Otherwise, respond with null. Additionally, respond with null if the text includes the token "RT @", "✅" or if there are multiple props:'

def write_array_to_file(array, filename):
    with open(filename, 'w') as file:
        for item in array:
            file.write(str(item) + '\n')
    upload_to_gcs('plays-bucket', filename, filename, "google-credentials.json")
    os.remove(filename)

def unpackage_tweets_json(tweets_json):
    result = []
    for item in tweets_json:
        result.append({
            "capper_name": item["capper_name"],
            "tweet_id": item["tweet_id"],
            "time_created": item["time_created"],
            "content": item["content"]
        })
    print(result)
    return result

def find_minutes_since_given_datetime(dt):
    return int((datetime.now(pytz.UTC) - dt).total_seconds() / 60)

def parse_datetime(datetime_str):
    return datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %z %Y')
    
def get_player_prop_from_tweet(tweet_content):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": f'{GPT_QUESTION}\n{tweet_content}'}
    ]
    )
    ai_output = completion.choices[0].message.content
    if(ai_output.lower() == 'null'):
        return None
    return ai_output