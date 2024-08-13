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
"""
print(sys.argv)

date = sys.argv[1]

print(f"Succesfully loaded pandas, we can execute this on given day= {date}")
