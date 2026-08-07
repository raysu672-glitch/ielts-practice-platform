import requests

url = 'http://localhost:8000/transcribe'
file_path = r'c:\Users\49873\.trae-cn\work\6a4f11db7a80cdd9cd13314d\recording.wav'

print(f'Uploading {file_path} to {url}')
with open(file_path, 'rb') as f:
    files = {'file': ('recording.wav', f, 'audio/wav')}
    res = requests.post(url, files=files, timeout=300)

print(f'Status: {res.status_code}')
print(res.json())
