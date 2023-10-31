import json

import requests

class ScrapeMarineTraffic:
    def __init__(self, imo):
        self.response = self.get_ship_info(imo)

    def get_ship_info(self, imo):

        url = f"https://www.marinetraffic.com/en/ais/details/ships/imo:{imo}"

        headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate",
            "user-agent": "Mozilla/5.0",
            "x-requested-with": "XMLHttpRequest",
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

        except requests.exceptions.HTTPError:
            return None

        return response.content

    @staticmethod
    def get_response_data(self):
        data = self.response

        if not data:
            return
        
        return json.loads(data.decode("utf-8"))





