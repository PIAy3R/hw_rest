import requests

response = requests.get("http://gitlab.tcjk.com/api/v4/projects")

print(response.headers.get('Date'))