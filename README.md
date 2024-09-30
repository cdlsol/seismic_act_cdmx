#Seismic activity in CDMX data pipeline practice project focused on Data Ingestion 


This is a guided project to stablish a pipeline with the source being https://www.kaggle.com/datasets/vladimirgc/mexico-city-earthquakes-2020-2024. I first used the Kaggle API to download the needed csv file.

For Database, I used Postgresql, which will be set-up via Docker Container.

In order to run the containerized pipeline, you need to execute the following command:

CSV_PATH="sismologico_CDMX.csv"
docker run -it \
    --network=seismic_act_cdmx_default \
    python_test:001 \
    --user=root \
    --password=root \
    --host=seismic_act_cdmx-pgdatabase-1 \
    --port 5432 \
    --db=sismos24 \
    --table=seismic24 \
    --csv_path=${CSV_PATH}

*You can review the data in the DB by going to https://localhost:8080
