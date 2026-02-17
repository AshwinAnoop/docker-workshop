import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

#sqlalchemy is used to connect to the Postgres database
#tqdm is used to show progress bars during data ingestion
#click is used to create a command-line interface for the script, allowing us to specify parameters such as the year and month of the data to ingest.

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

@click.command()
@click.option("--year", default=2021, help="Year of the data to ingest")
@click.option("--month", default=1, help="Month of the data to ingest")
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
@click.option('--chunk-size', default=100000, help='Number of rows to process in each chunk')

def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table, chunk_size, year, month):

    # Create the connection string
    engine = create_engine(
        f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )

    prefix = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/"
    url = f"{prefix}yellow_tripdata_{year:04d}-{month:02d}.csv.gz"
    
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
