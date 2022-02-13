import re
import os
import shutil
import json
import random
import requests
import logging
from datetime import datetime
# Retreive keys and tokens
path = 'auth.txt'
lines = []
data_list = []


with open(path,"r") as f:
    lines =  f.readlines()
        
bearer_token = lines[6][12:]

def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    json_response = response.json()['data']
    for i in range(len(json_response)-1):
        text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(&[A-Za-z0-9]+)"," ",json_response[i]["text"]).split())    
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
    #print(response.status_code)
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
    logfile = 'FromTweetsToNFT_{}.log'.format(str(datetime.now())[:10])
    logging.basicConfig(filename=logfile,
                        encoding='utf-8',
                        level=logging.INFO, 
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')
    #Retrieve tweets
    logging.info('Script launched:')
    username = "elonmusk"
    logging.info('Retrieve tweets of : {}'.format(username))
    user_id = get_user_id(username)
    url = create_url(user_id)
    params = get_params()
    tweets = list(filter(None, connect_to_endpoint(url, params)))
    tweets = [item for item in tweets if len(item)< 100] #limit to avoid a too lon tweet
    logging.info('This is the results: {}'.format(tweets))
    #store tweets in a file a part
    
    tweet_number = random.randint(0,len(tweets)-1)
    choosed_tweet = tweets[tweet_number]
    print("The choosed tweet is:", choosed_tweet)
    logging.info('The choosed tweet is: {}'.format(choosed_tweet))
    #print(json.dumps(tweets, indent=4, sort_keys=True))
    dest_dir = os.path.join(os.getcwd(),'OUTPUT')
    os.chdir(r"VQGAN-CLIP/") 
    #os.system("conda activate vqgan")
    #print(os.getcwd())
    samples = os.listdir(r"samples/")
    samples = [s for s in samples if s[-3:]=="png" or s[-3:]=="jpg" ]
    style_number = random.randint(0,len(samples)-1)
    choosed_style = samples[style_number]
    print("The choosed style is:", choosed_style[:-4])
    logging.info('The choosed style is: {}'.format(choosed_style))
    cmd = " python generate.py -p  \"{}\" -ii samples/{} ".format(choosed_tweet,choosed_style)
    #generate image
    try:
        os.system(cmd)
        src_img = os.path.join(os.getcwd(), 'output.png')
        dest_img = os.path.join(dest_dir,src_img)
        shutil.copy(src_img,dest_dir)
        new_dst_img_name = os.path.join(dest_dir, choosed_tweet+"_"+choosed_style[:-4]+".png")
        os.rename(dest_img, new_dst_img_name)
        logging.info('Image correctly generated and it is located here : {}'.format(new_dst_img_name))
    except Exception as e:
        logging.info('Something went wrong:', e)    
        
    logging.info('Script stopped')


if __name__ == "__main__":
    main()
