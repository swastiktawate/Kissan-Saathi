import requests

url = 'https://api.sarvam.ai/speech-to-text'
headers = {'api-subscription-key': 'sk_2zmoto84_K7CmckcZyOV2LexsDzn8ltUK'}

# Try with a dummy file
files = {'file': ('dummy.wav', b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00')}
try:
    res = requests.post(url, headers=headers, files=files)
    print(res.status_code, res.text)
except Exception as e:
    print(e)
