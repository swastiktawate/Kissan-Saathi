import requests

url = 'https://api.sarvam.ai/speech-to-text'
headers = {'api-subscription-key': 'sk_2zmoto84_K7CmckcZyOV2LexsDzn8ltUK'}

# Try a dummy call to see the required fields
try:
    res = requests.post(url, headers=headers)
    print(res.status_code, res.text)
except Exception as e:
    print(e)
