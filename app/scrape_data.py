import re

import requests
from bs4 import BeautifulSoup


class ScrapeMarineTraffic:
    def __init__(self, imo):
        self.imo = imo

    def request_ship_data_with_imo(self):

        url = f"https://www.marinetraffic.com/en/ais/details/ships/imo:{self.imo}"

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
    
    def get_ship_data(self):
        byte_data = self.request_ship_data_with_imo()
        soup = BeautifulSoup(byte_data, "html.parser")
        
        try:
            string = soup.title.string
        except AttributeError as e:
            return e
    

        vessel_dict = {"imo": None, "mmsi": None, "callsign": None, "vessel": None}

        imo_match = re.search(r"IMO (\d+)", string)
        if imo_match:
            vessel_dict["imo"] = int(imo_match.group(1))

        mmsi_match = re.search(r"MMSI (\d+)", string)
        if mmsi_match:
            vessel_dict["mmsi"] = int(mmsi_match.group(1))

        callsign_match = re.search(r"Call Sign (\w+)", string)
        if callsign_match:
            vessel_dict["callsign"] = callsign_match.group(1)

        vessel_name_match = re.search(r"Ship\s+([\w\s]+)\s+\(", string)
        if vessel_name_match:
            vessel_dict["vessel"] = vessel_name_match.group(1)
        
        return vessel_dict





