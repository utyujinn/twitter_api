import twitter_api as twi

flag = True
utyu = twi.Twitter_api()

while flag:
  print("<><><><><><><><><><><><><><><><><><><><>")
  utyu.username = input("User name?\n")
  utyu.redirect_uri = input("redirect_uri?\n(default:""http://localhost:8080"")\n")
  utyu.client_id = input("client_id?\n")
  print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
  print("username     = " + utyu.username)
  print("redirect_uri = " + utyu.redirect_uri)
  print("client_id    = " + utyu.client_id)
  print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
  print("Is this correct?(y/n)")
  c = input()
  if c == "y":
    flag = False

utyu.add_user()
