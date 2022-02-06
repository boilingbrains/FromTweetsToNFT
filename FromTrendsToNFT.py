import re
import os
import json
import requests

# Retreive keys and tokens
path = 'auth.txt'
lines = []
data_list = []
with open(path,"r") as f:
    lines =  f.readlines()
        
bearer_token = lines[6][12:]

def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    json_response = response.json()['data']
    for i in range(len(json_response)-1):
        text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",json_response[i]["text"]).split())    
        data_list.append(text)
    
    return data_list

def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "text"}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def get_user_id(username):
    getuid_url = "https://api.twitter.com/2/users/by?tweet.fields=id&usernames={}".format(username)
    response = requests.request("GET", getuid_url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    data = response.json()["data"][0]
    return data["id"]

def create_url(user_id):
    # Replace with user ID below
    #user_id = 44196397 #elon musk
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)


def main():
    #Retrieve tweets
    user_id = get_user_id("elonmusk")
    url = create_url(user_id)
    params = get_params()
    tweets = list(filter(None, connect_to_endpoint(url, params)))
    #print(json_response)
    print(json.dumps(tweets, indent=4, sort_keys=True))
    
    

if __name__ == "__main__":
    main()