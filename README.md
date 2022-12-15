# Twitter_api

## How to use
1. First, `python adduser.py` to make `users.json` and `key.json` file. 
2. Write method you want to do in `main.py` and 
   `python main.py` to do.
3. If you want to change user, `python chuser.py`.

## Libraries
To use api, write `import twitter_api` to header in the program. 
There are many useful functions.

Once you executed the `mkjson.py`, you can use api's by writing
this code on top of the programs.
```
import twitter_api as twi

func_name = twi.Twitter_api()
```

After write this code, you can use below api's.
In the below, I'll write utyu as func_name.

### tweet
`utyu.tweet("text")`
makes the simple tweet.

### retweet

### get tweet id

### reply

## config

### reset data
If you want to reset all user data, `python reset.py` will remove user data.