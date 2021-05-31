import tweepy
import time
# from meigaku.googlespread import get_info
import csv
import math
import random
import datetime
import configparser
##########################################################################
# いいねは２４時間で１０００件まで。１０００件以上いいねをするとペナルティを受けます。 #
##########################################################################

config=configparser.ConfigParser()
config.read('meigaku/config.py')

CONSUMER_KEY = config['twitter']['CONSUMER_KEY']
CONSUMER_SECRET = config['twitter']['CONSUMER_SECRET']
ACCESS_TOKEN = config['twitter']['ACCESS_TOKEN']
ACCESS_SECRET = config['twitter']['ACCESS_SECRET']
auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)
api=tweepy.API(auth)

# 自動いいね
def auto_good(searchtext):
    count=10
    search_results = api.search(q=searchtext,count=count)
    print('『{}』を含むツイートを{}件いいねしています'.format(searchtext,count))
    for result in search_results:
        tweet_id=result.id
        time.sleep(2)
        try:
            api.create_favorite(id=tweet_id)
            time.sleep(2)
        except Exception as e:
            print(e)
# 自動フォロー、自動いいね同時におこなう
def auto_follow(searchtext):
    count=10
    search_results = api.search(searchtext, count)
    for result in search_results:
        tweet_id = result.id
        user_id = result.user._json['id']  # ←追記
        try:
            api.create_favorite(tweet_id)
            time.sleep(3)
            # api.retweet(tweet_id)          # リツイート
            api.create_friendship(user_id) # ←追記
            time.sleep(3)
        except Exception as e:
            print(e)

def auto_tweet_circle():
    clubs = get_info_fromecsv()
    n=random.shuffle(clubs)

    for club in clubs[0:3]:
        title,url,subtext =club[0],club[1],club[2][0:100]
        date_time=datetime.datetime.now()
        post_time = date_time.strftime('%Y-%m-%d %H:%M')
        content='サークル紹介します!!\n'+str(title)+'\n'+subtext+'\n'+date_time+'\n'+url
        api.update_status(content)
        time.sleep(60)

    print("tweet数：{},投稿完了".format(3))

def auto_tweet_famous_post():
    urls=['https://gakuseikoujyou.com/jikanwari/','https://gakuseikoujyou.com/risyu/','https://gakuseikoujyou.com/online_kotsu/','https://gakuseikoujyou.com/onlineclass/']
    title='皆さんこんにちは！！明学ナビです.\n新入生の皆さんにオススメの記事を紹介します！！\n'
    date_time=datetime.datetime.now()
    post_time=date_time.strftime('%Y-%m-%d %H:%M')
    hasshutagu='\n#春から明学'
    for url in urls:
        api.update_status(title+url+'\n'+post_time+hasshutagu)
        time.sleep(90)

def get_info_fromecsv():
    with open('meigaku_id.csv') as f:
        reader=csv.reader(f)
        l=[row for row in reader]
        return l

if __name__=='__main__':
    searchtext =['春から明学','明学ナビ','明学']
    # for text in searchtext:
    #     auto_good(text)
    # auto_tweet_famous_post()
    auto_tweet_circle()

#/Users/mamoru/opt/anaconda3/bin:/Users/mamoru/opt/anaconda3/condabin:/Users/mamoru/.rbenv/shims:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin










