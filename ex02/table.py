import os
import psycopg2

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# PARENT_DIR = os.path.dirname(BASE_DIR)
# csv_relative_path = os.path.join('data', 'customer', 'data_2022_oct.csv')
# csv_absolute_path = os.path.join(PARENT_DIR, csv_relative_path)

# print(csv_absolute_path)

# if not os.path.exists(csv_absolute_path):
#     raise FileNotFoundError(f"CSV file not found at: {csv_absolute_path}")

conn = psycopg2.connect(
    database="piscineds",
    user="nzhuzhle",
    password="mysecretpassword",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

create_table_sql = """
CREATE TABLE IF NOT EXISTS  data_2022_oct (
    event_time TIMESTAMP WITH TIME ZONE NOT NULL,
    event_type TEXT,
    product_id INTEGER,
    price NUMERIC(10,2),
    user_id BIGINT,
    user_session UUID
);
"""

copy_sql = """
COPY data_2022_oct FROM '/csv_data/data_2022_oct.csv' 
WITH (FORMAT csv, HEADER true);
"""

try:
    cur.execute(create_table_sql)
    print("Table created")
    conn.commit()
    cur.execute(copy_sql)
    conn.commit()
    print("Data copied")
except Exception as e:
    print("Error: ", e)
    conn.rollback()
finally:
    cur.close()
    conn.close()