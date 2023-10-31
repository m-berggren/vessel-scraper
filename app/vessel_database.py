import sqlite3
import tkinter as tk
from tkinter import messagebox

DB = r"db\vessel_info.db"

def get_data_from_db() -> list:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    data = cur.execute("SELECT * FROM vessels ORDER BY vessel ASC")
    list_of_data = data.fetchall()
    conn.close()
    return list_of_data

def update_data_to_db(data:list):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("UPDATE vessels SET vessel=?, callsign=?, mmsi=? WHERE imo=?", (data[1], data[2], data[3], data[0]))
    conn.commit()
    cur.close()

def add_vessel_to_db(data: dict):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    imo_exist = cur.execute("SELECT imo FROM vessels WHERE imo = ?", (data.get('imo'),))
    if imo_exist.fetchone():
        tk.messagebox.showinfo(title=None, message="IMO already exists in database.")
        return False

    cur.execute("INSERT OR IGNORE INTO vessels(imo, vessel, callsign, mmsi) VALUES(?, ?, ?, ?)",
                (data.get('imo'), data.get('vessel'), data.get('callsign'), data.get('mmsi')))
    conn.commit()
    cur.close()
    return True

def delete_vessel_from_db(imo: int):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("DELETE FROM vessels where imo=?", (imo,))
    conn.commit()

def count_vessels_in_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    count = cur.execute("SELECT COUNT(imo) FROM vessels")
    count = count.fetchone()
    conn.commit()
    cur.close()

    return ''.join([str(x) for x in count])

if __name__ == "__main__":
    pass



    


