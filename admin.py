import twitter_api as twi

def add():
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


while(True):
  print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n0:adduser\n1:change_user\n2:reset_userdata\nelse:exit\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
  mode = input()
  if mode == "0":
    add()
  elif mode == "1":
    utyu = twi.Twitter_api()
    utyu.change_user()
  elif mode == "2":
    twi.reset_data()
  else:
    break