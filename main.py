import twitter_api as twi

utyu = twi.Twitter_api()

tweets = utyu.mentioned_tweet()

strings = ["ぼざろガチャ","ぼガチャ","ざガチャ"]
for i in tweets["data"]:
  print(i)
  for string in strings:
    if string in i["text"]:
      id = i["id"]
      print(utyu.reply("にゃーん",id))
