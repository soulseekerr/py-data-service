# py-data-service

### Install virtual env
In a terminal, execute the following commands.
> python3 -m venv .venv
> source .venv/bin/activate
> pip list
pip     24.3.1
> pip -m pip install --upgrade pip
> pip install --upgrade pip
pip     26.1.2


(*) api → Python app (FastAPI) served by uvicorn, connecting to the Postgres DB via service name db.

create folder 'api'
create requirements.txt in api

fastapi
uvicorn[standard]
psycopg[binary]
psycopg_pool
pydantic
pandas
pyarrow
duckdb
numpy
pandera
python-multipart

> pip install -r requirements.txt

create folder 'streamlit'
create requirements.txt in streamlit

streamlit
streamlit-autorefresh
requests
pandas
numpy

> pip install -r requirements.txt

create docker files for api and streamlit

create docker compose file
...
...
[+] Running 9/9
 ✔ py-data-service-api                    B...                       0.0s 
 ✔ py-data-service-streamlit              Built                      0.0s 
 ✔ Network py-data-service_default        Created                    0.0s 
 ✔ Volume "py-data-service_pgadmin_data"  Created                    0.0s 
 ✔ Volume "py-data-service_db_data"       Created                    0.0s 
 ✔ Container py-data-service-db-1         Healthy                    5.8s 
 ✔ Container py-data-service-api-1        Started                    5.9s 
 ✔ Container py-data-service-pgadmin-1    Started                    5.9s 
 ✔ Container py-data-service-streamlit-1  Started                    6.0s

 ## Testing

docker compose down --volumes --remove-orphans
docker compose up -d --build
docker compose logs -f db
docker compose ps
docker compose exec api sh -lc 'ls -lh data' 

docker compose down api
docker compose build api
docker compose up -d --build
docker compose logs -f api
docker compose down -v && docker compose up -d --build

docker compose down streamlit && docker compose up streamlit -d --build

docker compose exec api find /app/mock_data -maxdepth 3 -type f
