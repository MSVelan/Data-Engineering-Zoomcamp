import pandas as pd
import sys

# Do something with pandas
# I ran the following in the terminal
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
    --name pg-database \
    dpage/pgadmin4
"""
print(sys.argv)

date = sys.argv[1]

print(f"Succesfully loaded pandas, we can execute this on given day= {date}")
