from dotenv import load_dotenv
load_dotenv()

import token
# Declare empty header dictionary
apiHeader = {}
# open token
access_token =  token.env('ACCESS_TOKEN')
# secret key
secret_key = token.env('CLIENT_SECRET')
nonce = uuid.uuid4()
t = int(round(time.time() * 1000))
string_to_sign = "{}{}{}".format(access_token, t, nonce)

string_to_sign = bytes(string_to_sign, "utf-8")
secret_key = bytes(secret_key, "utf-8")

sign = base64.b64encode(
    hmac.new(secret_key, msg=string_to_sign, digestmod=hashlib.sha256).digest()
)
print("Authorization: {}".format(access_token))
print("t: {}".format(t))
print("sign: {}".format(str(sign, "utf-8")))
print("nonce: {}".format(nonce))

# Build api header JSON
apiHeader["Authorization"] = access_token
apiHeader["Content-Type"] = "application/json"
apiHeader["charset"] = "utf8"
apiHeader["t"] = str(t)
apiHeader["sign"] = str(sign, "utf-8")
apiHeader["nonce"] = str(nonce)

######################
# Webhook登録

WEBHOOK_URL = token.env('DISCORD_WEBHOOK')

# Request body
req_body_json = {
    "action": "setupWebhook",
    "url": WEBHOOK_URL,
    "deviceList": "ALL",
}
# リクエストを送信
response = requests.post(
    "https://api.switch-bot.com/v1.1/webhook/setupWebhook",
    json=req_body_json,
    headers=apiHeader,
)

# レスポンスを確認
if response.status_code != 200:
    raise ValueError(f"Status code: {response.status_code}")

data = response.json()
print(f"レスポンス:{data}")