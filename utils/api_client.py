import requests

class APIClient:
    BASE_URL = 'https://petstore.swagger.io/v2'

    def get(self, path, **kwargs):
        return requests.get(f"{self.BASE_URL}{path}", **kwargs)

    def post(self, path, **kwargs):
        return requests.post(f"{self.BASE_URL}{path}", **kwargs)

    def put(self, path, **kwargs):
        return requests.put(f"{self.BASE_URL}{path}", **kwargs)

    def delete(self, path, **kwargs):
        return requests.delete(f"{self.BASE_URL}{path}", **kwargs)