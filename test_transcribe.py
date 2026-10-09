import requests

url = 'http://localhost:8000/api/v1/transcribe'

files = {'file': ('dummy.wav', b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00', 'audio/wav')}
data = {'language': 'hi'}
try:
    res = requests.post(url, files=files, data=data)
    print(res.status_code, res.text)
except Exception as e:
    print(e)
