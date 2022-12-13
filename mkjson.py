import twitter_api as twi

args = twi.get_args()
key_path = args["key_path"]

app_name = "utyujin"
redirect_uri = "https://utyujin.cf"
client_id = "b3ZoMU10cHFVOXBodVRzYmp0emg6MTpjaQ"
code_verifier = twi.generate_csrf_token()

x = twi.Twitter_api(client_id = client_id, app_name = app_name, redirect_uri = redirect_uri, key_path = key_path)
print(x.generate_authorization_url(code_verifier = code_verifier)+"\n")

redirected_url = input("redirected url?\n")
print()
print(x.access_token_request(code_verifier = code_verifier, redirected_url = redirected_url))