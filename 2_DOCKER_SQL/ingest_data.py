import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # download the csv
    csv_name = "output.csv"

    os.system(f"wget {url} -O {csv_name}.gz")
    os.system(f"gzip -d {csv_name}.gz")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)

    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")
    df.to_sql(name=table_name, con=engine, if_exists="append")

    cnt = 0
    while True:
        df = next(df_iter)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        t1 = time()
        df.to_sql(name=table_name, con=engine, if_exists="append")
        t2 = time()
        cnt += 1
        print(f"inserted chunk: {cnt}, time taken: {t2-t1} seconds.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")
    # User, Password, Host, Port, database name, table name, url of the csv file
    parser.add_argument("--user", help="username for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="database name for postgres")
    parser.add_argument(
        "--table_name", help="name of the table where we write results to"
    )
    parser.add_argument("--url", help="url of the csv file")

    args = parser.parse_args()
    main(args)

    """
    docker run -it \
        -e POSTGRES_USER="root" \
        -e POSTGRES_PASSWORD="root" \
        -e POSTGRES_DB="ny_taxi" \
        -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
        -p 5432:5432 \
        postgres:13

    to create the postgres container and then to run postgres use

    pgcli -h localhost -p 5432 -u root -d ny_taxi

    we can also use pgadmin (web based GUI) to connect to the postgres container

    docker run -it \
        -e POSTGRES_USER="root" \
        -e POSTGRES_PASSWORD="root" \
        -e POSTGRES_DB="ny_taxi" \
        -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
        -p 5432:5432 \
        --network=pg_network \
        --name pg-database \
        postgres:13

    docker run -it \
        -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
        -e PGADMIN_DEFAULT_PASSWORD="root" \
        -p 8080:80 \
        dpage/pgadmin4

    create a network to connect the two containers, so now the command changes as follows:

    docker network create pg_network

    docker run -it \
        -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
        -e PGADMIN_DEFAULT_PASSWORD="root" \
        -p 8080:80 \
        --network=pg_network \
        --name pgadmin \
        dpage/pgadmin4
    
    To create the table using this file run the following:
    URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
    python ingest_data.py \
        --user=root \
        --password=root \
        --host=localhost \
        --port=5432 \
        --db=ny_taxi \
        --table_name=yellow_taxi_trips \
        --url=${URL}
    
    To dockerize the ingest_data.py file,
    I have changed the Dockerfile and then build using: docker build -t taxi_ingest:v001 .
    docker run -it \
      --network=pg-network \
      taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=<local-ip-address> \
        --port=5432 \
        --db=ny_taxi \
        --table_name=yellow_taxi_trips \
        --url=${URL}
    
    To use the docker-compose file, run the following:
    docker compose up -d
    
    Then run the dockerized program:
    docker run -it taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=pg-database \
        --port=5432 \
        --db=ny_taxi \
        --table_name=yellow_taxi_trips \
        --url=${URL}

    This is convenient since, we need not run all the containers that are required for the program manually.
    """
