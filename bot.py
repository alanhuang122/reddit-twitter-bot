# -*- coding: utf-8 -*-

import praw, tweepy, requests, os, time, urlparse
from glob import glob
from PIL import Image

reddit_client_id = ''
reddit_client_secret = ''
reddit_username = ''
reddit_password = ''
reddit_user_agent = ''

twitter_access_token = ''
twitter_access_secret = ''
twitter_consumer_key = ''
twitter_consumer_secret = ''

auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)

api = tweepy.API(auth)
config = api.configuration()
t_co_length = config['short_url_length_https']

subreddit = ''

image_dir = ''

cache_file = 'archive.dat'

twitter_max_len = 140

delay = 30

def setup_reddit_connection(subreddit):
    print('setting up reddit connection')
    r_api = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, password=reddit_password, user_agent=reddit_user_agent, username=reddit_username)
    return r_api.subreddit(subreddit)

def create_tweets(subreddit):
    post_dict = {}
    post_ids = []

    print('getting reddit posts')
    for submission in subreddit.new(limit=10):
        if not already_tweeted(submission.id):
            post_dict[submission.title] = {}
            post = post_dict[submission.title]
            post['link'] = submission.permalink

            post['img_path'] = get_image(submission.url)
            if not post['img_path']:
                continue

            post_ids.append(submission.id)
        else:
            print('already tweeted: {0}'.format(str(submission)))

    return post_dict, post_ids

import cPickle

def already_tweeted(post_id):
    cache = cPickle.load(open(cache_file))
    try:
        return post_id in cache
    except TypeError:
        print('error in searching cache')

def strip_title(title, num):
    if len(title) <= num:
        return title
    else:
        return title[:num - 1] + '…'

def get_image(img_url):
    if img_url.endswith(('.jpg', '.png', '.gifv', '.gif')):
        file_name = os.path.basename(urlparse.urlsplit(img_url).path)
        img_path = image_dir + '/' + file_name
        print('downloading image at {0} to {1}'.format(img_url, img_path))
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open(img_path, 'wb') as img_file:
                for chunk in response:
                    img_file.write(chunk)
            if img_path.endswith('.png'):
                edit_image(img_path)
            return img_path
        else:
            print('dl failure - status code {0}'.format(resp.status_code))
    else:
        print('url not image link: {0}'.format(img_url))

    return None

def edit_image(img_path):
    img = Image.open(img_path)
    img = img.convert('RGBA')
    pixdata = img.load()
    pixel = pixdata[0,0]
    pixdata[0,0] = (pixel[0], pixel[1], pixel[2], 0)
    img.save(img_path)

def tweet(post_dict, post_ids):
    for post, post_id in zip(post_dict, post_ids):
        img_path = post_dict[post]['img_path']
        print(img_path)

        text = ' https://reddit.com' + post_dict[post]['link']
        post_text = strip_title(post, 140 - t_co_length) + text
        print('posting on Twitter: {0}'.format(text))
        if img_path:
            print('with image {0}'.format(img_path))
            try:
                media_id = api.media_upload(filename=img_path)
                api.update_status(status=post_text, media_ids=[media_id.media_id_string])
            except tweepy.TweepError as e:
                print(e)
        else:
            api.update_status(status=post_text)
        log_tweet(post_id)
        time.sleep(delay)

def log_tweet(post_id):
    cache = cPickle.load(open(cache_file))
    cache.append(post_id)
    cPickle.dump(cache, open(cache_file, 'w'))

def main():
    if not os.path.exists(cache_file):
        f = open(cache_file, 'w')
        cPickle.dump([], f)
        f.close()
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    sr = setup_reddit_connection(subreddit)
    post_dict, post_ids = create_tweets(sr)
    tweet(post_dict, post_ids)

    for filename in glob(image_dir + '/*'):
        os.remove(filename)

if __name__ == '__main__':
    main()
