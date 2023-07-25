import requests


class ZoomaClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def field_label(self):
        resp = requests.get(self.base_url)
        if resp.status_code == 200:
            return resp.json()
        return None
