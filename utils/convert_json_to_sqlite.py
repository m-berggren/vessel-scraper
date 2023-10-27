import sqlite3
import json

DB_FILE = r".\db\vessel_info.db"
VESSEL_JSON = r".\utils\vessel_info.json"

conn = sqlite3.connect(DB_FILE)

with open(VESSEL_JSON, 'r') as json_file:
    data = json.load(json_file)

sql_str = "INSERT INTO vessels(imo, vessel, callsign, mmsi) VALUES(?, ?, ?, ?)"

for item in data:
    conn.execute(sql_str, (item['imo'], item['vessel'], item['callsign'], item['mmsi']))
    print(item['imo'])

conn.commit()
conn.close()
