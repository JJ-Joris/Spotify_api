import requests
import json
from datetime import datetime
import datetime
import base64
from secrets import CLIENTID, CLIENTSECRET

# Get an access token with a real api, this needs more implementations to work
def get_access_token():
    #Base64 encode client ID & client secret
    message = f"{CLIENTID}:{CLIENTSECRET}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    auth_url = "https://accounts.spotify.com/api/token"

    auth_headers = {
        "Authorization" : "Basic " + base64_message
    }

    aut_data = {
        "grant_type" : "client_credentials"
    }

    res = requests.post(auth_url, headers=auth_headers, data=aut_data)

    data = res.json()
    print(json.dumps(data, indent = 2))

    access_token = data["access_token"]

    return access_token