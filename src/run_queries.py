import glob, sqlite3
import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)
conn = sqlite3.connect("olist.db")
for f in sorted(glob.glob("sql/*.sql")):
    print("\n=====", f, "=====")
    df = pd.read_sql(open(f, encoding="utf-8-sig").read(), conn)
    print(df.head(15).to_string(index=False))
