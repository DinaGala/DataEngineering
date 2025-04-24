import os
from datetime import datetime
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.types import (
    Integer, BigInteger, Float, String, Boolean, DateTime, UUID as PG_UUID
)
from uuid import UUID

CSV_PATH = '/home/nzhuzhle/Downloads/data/customer/'
engine = create_engine('postgresql://nzhuzhle:mysecretpassword@localhost:5432/piscineds')

# Path to the 'customer' folder relative to this script
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(CSV_PATH)
print(CSV_DIR)

def is_valid_uuid(val):
    try:
        return str(UUID(val)) == val
    except (ValueError, TypeError):
        return False

def map_dtype(col_name, series):
    if pd.api.types.is_integer_dtype(series):
        return BigInteger()
    elif pd.api.types.is_float_dtype(series):
        return Float()
    elif pd.api.types.is_bool_dtype(series):
        return Boolean()
    elif pd.api.types.is_datetime64_any_dtype(series):
        return DateTime(timezone=True)
    elif series.apply(is_valid_uuid).all():
        return PG_UUID()
    else:
        return String()

def create_table_and_import_data(csv_file_path, table_name):
    
    df_sample = pd.read_csv(csv_file_path, nrows=1, low_memory=False)

    headers = list(df_sample.columns)
    dtype_mapping = {
        headers[0]: DateTime(timezone=True)
    }

    for header in headers[1:]:
        dtype_mapping[header] = map_dtype(header, df_sample[header])
    
    df_full = pd.read_csv(csv_file_path, nrows=1, low_memory=False)

    df_full.to_sql(
        name=table_name,
        con=engine,
        if_exists='replace',
        index=False,
        dtype=dtype_mapping
    )
    

def main():

    if not os.path.isdir(CSV_DIR):
        raise RuntimeError(f"CSV directory not found: {CSV_DIR}")
    
    for filename in os.listdir(CSV_DIR):
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(CSV_DIR, filename)
            table_name = os.path.splitext(filename)[0].lower().replace(' ', '_') 
            print(f"Processing file: {filename} -> Table: {table_name}")
            create_table_and_import_data(csv_file_path, table_name)
            print(f"Table '{table_name}' created and data imported successfully.")

    print(f"All tables are created and copied.")

if __name__ == '__main__':
    main()