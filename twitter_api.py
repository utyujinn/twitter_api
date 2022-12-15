import re
import base64
import os
import hashlib
from urllib import parse
import webbrowser
import requests
import json
import argparse
from time import time

SCOPES="tweet.read tweet.write tweet.moderate.write users.read follows.read follows.write offline.access space.read mute.read mute.write like.read like.write list.read list.write block.read block.write bookmark.read bookmark.write"

#ランダムな文字列(トークン)の生成
def generate_csrf_token(size:int=64):
  return re.sub('[^a-zA-Z0-9]+','',base64.urlsafe_b64encode(os.urandom(size)).decode("utf-8"))

class Twitter_api():

  #初期化処理
  def __init__(self) -> None:

    self.scope = SCOPES
    with open("users.json", "r", encoding = "utf-8") as f:
      data = json.load(f)
    self.username = data["default"]
    
    with open("key.json", "r", encoding = "utf-8") as f:
      data = json.load(f)
    if self.username in data:
      self.load_keys()
    else:
      return

    if self.expiration_time <= time()+60:
      self.refresh()


  #ユーザー情報の登録
  def add_user(self):
    code_verifier = generate_csrf_token()
    print(self.generate_authorization_url(code_verifier = code_verifier)+"\n")

    redirected_url = input("redirected url?\n")
    print()
    print(self.access_token_request(code_verifier = code_verifier, redirected_url = redirected_url))

    with open("users.json", "r", encoding = "utf-8") as f:
      data = json.load(f)
    
    tmp = {
      "access_token":self.access_token,
      "refresh_token":self.refresh_token,
      "client_id":self.client_id,
      "expiration_time":self.expiration_time
    }
    
    with open('key.json', 'r') as f:
      data = json.load(f)

    data["users"] = data["users"]+[self.username]
    data["default"] = self.username
    with open("key.json", "w", encoding = "utf-8") as f:
      json.dump(data, f, indent = 2)


  #アプリの認証urlを生成し、ブラウザで開く
  def generate_authorization_url(self, code_verifier:str)->str:

    csrf_token    = generate_csrf_token()
    authorize_url = "https://twitter.com/i/oauth2/authorize"
    params = {
      "response_type":"code",
      "client_id":self.client_id,
      "redirect_uri":self.redirect_uri,
      "scope":self.scope,
      "state":csrf_token,
      "code_challenge":base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest()).decode("utf-8").replace("=",""),
      "code_challenge_method":"S256"
    }
    q=parse.urlencode(params,quote_via=parse.quote,safe=':/')
    url = authorize_url+'?'+q
    webbrowser.open(url)
    return url


  #実行するためのトークンを発行、保存する。
  def access_token_request(self, code_verifier:str, redirected_url:str)->dict:

    url = parse.urlparse(redirected_url)
    query = url.query
    query_dict = dict(q.split('=') for q in query.split('&'))
    authorization_code = query_dict["code"]

    token_url = "https://api.twitter.com/2/oauth2/token"
    header = {
      "Content-Type":"application/x-www-form-urlencoded"
    }
    params = {
      "code":authorization_code,
      "client_id":self.client_id,
      "redirect_uri":self.redirect_uri,
      "code_verifier":code_verifier,
      "grant_type":"authorization_code"
    }
    response=requests.request(method="post",headers=header,url=token_url,params=params)
    response=json.loads(response.text)
    self.access_token = response["access_token"]
    self.refresh_token = response["refresh_token"]
    self.expiration_time = response["expires_in"]+time()
    self.save_keys()
    return response


  #トークンを保存 access_token_request内で呼び出される。
  def save_keys(self)->None:

    tmp = {
      "access_token":self.access_token,
      "refresh_token":self.refresh_token,
      "client_id":self.client_id,
      "expiration_time":self.expiration_time
    }
    
    with open('key.json', 'r') as f:
      data = json.load(f)

    data[self.username] = tmp

    with open("key.json", "w", encoding = "utf-8") as f:
      json.dump(data, f, indent = 2)


  #トークンを読み込む
  def load_keys(self)->None:

    with open("key.json", "r", encoding = "utf-8") as f:
      data = json.load(f)
    self.access_token     = data[self.username]["access_token"]
    self.refresh_token    = data[self.username]["refresh_token"]
    self.client_id        = data[self.username]["client_id"]
    self.expiration_time  = data[self.username]["expiration_time"]


  #トークンのリフレッシュを行う。
  def refresh(self)->dict:
    token_url = "https://api.twitter.com/2/oauth2/token"
    header = {
      "Content-Type":"application/x-www-form-urlencoded"
    }
    params = {
      "refresh_token":self.refresh_token,
      "client_id":self.client_id,
      "grant_type":"refresh_token"
    }

    response=requests.request(method="post",headers=header,params=params,url=token_url)
    response = json.loads(response.text)

    self.access_token = response["access_token"]
    self.refresh_token = response["refresh_token"]
    self.expiration_time = response["expires_in"] + time()
    self.save_keys()
    return response


  #ツイートする
  def tweet(self, text:str)->dict:

    endpoint_url = "https://api.twitter.com/2/tweets"
    header = {
      "Authorization":"Bearer " + self.access_token,
      "Content-type":"application/json"
    }
    data = {}
    data.setdefault("text", text)

    response = requests.request(method = "post", headers = header, url = endpoint_url, json = data)
    response = json.loads(response.text)
    return response


  #ツイートを取得する
  def get_tweet(self, id:str = None)->dict:
    if id == None:
      id = self.id
    endpoint_url = "https://api.twitter.com/2/tweets"

  #useridを取得する
  def get_userid(self, username:str)->dict:
    
    endpoint_url = "https://api.twitter.com/2/users/" + username
    header = {
      "Authorization":"Bearer " + self.access_token
    }

    response = requests.request(method = "post", headers = header, url = endpoint_url)
    response = json.loads(response.text)
    return response
