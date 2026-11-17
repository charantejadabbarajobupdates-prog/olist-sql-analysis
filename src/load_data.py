import glob, os, sqlite3
import pandas as pd

conn = sqlite3.connect("olist.db")
for f in glob.glob("data/raw/*.csv"):
    name = os.path.splitext(os.path.basename(f))[0]
    name = name.replace("olist_", "").replace("_dataset", "")
    pd.read_csv(f).to_sql(name, conn, if_exists="replace", index=False)
    print("loaded", name)
conn.close()
