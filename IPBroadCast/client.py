import requests

header = {'user-agent':'fromRouter/0.1'}
r = requests.get("http://doris.work/lab/")
if r.status_code == 200:
    print r.text
    print r.headers