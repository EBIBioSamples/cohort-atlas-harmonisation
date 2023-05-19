import requests


class ZoomaClient:
    def __init__(self):
        pass

    def get_json(self, url):
        resp = requests.get(url)
        if resp.status_code == 200:
            return (resp.json())
        return None
