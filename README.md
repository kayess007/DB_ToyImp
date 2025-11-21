Start docker

Create container:
    move to folder containing docker-compose.yml
    run "docker compose up -d"

Start container:
    docker start pg_local
    docker start cassandra_local

Stop container:
    docker stop pg_local
    docker stop cassandra_local

To interact with DB manually or test
Connect to SQL Shell:
    docker exec -it pg_local psql -U admin -d welllogs

Connect to Cassandra Shell:
    docker exec -it cassandra_local cqlsh

