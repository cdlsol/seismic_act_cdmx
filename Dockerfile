FROM python:3.9

WORKDIR /app
RUN pip install pandas sqlalchemy psycopg2-binary
RUN mkdir -p /home/cdlzs/seismic24/maps
COPY sismologico_CDMX.csv sismologico_CDMX.csv
COPY dataingest.py dataingest.py
COPY query_seismic_data.py query_seismic_data.py 

ENTRYPOINT [ "python","dataingest.py" ]

# docker run -it \
#     -e POSTGRES_USER="root" \
#     -e POSTGRES_PASSWORD="root" \
#     -e POSTGRES_DB="sismos24" \
#     -v "/home/cdlzs/seismic24/seismic_act_cdmx/postgres_data:/var/lib/postgresql/data:rw" \
#     -p 5432:5432 \
#     --network=pg-network \
#     --name=pg-database \
#     postgres:13

# CSV_PATH="sismologico_CDMX.csv"
# docker run -it \
#     --network=seismic_act_cdmx_default \
#     python_test:001 \
#     --user=root \
#     --password=root \
#     --host=seismic_act_cdmx-pgdatabase-1 \
#     --port 5432 \
#     --db=sismos24 \
#     --table=seismic24 \
#     --csv_path=${CSV_PATH}