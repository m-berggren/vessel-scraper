import sqlite3

DB = r"db\vessel_info.db"

def get_data_from_db() -> list:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    data = cur.execute("SELECT * FROM vessels")
    list_of_data = data.fetchall()
    conn.close()
    return list_of_data

def update_data_to_db(data:list):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("UPDATE vessels SET vessel=?, callsign=?, mmsi=? WHERE imo=?", (data[1], data[2], data[3], data[0]))
    conn.commit()
    cur.close()

if __name__ == "__main__":
    pass



    


