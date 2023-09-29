from telethon import TelegramClient
from telethon.tl.functions.contacts import ResolveUsernameRequest
import os
import time
import re
import numpy as np
import pandas as pd
from random import randint

CHANNEL_LIST = pd.read_csv('valid_ids.csv')
CHANNEL_LIST = CHANNEL_LIST['channel'].tolist()

# telegram API
api_id = 252493
api_hash = 'eb5e4d9afafb381a04881408fc4c5546'

client = TelegramClient('telegram_stats', api_id, api_hash)
#client.start()
client.connect()

def clean_text(post_text, channel_name):
    channel_title_1 = "\@" + channel_name
    channel_title_2 = channel_title_1.upper()
    post_text = re.sub(r"\bhttp\S+\b", "", post_text)
    post_text = re.sub('\r', '', 
                          re.sub('\n', '', 
                                 re.sub('\t', '', 
                                        re.sub('xa0', ' ',
                                               re.sub('u200b', ' ', post_text)))))
    post_text = re.sub(channel_title_1, ' ', post_text)
    post_text = re.sub(channel_title_2, ' ', post_text)
    post_text = re.sub('\.', '. ', post_text)
    post_text = re.sub(' +', ' ', post_text)
    return(post_text)
    
def extract_posts(channel_name):
    try:
        messages = client.iter_messages(channel_name, limit = 200)
        messages = list(messages)
    except Exception:
        return        
    posts = []
    for i in range(0,len(messages)):
        if messages[i].message is not None:
            new_post = clean_text(messages[i].message, channel_name)
            posts.append(new_post)
    channel_title = [channel_name]*len(posts)
    new_row = pd.DataFrame({'channel': channel_title, 'posts': posts})       
    return new_row

CHANNEL_POSTS = pd.DataFrame(columns=['channel', 'posts'])
for i in range(20, len(CHANNEL_LIST)):
    print(i, CHANNEL_LIST[i])
    NEW_ROW = extract_posts(CHANNEL_LIST[i]) 
    if NEW_ROW is not None:
        CHANNEL_POSTS = CHANNEL_POSTS.append(NEW_ROW, ignore_index=True)
    if i > 0 and i%100 == 0:
        textfile = open("Telegram_texts.csv", 
                    'w', encoding='utf-8')
        CHANNEL_POSTS.to_csv(textfile, index = False)
        textfile.close()
    if i > 0 and i%250 == 0:
        pause = randint(1, 50)
        time.sleep(pause)
    if i > 0 and i%50 == 0:
        pause = randint(1, 7)
        time.sleep(pause)

textfile = open("Telegram_texts.csv", 'w', encoding='utf-8')
CHANNEL_POSTS.to_csv(textfile, index = False)
textfile.close()

bb = extract_posts("a_zet")
messages = client.iter_messages("a_zet", limit = 120)
messages = list(messages)

client.disconnect()


