Install Docker Desktop
Start docker

Create container:
    move to folder containing docker-compose.yml
    run "docker compose up -d"

At this point, when you open docker desktop you can see a volume "db_toyimp" with 2 containers in it:
- pg_local
- cassandra_local
If they are not running then press start button for both of them

Wait for the containers to start

Open a terminal in the code repository folder, then run:
docker exec -it pg_local psql -U admin -d welllogs
to access the interface for Postgres DB Shell

If the DB is empty (you have just created the container):
    Init DB:
        Create tables: Copy the queries in wellv2.sql into the terminal and run
        Create default mnemonics: Copy the queries in well_mnemonic.sql and mnemonic_name.sql into the terminal and run

Now that you have all the tables, and a dictionary table for mnemonics
Start by creating the first well. From vscode terminal, run: python create_well.py (this create the well Hibernia B-16 2Z)
Next, fill the DB with data from LAS files for Hibernia B-16 2Z: 
- download LAS-file name LAS-017963 from Hibernia B-16 2Z and put to the code repository
- run: python las_parser.py 

After this step, you have filled the database with data for Hibernia B-16 2Z

You can query directly using the Postgres DB Shell we started from above, such as: select * from well_curve;
I recommend you explore queries using the SQL shell above.

Or there are 3 search functions in well_query.py:
- get_well_metadata(uwi)
- get_well_info(uwi)
- get_curve_in_range(mnemonic, start, stop, uwi)
- get_curve_data(uwi, mnemonics)

I'm integrating the UI, so I don't know whether it is correct or not.

Connect to Cassandra Shell:
    docker exec -it cassandra_local cqlsh


