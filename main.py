import twitter_api as twi
import time

args = twi.get_args()
key_path = args["key_path"]

utyu = twi.Twitter_api(key_path = key_path)
utyu.load_keys()

if t.expiration_time<=time.time()+60:
    t.refresh()
    print("refresh")

print(utyu.tweet("にゃーん"))