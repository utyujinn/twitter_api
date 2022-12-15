import twitter_api as twi

utyu = twi.Twitter_api()

tweets = utyu.get_tweet()

for i in tweets["data"]:
  print(i)