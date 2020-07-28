import json
from phonebook.data_operations.api.constants import BASE_URL
import requests


class API:

    @staticmethod
    def send_request(telephone):
        params = {
            'number': telephone
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        response_json = response.content
        response_dict = json.loads(response_json)
        print(response_dict)

        if 'valid' in response_dict:
            return response_dict
        else:
            return response_dict['error']
