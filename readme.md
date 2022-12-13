# Twitter_api

## How to use
1. First, `mkjson.py -id userid` to make `userid.json` file. 
   If there were not argument, It will make `key.json` file.
2. Second, `main.py -id userid`

## Libraries
To use api, write `import twitter_api` to header in the program. 
There are many useful functions.

Once you executed the `mkjson.py`, you can use api's by writing
this code on top of the programs.
```
import twitter_api as twi
import time

args = twi.get_args()
key_path = args["key_path"]

utyu = twi.Twitter_api(key_path = key_path)
utyu.load_keys()

if t.expiration_time<=time.time()+60:
    t.refresh()
    print("refresh")
```

After write this code, you can use below api's.

### tweet
`utyu.tweet("text")`
makes the simple tweet.

### retweet

### get tweet id

### reply
