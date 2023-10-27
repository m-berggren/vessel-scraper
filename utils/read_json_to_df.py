import pandas as pd

DB_FILE = r".\db\vessel_info.db"
VESSEL_JSON = r".\utils\vessel_info.json"

df = pd.read_json(VESSEL_JSON)

df = df.drop(index=2814)
df.to_csv("test_file2.csv")