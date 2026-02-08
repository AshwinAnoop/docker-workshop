import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

#sqlalchemy is used to connect to the Postgres database
#tqdm is used to show progress bars during data ingestion

# Define the data types for each column
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

# Define the columns to parse as dates
parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
]



def run():

    year = 2021
    month = 1

    pg_user = "root"
    pg_pass = "root"
    pg_host = "localhost"
    pg_port = 5432
    pg_db = "ny_taxi"


    # Create the connection string
    engine = create_engine(
        f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )

    prefix = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/"
    url = f"{prefix}yellow_tripdata_{year:04d}-{month:02d}.csv.gz"
    target_table = "yellow_taxi_data"

    # Read the CSV file in chunks
    chunk_size = 100000
    
    df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=chunk_size,
    )

    # Initialize a flag to indicate the first chunk
    first = True

    for df_chunk in tqdm(df_iter, desc="Ingesting data", unit="chunk"):

        # Write the chunk to the database
        if first:
            df_chunk.head(0).to_sql(name=target_table, con=engine, if_exists="replace")
            first = False

        df_chunk.to_sql(name=target_table, con=engine, if_exists="append")
        
if __name__ == "__main__":
    print("Starting data ingestion...")
    run()
    print("Data ingestion completed.")
