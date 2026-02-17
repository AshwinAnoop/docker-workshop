# docker-workshop

Workshop codespaces — utilities for running a local Postgres instance in Docker for the ny_taxi example.

## Start a Postgres container

Run Postgres in Docker with the following command. This creates (or reuses) a Docker volume named `ny_taxi_postgres_data` to persist database files and exposes Postgres on port 5432.

```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

Notes:
- `--rm` removes the container when it stops. Remove it if you want the container to remain.
- The volume `ny_taxi_postgres_data` keeps DB files between container restarts.

## Connect to the database

You can connect using `pgcli` (a user-friendly Postgres CLI). If you don't have it, install with `uv add --dev pgcli` in the `pipeline` directory.

```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```


## To install sqlalchemy and psycopg in the pipeline environment

```bash
uv add sqlalchemy "psycopg[binary,pool]"
````

## To install tqdm in the pipeline environment which is useful for progress bars
```bash 
uv add tqdm
```

## To run the data ingestion script with the appropriate parameters to ingest data into your local Postgres instance. This CLI Parameters are introduced using `click` in the `ingest-data.py` script.
```bash
uv run python ingest-data.py \
  --year 2021 \
  --month 1 \
  --pg-user root \
  --pg-pass root \
  --pg-host localhost \
  --pg-port 5432 \
  --pg-db ny_taxi \
  --target-table yellow_taxi_data \
  --chunk-size 100000
```

## Command to build the Docker image for the data ingestion script.
```bash
docker build -t taxi_ingest:v001 .
```

## Run PostgreSQL on the network

### create the network
```bash
docker network create pg-network
```

### run PostgreSQL on the network
```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:18
```

## Run the data ingestion script in a container on the same network to connect to PostgreSQL using the hostname `pgdatabase` (the name of the Postgres container).

```bash
docker run -it --rm \
  --network=pg-network \
  taxi_ingest:v001 \
  --year 2021 \
  --month 1 \
  --pg-user root \
  --pg-pass root \
  --pg-host pgdatabase \
  --pg-port 5432 \
  --pg-db ny_taxi \
  --target-table yellow_taxi_data \
  --chunk-size 100000
```

## Run pgAdmin on the same network to connect to PostgreSQL using the hostname `pgdatabase`.
pg admin is a web-based GUI for managing PostgreSQL databases. The following command runs pgAdmin in a Docker container, connects it to the same `pg-network`, and exposes it on port 8085.

```bash
docker run -it --rm \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

once pgAdmin is running, you can access it in your web browser at `http://localhost:8085`. Log in with the email `admin@admin.com` and password `root`. Then, Register a new server connection with the following details:
- Name: `PostgreSQL` (any name you like)
- Hostname/address: `pgdatabase`
- Port: `5432`
- Username: `root`
- Password: `root`