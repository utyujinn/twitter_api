import twitter_api as twi

args = twi.get_args()
key_path = args["key_path"]

utyu = twi.Twitter_api(key_path = key_path)
utyu.load_keys()

print(utyu.tweet("にゃーん"))