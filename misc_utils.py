from gcp_proxy import *
import os

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
    

def is_player_prop(tweet_content):
    return True