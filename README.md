#reddit Twitter Bot

A Python bot that looks up image links from reddit and automatically posts them on Twitter.

This fork automatically edits PNG images to circumvent Twitter's JPEG compression, allowing for higher-quality image uploads.

##Disclaimer

I hold no liability for what you do with this script or what happens to you by using this script. Abusing this script *can* get you banned from Twitter, so make sure to read up on proper usage of the Twitter API.

##Dependencies

You will need to install Python's [tweepy](https://github.com/tweepy/tweepy), [Pillow](https://github.com/python-pillow/Pillow), and [PRAW](https://praw.readthedocs.org/en/) libraries first:

    pip install tweepy
    pip install Pillow
    pip install praw
    
You will also need to create an app account on Twitter and an app account on reddit: 

[[Twitter]](https://dev.twitter.com/apps)

1. Sign in with your Twitter account
2. Create a new app account
3. Modify the settings for that app account to allow read & write
4. Generate a new OAuth token with those permissions
5. Manually edit this script and put those tokens in the script

[[Reddit]](https://www.reddit.com/prefs/apps/)

1. Sign in with your reddit account
2. Create an app ("script" is easiest)
3. Register for production API usage https://www.reddit.com/wiki/api
4. Edit the script to use the client ID and secret, as well as your username/password and user-agent (recommended format [here](https://github.com/reddit/reddit/wiki/API))

##Usage

Once you edit the bot script to provide the necessary API keys and the subreddit you want to tweet from, you can run the bot on the command line:

    python reddit_twitter_bot.py

##Have questions? Need help with the bot?

If you're having issues with or have questions about the bot, please [file an issue](https://github.com/alanhuang122/reddit-twitter-bot/issues) in this repository or [upstream](https://github.com/rhiever/reddit-twitter-bot/issues). Please check the existing (and closed) issues to make sure your issue hasn't already been addressed.
