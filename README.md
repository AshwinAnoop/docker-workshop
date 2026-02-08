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
