import twitter_api as twi
from time import time

args = twi.get_args()
key_path = args["key_path"]

utyu = twi.Twitter_api(key_path = key_path)
utyu.load_keys()
print(utyu)

if utyu.expiration_time >= time()+60:
    utyu.refresh()
    print("refresh")

print(utyu.tweet("にゃーん"))