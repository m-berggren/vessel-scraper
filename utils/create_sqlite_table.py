import sqlite3

DB_FILE = r".\db\vessel_info.db"

# Run the first time table should be set up
table = """
CREATE TABLE vessels (
imo int PRIMARY KEY,
vessel text,
callsign text,
mmsi int
);"""

conn = sqlite3.connect(DB_FILE)
conn.execute(table)
conn.close()

