import sqlite3
import pandas as pd
from main import output

conn = sqlite3.connect('CV.db')

c = conn.cursor()

c.execute("""CREATE TABLE CV (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_name text,
            job_salary text,
            job_net_or_gross text,
            job_currency text,
            job_city text,
            job_time text,
            job_link text,
            job_desc_column_name_1 text,
            job_desc_column_value_1 text,
            job_desc_column_name_2 text,
            job_desc_column_value_2 text,
            job_desc_column_name_3 text,
            job_desc_column_value_3 text,
            job_desc_column_name_4 text,
            job_desc_column_value_4 text
            )""")

output.to_sql('CV', conn, if_exists='replace', index = False)

c.execute("SELECT * FROM CV")

conn.commit()

pd.options.display.max_rows = 150
pd.options.display.max_columns = 16
print(pd.read_sql_query("SELECT * FROM CV", conn))

conn.close()
