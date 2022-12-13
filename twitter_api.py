import re
import base64
import os
import hashlib
from urllib import parse
import webbrowser
import requests
import json
import argparse

SCOPES="tweet.read tweet.write tweet.moderate.write users.read follows.read follows.write offline.access space.read mute.read mute.write like.read like.write list.read list.write block.read block.write bookmark.read bookmark.write"

#ランダムな文字列(トークン)の生成
def generate_csrf_token(size:int=64):
  return re.sub('[^a-zA-Z0-9]+','',base64.urlsafe_b64encode(os.urandom(size)).decode("utf-8"))

#引数取得
def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("-id", type=str, required=False, help="username")
  args = parser.parse_args()

  my_dict = dict()
  if args.id == None:
    args.id = "key"
  #id -> key_path : id.json
  my_dict["key_path"] = args.id + ".json"
  return my_dict

class Twitter_api():

  #初期化処理
  def __init__(self,consumer_key:str=None,consumer_secret:str=None,client_id:str=None,
  client_secret:str=None,app_name:str=None,access_token:str=None,refresh_token:str=None,
  scopes:str=SCOPES,redirect_uri:str="http://localhost:8080",key_path:str="key.json") -> None:

    self.consumer_key     = consumer_key
    self.consumer_secret  = consumer_secret
    self.client_id        = client_id
    self.client_secret    = client_secret
    self.app_name         = app_name
    self.redirect_uri     = redirect_uri
    self.access_token     = access_token
    self.refresh_token    = refresh_token
    self.expiration_time  = 0
    self.scope            = scopes
    self.key_path         = key_path


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
    
    self.access_token=response["access_token"]
    self.save_keys()
    return response


  #トークンを保存 access_token_request内で呼び出される。
  def save_keys(self)->None:

    data = {
      "access_token":self.access_token,
    }
    with open(self.key_path, "w", encoding = "utf-8") as f:
      json.dump(data, f, indent = 2)
      

  #トークンを読み込む
  def load_keys(self)->None:

    with open(self.key_path, "r", encoding = "utf-8") as f:
      data = json.load(f)
    
    self.access_token   = data["access_token"]


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
