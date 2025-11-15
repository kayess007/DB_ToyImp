# import lasio
# import numpy
# import sqlite3
# import pandas as pd

# # Step 1: Parse LAS file locally
# las = lasio.read_csv(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS-011752.csv")
# df = las.df()  # Convert LAS curves to DataFrame, index is depth

# # Step 2: Prepare DataFrame
# df.reset_index(inplace=True)
# df.rename(columns={'index': 'depth'}, inplace=True)

# # Step 3: Create SQLite DB and tables
# conn = sqlite3.connect('toy_las_system.db')
# cursor = conn.cursor()

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Wells (
#     well_id INTEGER PRIMARY KEY,
#     well_name TEXT
# )
# ''')

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS LogData (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     well_id INTEGER,
#     depth REAL,
#     ''' + ', '.join([f'"{col}" REAL' for col in df.columns if col != 'depth']) + ''',
#     FOREIGN KEY(well_id) REFERENCES Wells(well_id)
# )
# ''')

# conn.commit()

# # Step 4: Insert well info (toy example)
# well_id = 1
# well_name = las.well.WELL.value if hasattr(las.well, 'WELL') else 'Sample Well'
# cursor.execute('INSERT OR IGNORE INTO Wells (well_id, well_name) VALUES (?, ?)', (well_id, well_name))
# conn.commit()

# # Step 5: Insert log data
# insert_query = f'''
# INSERT INTO LogData (well_id, depth, {', '.join([f'"{col}"' for col in df.columns if col != 'depth'])})
# VALUES ({', '.join(['?'] * (len(df.columns) + 1))})
# '''

# data_to_insert = []
# for _, row in df.iterrows():
#     values = [well_id, row['depth']] + [row[col] for col in df.columns if col != 'depth']
#     data_to_insert.append(values)

# cursor.executemany(insert_query, data_to_insert)
# conn.commit()

# # Step 6: Verify by querying a few entries
# for row in cursor.execute('SELECT * FROM LogData LIMIT 5'):
#     print(row)

# conn.close()



# import lasio
# import sqlite3
# import pandas as pd

# # Step 1: Parse LAS / LAS-derived CSV
# las = lasio.read_csv(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS-011752.csv")
# df = las.df()

# # Step 2: Prepare DataFrame
# df = df.reset_index().rename(columns={"index": "depth"})

# # Optional: convert NaNs to None for nicer NULLs in SQLite
# df = df.where(pd.notnull(df), None)

# with sqlite3.connect("toy_las_system.db") as conn:
#     cursor = conn.cursor()

#     # Wells table
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS Wells (
#         well_id   INTEGER PRIMARY KEY,
#         well_name TEXT
#     )
#     """)

#     # LogData table with dynamic curve columns
#     curve_cols = [col for col in df.columns if col != "depth"]
#     curve_defs = ", ".join([f'"{col}" REAL' for col in curve_cols])

#     cursor.execute(f"""
#     CREATE TABLE IF NOT EXISTS LogData (
#         id      INTEGER PRIMARY KEY AUTOINCREMENT,
#         well_id INTEGER,
#         depth   REAL,
#         {curve_defs},
#         FOREIGN KEY (well_id) REFERENCES Wells(well_id)
#     )
#     """)

#     # Insert well
#     well_id = 1
#     well_name = getattr(getattr(las, "well", None), "WELL", None)
#     well_name = getattr(well_name, "value", None) or "Sample Well"

#     cursor.execute(
#         "INSERT OR IGNORE INTO Wells (well_id, well_name) VALUES (?, ?)",
#         (well_id, well_name),
#     )

#     # Build insert
#     col_list = ", ".join([f'"{c}"' for c in curve_cols])
#     placeholders = ", ".join(["?"] * (len(curve_cols) + 2))  # well_id + depth + curves

#     insert_query = f"""
#     INSERT INTO LogData (well_id, depth, {col_list})
#     VALUES ({placeholders})
#     """

#     # Data to insert
#     data_to_insert = []
#     for _, row in df.iterrows():
#         values = [well_id, row["depth"]] + [row[c] for c in curve_cols]
#         data_to_insert.append(values)

#     cursor.executemany(insert_query, data_to_insert)

#     # Verify
#     for row in cursor.execute("SELECT * FROM LogData LIMIT 5"):
#         print(row)



# import sqlite3
# import pandas as pd

# # =====================================================
# # Step 1: Load LAS-style CSV into a DataFrame
# # =====================================================
# csv_path = r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS-011752.csv"

# df = pd.read_csv(csv_path)

# # Assume the first column is depth → rename it to "depth"
# # (Change this if your file already has a proper depth column name)
# df.rename(columns={df.columns[0]: "depth"}, inplace=True)

# # Convert all non-depth columns to numeric (coerce errors to NaN)
# for col in df.columns:
#     if col != "depth":
#         df[col] = pd.to_numeric(df[col], errors="coerce")

# # Optional: replace NaN with None so SQLite stores NULL
# df = df.where(pd.notnull(df), None)

# # =====================================================
# # Step 2: Create SQLite DB and tables
# # =====================================================
# conn = sqlite3.connect("toy_las_system.db")
# cursor = conn.cursor()

# # Wells table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Wells (
#     well_id   INTEGER PRIMARY KEY,
#     well_name TEXT
# )
# """)

# # LogData table with dynamic curve columns
# curve_cols = [col for col in df.columns if col != "depth"]
# curve_defs = ", ".join([f'"{col}" REAL' for col in curve_cols])

# cursor.execute(f"""
# CREATE TABLE IF NOT EXISTS LogData (
#     id      INTEGER PRIMARY KEY AUTOINCREMENT,
#     well_id INTEGER,
#     depth   REAL,
#     {curve_defs},
#     FOREIGN KEY (well_id) REFERENCES Wells(well_id)
# )
# """)

# conn.commit()

# # =====================================================
# # Step 3: Insert well info (toy example)
# # =====================================================
# well_id = 1
# well_name = "Well_011752"   # You can change this to something better

# cursor.execute(
#     "INSERT OR IGNORE INTO Wells (well_id, well_name) VALUES (?, ?)",
#     (well_id, well_name),
# )
# conn.commit()

# # =====================================================
# # Step 4: Insert log data into LogData
# # =====================================================
# # Build the INSERT query
# col_list = ", ".join([f'"{c}"' for c in curve_cols])
# # number of placeholders = well_id + depth + curve columns
# placeholders = ", ".join(["?"] * (len(curve_cols) + 2))

# insert_query = f"""
# INSERT INTO LogData (well_id, depth, {col_list})
# VALUES ({placeholders})
# """

# # Prepare data rows
# data_to_insert = []
# for _, row in df.iterrows():
#     values = [well_id, row["depth"]] + [row[c] for c in curve_cols]
#     data_to_insert.append(values)

# # Bulk insert
# cursor.executemany(insert_query, data_to_insert)
# conn.commit()

# # =====================================================
# # Step 5: Verify a few rows
# # =====================================================
# for row in cursor.execute("SELECT * FROM LogData LIMIT 5"):
#     print(row)

# conn.close()



# import sqlite3
# import pandas as pd

# # =====================================================
# # Step 1: Load LAS-style CSV into a DataFrame
# # =====================================================
# csv_path = r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS-011752.csv"
# print(f"Reading CSV from: {csv_path}")

# df = pd.read_csv(csv_path)
# print("Original columns:", df.columns.tolist())

# # Assume the first column is depth → rename it to "depth"
# if "depth" not in df.columns:
#     df.rename(columns={df.columns[0]: "depth"}, inplace=True)

# print("Columns after renaming first to 'depth' if needed:", df.columns.tolist())

# # Convert all non-depth columns to numeric (coerce errors to NaN)
# for col in df.columns:
#     if col != "depth":
#         df[col] = pd.to_numeric(df[col], errors="coerce")

# # Optional: replace NaN with None so SQLite stores NULL
# df = df.where(pd.notnull(df), None)

# print("Preview of data (first 5 rows):")
# print(df.head())

# # =====================================================
# # Step 2: Create SQLite DB and tables
# # =====================================================
# print("\nConnecting to SQLite database: toy_las_system.db")
# conn = sqlite3.connect("toy_las_system.db")
# cursor = conn.cursor()

# # Wells table
# print("Creating Wells table (if not exists)")
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Wells (
#     well_id   INTEGER PRIMARY KEY,
#     well_name TEXT
# )
# """)

# # LogData table with dynamic curve columns
# curve_cols = [col for col in df.columns if col != "depth"]
# print("Curve columns detected:", curve_cols)

# # If there are no curve columns, we should stop – nothing to store
# if not curve_cols:
#     raise ValueError("No curve columns found besides 'depth'. Check your CSV.")

# curve_defs = ", ".join([f'"{col}" REAL' for col in curve_cols])

# # Drop old LogData so schema always matches current CSV
# print("Dropping old LogData table (if it exists) to avoid schema mismatch")
# cursor.execute("DROP TABLE IF EXISTS LogData")

# print("Creating LogData table")
# cursor.execute(f"""
# CREATE TABLE LogData (
#     id      INTEGER PRIMARY KEY AUTOINCREMENT,
#     well_id INTEGER,
#     depth   REAL,
#     {curve_defs},
#     FOREIGN KEY (well_id) REFERENCES Wells(well_id)
# )
# """)

# conn.commit()
# print("Tables created/updated successfully.\n")

# # =====================================================
# # Step 3: Insert well info (toy example)
# # =====================================================
# well_id = 1
# well_name = "Well_011752"   # You can change this to something better

# print(f"Inserting well info: well_id={well_id}, well_name={well_name}")
# cursor.execute(
#     "INSERT OR IGNORE INTO Wells (well_id, well_name) VALUES (?, ?)",
#     (well_id, well_name),
# )
# conn.commit()
# print("Well info inserted.\n")

# # =====================================================
# # Step 4: Insert log data into LogData
# # =====================================================
# # Build the INSERT query
# col_list = ", ".join([f'"{c}"' for c in curve_cols])
# # number of placeholders = well_id + depth + curve columns
# placeholders = ", ".join(["?"] * (len(curve_cols) + 2))

# insert_query = f"""
# INSERT INTO LogData (well_id, depth, {col_list})
# VALUES ({placeholders})
# """

# print("Insert query:")
# print(insert_query)

# # Prepare data rows
# data_to_insert = []
# for _, row in df.iterrows():
#     values = [well_id, row["depth"]] + [row[c] for c in curve_cols]
#     data_to_insert.append(values)

# print(f"\nPrepared {len(data_to_insert)} rows for insert.")

# # Bulk insert
# try:
#     cursor.executemany(insert_query, data_to_insert)
#     conn.commit()
#     print(f"Inserted {len(data_to_insert)} rows into LogData.\n")
# except Exception as e:
#     print("Error during bulk insert:")
#     print(e)
#     conn.rollback()
#     conn.close()
#     raise

# # =====================================================
# # Step 5: Verify a few rows
# # =====================================================
# print("First 5 rows from LogData:")
# for row in cursor.execute("SELECT * FROM LogData LIMIT 5"):
#     print(row)

# conn.close()
# print("\nDone. Connection closed.")



# import lasio
# import sqlite3
# import pandas as pd

# # =====================================================
# # Step 1: Load LAS file with lasio
# # =====================================================
# las_path = r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS-011752.csv"  # extension doesn't matter if content is LAS
# print(f"Reading LAS from: {las_path}")

# las = lasio.read(las_path)   
# df = las.df()                

# print("Columns from LAS curves:", df.columns.tolist())
# print("Index name (depth):", df.index.name)


# df = df.reset_index().rename(columns={df.index.name or "index": "depth"})
# print("Columns after reset_index:", df.columns.tolist())

# for col in df.columns:
#     if col != "depth":
#         df[col] = pd.to_numeric(df[col], errors="coerce")


# df = df.where(pd.notnull(df), None)

# print("Preview of data (first 5 rows):")
# print(df.head())


# print("\nConnecting to SQLite database: toy_las_system.db")
# conn = sqlite3.connect("toy_las_system.db")
# cursor = conn.cursor()


# print("Creating Wells table (if not exists)")
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Wells (
#     well_id   INTEGER PRIMARY KEY,
#     well_name TEXT
# )
# """)


# curve_cols = [col for col in df.columns if col != "depth"]
# print("Curve columns detected:", curve_cols)

# if not curve_cols:
#     raise ValueError("No curve columns detected from LAS. Something is wrong with the LAS file.")

# curve_defs = ", ".join([f'"{col}" REAL' for col in curve_cols])


# print("Dropping old LogData table (if it exists)")
# cursor.execute("DROP TABLE IF EXISTS LogData")

# print("Creating LogData table")
# cursor.execute(f"""
# CREATE TABLE LogData (
#     id      INTEGER PRIMARY KEY AUTOINCREMENT,
#     well_id INTEGER,
#     depth   REAL,
#     {curve_defs},
#     FOREIGN KEY (well_id) REFERENCES Wells(well_id)
# )
# """)

# conn.commit()
# print("Tables created/updated successfully.\n")


# well_id = 1

# try:
#     well_name = las.well.WELL.value
#     if not well_name:
#         well_name = "Well_011752"
# except Exception:
#     well_name = "Well_011752"

# print(f"Inserting well info: well_id={well_id}, well_name={well_name}")
# cursor.execute(
#     "INSERT OR IGNORE INTO Wells (well_id, well_name) VALUES (?, ?)",
#     (well_id, well_name),
# )
# conn.commit()
# print("Well info inserted.\n")

# print("Preparing INSERT for LogData")

# col_list = ", ".join([f'"{c}"' for c in curve_cols])
# placeholders = ", ".join(["?"] * (len(curve_cols) + 2))  # well_id + depth + curves

# insert_query = f"""
# INSERT INTO LogData (well_id, depth, {col_list})
# VALUES ({placeholders})
# """

# print("Insert query:")
# print(insert_query)

# data_to_insert = []
# for _, row in df.iterrows():
#     values = [well_id, row["depth"]] + [row[c] for c in curve_cols]
#     data_to_insert.append(values)

# print(f"\nPrepared {len(data_to_insert)} rows for insert.")

# try:
#     cursor.executemany(insert_query, data_to_insert)
#     conn.commit()
#     print(f"Inserted {len(data_to_insert)} rows into LogData.\n")
# except Exception as e:
#     print("Error during bulk insert:")
#     print(e)
#     conn.rollback()
#     conn.close()
#     raise


# print("First 5 rows from LogData:")
# for row in cursor.execute("SELECT * FROM LogData LIMIT 5"):
#     print(row)

# conn.close()
# print("\nDone. Connection closed.")


# import lasio
# import sqlite3
# import pandas as pd

# # =====================================================
# # Step 1: Load LAS file with lasio
# # =====================================================
# las_path = r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS-011752.csv"  # extension ok
# print(f"Reading LAS from: {las_path}")

# las = lasio.read(las_path)
# df = las.df()                # curves DataFrame, index = depth

# # Move depth index into a column
# df = df.reset_index().rename(columns={df.index.name or "index": "depth"})

# # Convert non-depth columns to numeric
# for col in df.columns:
#     if col != "depth":
#         df[col] = pd.to_numeric(df[col], errors="coerce")

# # Replace NaNs with None for SQLite
# df = df.where(pd.notnull(df), None)


# # =====================================================
# # Step 2: Create SQLite DB and updated Wells table
# # =====================================================
# print("\nConnecting to SQLite database: toy_las_system.db")
# conn = sqlite3.connect("toy_las_system.db")
# cursor = conn.cursor()

# # Drop old Wells + LogData for clean rebuild
# cursor.execute("DROP TABLE IF EXISTS LogData")
# cursor.execute("DROP TABLE IF EXISTS Wells")

# # -----------------------------------------------------
# # UPDATED WELLS TABLE WITH ALL FIELDS YOU LISTED
# # -----------------------------------------------------
# cursor.execute("""
# CREATE TABLE Wells (
#     well_id             INTEGER PRIMARY KEY,
#     well_name           TEXT NOT NULL,
#     operator            TEXT,
#     reentry_times       INTEGER,
#     surface_lat_nad83   REAL,
#     surface_long_nad83  REAL,
#     land_tenure_area    TEXT,
#     well_classification TEXT,
#     datum               TEXT,
#     datum_elevation     REAL,
#     earliest_spud_date  DATE,
#     latest_release_date DATE
# );
# """)
# print("Created updated Wells table.")


# # =====================================================
# # Step 3: Create LogData table based on curves
# # =====================================================
# curve_cols = [col for col in df.columns if col != "depth"]
# curve_defs = ", ".join([f'"{col}" REAL' for col in curve_cols])

# cursor.execute(f"""
# CREATE TABLE LogData (
#     id       INTEGER PRIMARY KEY AUTOINCREMENT,
#     well_id  INTEGER,
#     depth    REAL,
#     {curve_defs},
#     FOREIGN KEY (well_id) REFERENCES Wells(well_id)
# );
# """)
# print("Created LogData table.")


# # =====================================================
# # Step 4: Insert full well information
# # =====================================================

# # Extract well name if available
# try:
#     well_name = las.well.WELL.value or "Unknown Well"
# except:
#     well_name = "Unknown Well"

# # You can later modify these or ingest from metadata CSV
# well_data = {
#     "well_id": 1,
#     "well_name": well_name,
#     "operator": "Unknown Operator",
#     "reentry_times": 0,
#     "surface_lat_nad83": None,
#     "surface_long_nad83": None,
#     "land_tenure_area": None,
#     "well_classification": None,
#     "datum": None,
#     "datum_elevation": None,
#     "earliest_spud_date": None,
#     "latest_release_date": None
# }

# cursor.execute("""
# INSERT INTO Wells (
#     well_id, well_name, operator, reentry_times,
#     surface_lat_nad83, surface_long_nad83,
#     land_tenure_area, well_classification,
#     datum, datum_elevation,
#     earliest_spud_date, latest_release_date
# ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
# """, tuple(well_data.values()))

# print("Inserted well metadata.")


# # =====================================================
# # Step 5: Insert log curve data
# # =====================================================
# col_list = ", ".join([f'"{c}"' for c in curve_cols])
# placeholders = ", ".join(["?"] * (len(curve_cols) + 2))  # well_id + depth + curves

# insert_query = f"""
# INSERT INTO LogData (well_id, depth, {col_list})
# VALUES ({placeholders})
# """

# data_to_insert = []
# for _, row in df.iterrows():
#     values = [1, row["depth"]] + [row[c] for c in curve_cols]
#     data_to_insert.append(values)

# cursor.executemany(insert_query, data_to_insert)
# conn.commit()

# print(f"Inserted {len(data_to_insert)} log rows.\n")


# # =====================================================
# # Step 6: Verify
# # =====================================================
# print("=== Wells Table ===")
# print(pd.read_sql_query("SELECT * FROM Wells", conn))

# print("\n=== LogData (first 5 rows) ===")
# print(pd.read_sql_query("SELECT * FROM LogData LIMIT 5", conn))

# conn.close()
# print("\nDone. Database updated successfully.")




# import lasio
# import sqlite3
# import pandas as pd
# from pathlib import Path

# DB_PATH = "toy_las_system.db"
# LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")


# def ingest_las_file(las_path: Path):
#     print(f"\n=== Ingesting: {las_path.name} ===")

#     # --- Load LAS ---
#     las = lasio.read(las_path)
#     df = las.df().reset_index().rename(columns={las.df().index.name or "index": "depth"})

#     # Convert numeric columns
#     for col in df.columns:
#         if col != "depth":
#             df[col] = pd.to_numeric(df[col], errors="coerce")

#     df = df.where(pd.notnull(df), None)

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # -------------------------
#     # Insert WELL METADATA
#     # -------------------------

#     # Try to extract the well name from LAS header
#     try:
#         well_name = las.well.WELL.value or las_path.stem
#     except:
#         well_name = las_path.stem

#     well_meta = (
#         well_name,          # well_name
#         None,               # operator
#         0,                  # reentry_times
#         None, None,         # lat/long
#         None,               # land tenure
#         None,               # classification
#         None,               # datum
#         None,               # datum elevation
#         None, None          # spud date, release date
#     )

#     cursor.execute("""
#         INSERT INTO Wells (
#             well_name, operator, reentry_times,
#             surface_lat_nad83, surface_long_nad83,
#             land_tenure_area, well_classification,
#             datum, datum_elevation,
#             earliest_spud_date, latest_release_date
#         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, well_meta)

#     well_id = cursor.lastrowid
#     print(f"Assigned well_id={well_id} to {well_name}")

#     # -------------------------
#     # Insert LOG DATA
#     # -------------------------
#     curve_cols = [c for c in df.columns if c != "depth"]
#     col_list = ", ".join([f'"{c}"' for c in curve_cols])
#     placeholders = ", ".join(["?"] * (len(curve_cols) + 2))  # well_id + depth + curves

#     insert_query = f"""
#     INSERT INTO LogData (well_id, depth, {col_list})
#     VALUES ({placeholders})
#     """

#     rows = []
#     for _, row in df.iterrows():
#         rows.append([well_id, row["depth"]] + [row[c] for c in curve_cols])

#     cursor.executemany(insert_query, rows)
#     conn.commit()
#     conn.close()

#     print(f"Inserted {len(rows)} rows for well: {well_name}")


# def setup_database():
#     """Create tables if not existing."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # Wells table
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS Wells (
#         well_id             INTEGER PRIMARY KEY AUTOINCREMENT,
#         well_name           TEXT NOT NULL,
#         operator            TEXT,
#         reentry_times       INTEGER,
#         surface_lat_nad83   REAL,
#         surface_long_nad83  REAL,
#         land_tenure_area    TEXT,
#         well_classification TEXT,
#         datum               TEXT,
#         datum_elevation     REAL,
#         earliest_spud_date  DATE,
#         latest_release_date DATE
#     );
#     """)

#     # LogData table
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS LogData (
#         id       INTEGER PRIMARY KEY AUTOINCREMENT,
#         well_id  INTEGER,
#         depth    REAL,
#         ATR      REAL,
#         BS       REAL,
#         GR_CDR   REAL,
#         PSR      REAL,
#         FOREIGN KEY (well_id) REFERENCES Wells(well_id)
#     );
#     """)

#     conn.commit()
#     conn.close()


# if __name__ == "__main__":
#     setup_database()

#     las_files = list(LAS_DIR.glob("*.las")) + list(LAS_DIR.glob("*.csv"))
#     print(f"Found {len(las_files)} LAS files to ingest.")

#     for file in las_files:
#         ingest_las_file(file)

#     print("\n=== Ingestion Completed ===")


# import lasio
# import sqlite3
# import pandas as pd
# from pathlib import Path

# DB_PATH = "toy_las_system.db"
# LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")


# def get_union_of_curves(las_files):
#     """Scan all LAS files and return the union of all curve names."""
#     all_curves = set()

#     for f in las_files:
#         print(f"Scanning curves in: {f.name}")
#         las = lasio.read(f)
#         df_curves = las.df()
#         all_curves.update(df_curves.columns.tolist())

#     curve_list = sorted(all_curves)
#     print("\nUnified curve list across all files:")
#     print(curve_list)
#     return curve_list


# def setup_database(curve_cols):
#     """Create (or recreate) Wells and LogData tables based on union of curve columns."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # Drop existing tables so schema always matches our union
#     cursor.execute("DROP TABLE IF EXISTS LogData")
#     cursor.execute("DROP TABLE IF EXISTS Wells")

#     # Wells table with rich metadata
#     cursor.execute("""
#     CREATE TABLE Wells (
#         well_id             INTEGER PRIMARY KEY AUTOINCREMENT,
#         well_name           TEXT NOT NULL,
#         operator            TEXT,
#         reentry_times       INTEGER,
#         surface_lat_nad83   REAL,
#         surface_long_nad83  REAL,
#         land_tenure_area    TEXT,
#         well_classification TEXT,
#         datum               TEXT,
#         datum_elevation     REAL,
#         earliest_spud_date  DATE,
#         latest_release_date DATE
#     );
#     """)

#     # LogData table with one column per curve in the union
#     curve_defs = ", ".join([f'"{c}" REAL' for c in curve_cols])

#     cursor.execute(f"""
#     CREATE TABLE LogData (
#         id       INTEGER PRIMARY KEY AUTOINCREMENT,
#         well_id  INTEGER,
#         depth    REAL,
#         {curve_defs},
#         FOREIGN KEY (well_id) REFERENCES Wells(well_id)
#     );
#     """)

#     conn.commit()
#     conn.close()
#     print("\nDatabase schema created with unified curve columns.\n")


# def ingest_las_file(las_path: Path, curve_cols):
#     """Ingest a single LAS file into Wells + LogData using the unified curve_cols."""
#     print(f"=== Ingesting: {las_path.name} ===")

#     las = lasio.read(las_path)
#     df_raw = las.df()

#     # Move index (depth) into a 'depth' column
#     df = df_raw.reset_index()
#     depth_col_name = df_raw.index.name or "index"
#     df = df.rename(columns={depth_col_name: "depth"})

#     # Convert all non-depth columns to numeric
#     for col in df.columns:
#         if col != "depth":
#             df[col] = pd.to_numeric(df[col], errors="coerce")

#     # Replace NaNs with None
#     df = df.where(pd.notnull(df), None)

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # --- Insert well metadata ---
#     try:
#         well_name = las.well.WELL.value or las_path.stem
#     except Exception:
#         well_name = las_path.stem

#     well_meta = (
#         well_name,          # well_name
#         None,               # operator
#         0,                  # reentry_times
#         None, None,         # lat/long NAD83
#         None,               # land_tenure_area
#         None,               # well_classification
#         None,               # datum
#         None,               # datum_elevation
#         None, None          # earliest_spud_date, latest_release_date
#     )

#     cursor.execute("""
#         INSERT INTO Wells (
#             well_name, operator, reentry_times,
#             surface_lat_nad83, surface_long_nad83,
#             land_tenure_area, well_classification,
#             datum, datum_elevation,
#             earliest_spud_date, latest_release_date
#         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, well_meta)

#     well_id = cursor.lastrowid
#     print(f"Assigned well_id={well_id} to {well_name}")

#     # --- Insert curve data ---
#     col_list = ", ".join([f'"{c}"' for c in curve_cols])
#     placeholders = ", ".join(["?"] * (len(curve_cols) + 2))  # well_id + depth + curves

#     insert_query = f"""
#     INSERT INTO LogData (well_id, depth, {col_list})
#     VALUES ({placeholders})
#     """

#     rows = []
#     for _, row in df.iterrows():
#         values = [well_id, row["depth"]]
#         # For each curve in the unified list, use the value if present in this file, else None
#         for c in curve_cols:
#             values.append(row.get(c, None))
#         rows.append(values)

#     cursor.executemany(insert_query, rows)
#     conn.commit()
#     conn.close()

#     print(f"Inserted {len(rows)} rows for well: {well_name}\n")


# if __name__ == "__main__":
#     LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")

#     las_files = list(LAS_DIR.glob("*.las")) + list(LAS_DIR.glob("*.csv"))
#     print(f"Found {len(las_files)} LAS files to ingest.\n")

#     if not las_files:
#         raise SystemExit("No LAS files found in LAS directory.")

#     # 1) Build union of curves across all files
#     curve_cols = get_union_of_curves(las_files)

#     # 2) Create DB schema with these curve columns
#     setup_database(curve_cols)

#     # 3) Ingest each file
#     for file in las_files:
#         ingest_las_file(file, curve_cols)

#     print("=== Ingestion completed for all files ===")


# import lasio
# import sqlite3
# import pandas as pd
# from pathlib import Path

# DB_PATH = "toy_las_system.db"
# LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")


# def get_union_of_curves(las_files):
#     """Scan all LAS files and return the union of all curve names."""
#     all_curves = set()

#     for f in las_files:
#         print(f"Scanning curves in: {f.name}")
#         try:
#             # 🔑 Force engine="normal" for wrapped files
#             las = lasio.read(f, engine="normal")
#             df_curves = las.df()
#             all_curves.update(df_curves.columns.tolist())
#         except Exception as e:
#             print(f"  !! Skipping {f.name} due to read error: {e}")

#     curve_list = sorted(all_curves)
#     print("\nUnified curve list across all files:")
#     print(curve_list)
#     return curve_list


# def setup_database(curve_cols):
#     """Create (or recreate) Wells and LogData tables based on union of curve columns."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # Drop existing tables so schema always matches our union
#     cursor.execute("DROP TABLE IF EXISTS LogData")
#     cursor.execute("DROP TABLE IF EXISTS Wells")

#     # Wells table with rich metadata
#     cursor.execute("""
#     CREATE TABLE Wells (
#         well_id             INTEGER PRIMARY KEY AUTOINCREMENT,
#         well_name           TEXT NOT NULL,
#         operator            TEXT,
#         reentry_times       INTEGER,
#         surface_lat_nad83   REAL,
#         surface_long_nad83  REAL,
#         land_tenure_area    TEXT,
#         well_classification TEXT,
#         datum               TEXT,
#         datum_elevation     REAL,
#         earliest_spud_date  DATE,
#         latest_release_date DATE
#     );
#     """)

#     # LogData table with one column per curve in the union
#     curve_defs = ", ".join([f'"{c}" REAL' for c in curve_cols])

#     cursor.execute(f"""
#     CREATE TABLE LogData (
#         id       INTEGER PRIMARY KEY AUTOINCREMENT,
#         well_id  INTEGER,
#         depth    REAL,
#         {curve_defs},
#         FOREIGN KEY (well_id) REFERENCES Wells(well_id)
#     );
#     """)

#     conn.commit()
#     conn.close()
#     print("\nDatabase schema created with unified curve columns.\n")


# def ingest_las_file(las_path: Path, curve_cols):
#     """Ingest a single LAS file into Wells + LogData using the unified curve_cols."""
#     print(f"=== Ingesting: {las_path.name} ===")

#     try:
#         # 🔑 Force engine="normal" for wrapped LAS
#         las = lasio.read(las_path, engine="normal")
#     except Exception as e:
#         print(f"  !! Failed to read {las_path.name}: {e}")
#         return

#     df_raw = las.df()

#     # Move index (depth) into a 'depth' column
#     df = df_raw.reset_index()
#     depth_col_name = df_raw.index.name or "index"
#     df = df.rename(columns={depth_col_name: "depth"})

#     # Convert all non-depth columns to numeric
#     for col in df.columns:
#         if col != "depth":
#             df[col] = pd.to_numeric(df[col], errors="coerce")

#     # Replace NaNs with None
#     df = df.where(pd.notnull(df), None)

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # --- Insert well metadata ---
#     try:
#         well_name = las.well.WELL.value or las_path.stem
#     except Exception:
#         well_name = las_path.stem

#     well_meta = (
#         well_name,          # well_name
#         None,               # operator
#         0,                  # reentry_times
#         None, None,         # lat/long NAD83
#         None,               # land_tenure_area
#         None,               # well_classification
#         None,               # datum
#         None,               # datum_elevation
#         None, None          # earliest_spud_date, latest_release_date
#     )

#     cursor.execute("""
#         INSERT INTO Wells (
#             well_name, operator, reentry_times,
#             surface_lat_nad83, surface_long_nad83,
#             land_tenure_area, well_classification,
#             datum, datum_elevation,
#             earliest_spud_date, latest_release_date
#         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, well_meta)

#     well_id = cursor.lastrowid
#     print(f"Assigned well_id={well_id} to {well_name}")

#     # --- Insert curve data ---
#     col_list = ", ".join([f'"{c}"' for c in curve_cols])
#     placeholders = ", ".join(["?"] * (len(curve_cols) + 2))  # well_id + depth + curves

#     insert_query = f"""
#     INSERT INTO LogData (well_id, depth, {col_list})
#     VALUES ({placeholders})
#     """

#     rows = []
#     for _, row in df.iterrows():
#         values = [well_id, row["depth"]]
#         # For each curve in the unified list, use the value if present in this file, else None
#         for c in curve_cols:
#             values.append(row.get(c, None))
#         rows.append(values)

#     cursor.executemany(insert_query, rows)
#     conn.commit()
#     conn.close()

#     print(f"Inserted {len(rows)} rows for well: {well_name}\n")


# if __name__ == "__main__":
#     LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")

#     las_files = list(LAS_DIR.glob("*.las")) + list(LAS_DIR.glob("*.csv"))
#     print(f"Found {len(las_files)} LAS files to ingest.\n")

#     if not las_files:
#         raise SystemExit("No LAS files found in LAS directory.")

#     # 1) Build union of curves across all files
#     curve_cols = get_union_of_curves(las_files)

#     if not curve_cols:
#         raise SystemExit("No curves found in any LAS file – check files or read errors above.")

#     # 2) Create DB schema with these curve columns
#     setup_database(curve_cols)

#     # 3) Ingest each file
#     for file in las_files:
#         ingest_las_file(file, curve_cols)

#     print("=== Ingestion completed for all files (where readable) ===")


# import lasio
# import sqlite3
# import pandas as pd
# from pathlib import Path

# DB_PATH = "toy_las_system.db"
# LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")


# def get_union_of_curves(las_files):
#     """Scan all LAS files and return the union of all curve names."""
#     all_curves = set()

#     for f in las_files:
#         print(f"Scanning curves in: {f.name}")
#         try:
#             # Force engine="normal" for wrapped LAS
#             las = lasio.read(f, engine="normal")
#             df_curves = las.df()
#             all_curves.update(df_curves.columns.tolist())
#         except Exception as e:
#             print(f"  !! Skipping {f.name} due to read error: {e}")

#     # Remove any curve that is actually the depth column
#     curve_list = sorted(c for c in all_curves if c.lower() != "depth")

#     print("\nUnified curve list across all files (excluding DEPTH as a curve):")
#     print(curve_list)
#     return curve_list


# def setup_database(curve_cols):
#     """Create (or recreate) Wells and LogData tables based on union of curve columns."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # Drop existing tables so schema always matches our union
#     cursor.execute("DROP TABLE IF EXISTS LogData")
#     cursor.execute("DROP TABLE IF EXISTS Wells")

#     # Wells table with rich metadata
#     cursor.execute("""
#     CREATE TABLE Wells (
#         well_id             INTEGER PRIMARY KEY AUTOINCREMENT,
#         well_name           TEXT NOT NULL,
#         operator            TEXT,
#         reentry_times       INTEGER,
#         surface_lat_nad83   REAL,
#         surface_long_nad83  REAL,
#         land_tenure_area    TEXT,
#         well_classification TEXT,
#         datum               TEXT,
#         datum_elevation     REAL,
#         earliest_spud_date  DATE,
#         latest_release_date DATE
#     );
#     """)

#     # LogData table with one column per curve in the union
#     curve_defs = ", ".join([f'"{c}" REAL' for c in curve_cols])

#     cursor.execute(f"""
#     CREATE TABLE LogData (
#         id       INTEGER PRIMARY KEY AUTOINCREMENT,
#         well_id  INTEGER,
#         depth    REAL,
#         {curve_defs},
#         FOREIGN KEY (well_id) REFERENCES Wells(well_id)
#     );
#     """)

#     conn.commit()
#     conn.close()
#     print("\nDatabase schema created with unified curve columns.\n")


# def ingest_las_file(las_path: Path, curve_cols):
#     """Ingest a single LAS file into Wells + LogData using the unified curve_cols."""
#     print(f"=== Ingesting: {las_path.name} ===")

#     try:
#         # Force engine="normal" for wrapped LAS
#         las = lasio.read(las_path, engine="normal")
#     except Exception as e:
#         print(f"  !! Failed to read {las_path.name}: {e}")
#         return

#     df_raw = las.df()

#     # Move index (depth) into a 'depth' column
#     df = df_raw.reset_index()
#     depth_col_name = df_raw.index.name or "index"
#     df = df.rename(columns={depth_col_name: "depth"})

#     # Convert all non-depth columns to numeric
#     for col in df.columns:
#         if col != "depth":
#             df[col] = pd.to_numeric(df[col], errors="coerce")

#     # Replace NaNs with None
#     df = df.where(pd.notnull(df), None)

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # --- Insert well metadata ---
#     try:
#         well_name = las.well.WELL.value or las_path.stem
#     except Exception:
#         well_name = las_path.stem

#     well_meta = (
#         well_name,          # well_name
#         None,               # operator
#         0,                  # reentry_times
#         None, None,         # lat/long NAD83
#         None,               # land_tenure_area
#         None,               # well_classification
#         None,               # datum
#         None,               # datum_elevation
#         None, None          # earliest_spud_date, latest_release_date
#     )

#     cursor.execute("""
#         INSERT INTO Wells (
#             well_name, operator, reentry_times,
#             surface_lat_nad83, surface_long_nad83,
#             land_tenure_area, well_classification,
#             datum, datum_elevation,
#             earliest_spud_date, latest_release_date
#         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, well_meta)

#     well_id = cursor.lastrowid
#     print(f"Assigned well_id={well_id} to {well_name}")

#     # --- Insert curve data ---
#     col_list = ", ".join([f'"{c}"' for c in curve_cols])
#     placeholders = ", ".join(["?"] * (len(curve_cols) + 2))  # well_id + depth + curves

#     insert_query = f"""
#     INSERT INTO LogData (well_id, depth, {col_list})
#     VALUES ({placeholders})
#     """

#     rows = []
#     for _, row in df.iterrows():
#         values = [well_id, row["depth"]]
#         # For each curve in the unified list, use the value if present in this file, else None
#         for c in curve_cols:
#             values.append(row.get(c, None))
#         rows.append(values)

#     cursor.executemany(insert_query, rows)
#     conn.commit()
#     conn.close()

#     print(f"Inserted {len(rows)} rows for well: {well_name}\n")


# if __name__ == "__main__":
#     LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")

#     las_files = list(LAS_DIR.glob("*.las")) + list(LAS_DIR.glob("*.csv"))
#     print(f"Found {len(las_files)} LAS files to ingest.\n")

#     if not las_files:
#         raise SystemExit("No LAS files found in LAS directory.")

#     # 1) Build union of curves across all files
#     curve_cols = get_union_of_curves(las_files)

#     if not curve_cols:
#         raise SystemExit("No curves found in any LAS file – check files or read errors above.")

#     # 2) Create DB schema with these curve columns
#     setup_database(curve_cols)

#     # 3) Ingest each file
#     for file in las_files:
#         ingest_las_file(file, curve_cols)

#     print("=== Ingestion completed for all files (where readable) ===")

# this 

# import lasio
# import sqlite3
# import pandas as pd
# from pathlib import Path

# DB_PATH = "toy_las_system.db"
# LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")


# def normalize_well_name(name: str) -> str:
#     """
#     Normalize well names so that the same physical well
#     doesn't appear multiple times with tiny text differences.
#     """
#     if not name:
#         return "UNKNOWN_WELL"

#     # Make sure it is string
#     name = str(name)

#     # Strip whitespace
#     name = name.strip()

#     # Replace underscores with hyphens (B-16_10 -> B-16-10)
#     name = name.replace("_", "-")

#     # Collapse multiple spaces
#     name = " ".join(name.split())

#     # All uppercase for consistency
#     name = name.upper()

#     return name


# def get_union_of_curves(las_files):
#     """Scan all LAS files and return the union of all curve names."""
#     all_curves = set()

#     for f in las_files:
#         print(f"Scanning curves in: {f.name}")
#         try:
#             # Force engine="normal" for wrapped LAS
#             las = lasio.read(f, engine="normal")
#             df_curves = las.df()
#             all_curves.update(df_curves.columns.tolist())
#         except Exception as e:
#             print(f"  !! Skipping {f.name} due to read error: {e}")

#     # Remove any curve that is actually the depth column
#     curve_list = sorted(c for c in all_curves if c.lower() != "depth")

#     print("\nUnified curve list across all files (excluding DEPTH as a curve):")
#     print(curve_list)
#     return curve_list


# def setup_database(curve_cols):
#     """Create (or recreate) Wells and LogData tables based on union of curve columns."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # Drop existing tables so schema always matches our union
#     cursor.execute("DROP TABLE IF EXISTS LogData")
#     cursor.execute("DROP TABLE IF EXISTS Wells")

#     # Wells table with rich metadata
#     cursor.execute("""
#     CREATE TABLE Wells (
#         well_id             INTEGER PRIMARY KEY AUTOINCREMENT,
#         well_name           TEXT NOT NULL UNIQUE,
#         operator            TEXT,
#         reentry_times       INTEGER,
#         surface_lat_nad83   REAL,
#         surface_long_nad83  REAL,
#         land_tenure_area    TEXT,
#         well_classification TEXT,
#         datum               TEXT,
#         datum_elevation     REAL,
#         earliest_spud_date  DATE,
#         latest_release_date DATE
#     );
#     """)

#     # LogData table with one column per curve in the union
#     curve_defs = ", ".join([f'"{c}" REAL' for c in curve_cols])

#     cursor.execute(f"""
#     CREATE TABLE LogData (
#         id       INTEGER PRIMARY KEY AUTOINCREMENT,
#         well_id  INTEGER,
#         depth    REAL,
#         {curve_defs},
#         FOREIGN KEY (well_id) REFERENCES Wells(well_id)
#     );
#     """)

#     conn.commit()
#     conn.close()
#     print("\nDatabase schema created with unified curve columns.\n")


# def ingest_las_file(las_path: Path, curve_cols):
#     """Ingest a single LAS file into Wells + LogData using the unified curve_cols."""
#     print(f"=== Ingesting: {las_path.name} ===")

#     try:
#         # Force engine="normal" for wrapped LAS
#         las = lasio.read(las_path, engine="normal")
#     except Exception as e:
#         print(f"  !! Failed to read {las_path.name}: {e}")
#         return

#     df_raw = las.df()

#     # Move index (depth) into a 'depth' column
#     df = df_raw.reset_index()
#     depth_col_name = df_raw.index.name or "index"
#     df = df.rename(columns={depth_col_name: "depth"})

#     # Convert all non-depth columns to numeric
#     for col in df.columns:
#         if col != "depth":
#             df[col] = pd.to_numeric(df[col], errors="coerce")

#     # Replace NaNs with None
#     df = df.where(pd.notnull(df), None)

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # --- Determine and normalize well name ---
#     try:
#         raw_name = las.well.WELL.value
#     except Exception:
#         raw_name = las_path.stem  # fallback to filename

#     norm_name = normalize_well_name(raw_name)
#     print(f"Raw WELL name: {raw_name!r}  ->  Normalized: {norm_name!r}")

#     # --- Ensure we do NOT create duplicate Wells rows for same well ---
#     cursor.execute("SELECT well_id FROM Wells WHERE well_name = ?", (norm_name,))
#     row = cursor.fetchone()

#     if row:
#         well_id = row[0]
#         print(f"Well already exists with well_id={well_id}, reusing it.")
#     else:
#         well_meta = (
#             norm_name,        # well_name (normalized, unique)
#             None,             # operator
#             0,                # reentry_times
#             None, None,       # lat/long NAD83
#             None,             # land_tenure_area
#             None,             # well_classification
#             None,             # datum
#             None,             # datum_elevation
#             None, None        # earliest_spud_date, latest_release_date
#         )

#         cursor.execute("""
#             INSERT INTO Wells (
#                 well_name, operator, reentry_times,
#                 surface_lat_nad83, surface_long_nad83,
#                 land_tenure_area, well_classification,
#                 datum, datum_elevation,
#                 earliest_spud_date, latest_release_date
#             ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, well_meta)

#         well_id = cursor.lastrowid
#         print(f"Inserted new well with well_id={well_id}")

#     # --- Insert curve data for this file ---
#     col_list = ", ".join([f'"{c}"' for c in curve_cols])
#     placeholders = ", ".join(["?"] * (len(curve_cols) + 2))  # well_id + depth + curves

#     insert_query = f"""
#     INSERT INTO LogData (well_id, depth, {col_list})
#     VALUES ({placeholders})
#     """

#     rows = []
#     for _, row in df.iterrows():
#         values = [well_id, row["depth"]]
#         # For each curve in the unified list, use the value if present in this file, else None
#         for c in curve_cols:
#             values.append(row.get(c, None))
#         rows.append(values)

#     cursor.executemany(insert_query, rows)
#     conn.commit()
#     conn.close()

#     print(f"Inserted {len(rows)} rows for well_id={well_id} ({norm_name}).\n")


# if __name__ == "__main__":
#     LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")

#     las_files = list(LAS_DIR.glob("*.las")) + list(LAS_DIR.glob("*.csv"))
#     print(f"Found {len(las_files)} LAS files to ingest.\n")

#     if not las_files:
#         raise SystemExit("No LAS files found in LAS directory.")

#     # 1) Build union of curves across all files
#     curve_cols = get_union_of_curves(las_files)

#     if not curve_cols:
#         raise SystemExit("No curves found in any LAS file – check files or read errors above.")

#     # 2) Create DB schema with these curve columns
#     setup_database(curve_cols)

#     # 3) Ingest each file (each well only gets ONE row in Wells)
#     for file in las_files:
#         ingest_las_file(file, curve_cols)

#     print("=== Ingestion completed for all files (where readable) ===")





# import lasio
# import sqlite3
# import pandas as pd
# from pathlib import Path

# DB_PATH = "toy_las_system.db"
# LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")


# def normalize_well_name(name: str) -> str:
#     """
#     Normalize well names for readability/consistency.
#     We DO NOT use this to detect duplicates anymore (we use file_name for that).
#     """
#     if not name:
#         return "UNKNOWN_WELL"

#     name = str(name).strip()
#     name = name.replace("_", "-")        # B-16_10 -> B-16-10
#     name = " ".join(name.split())        # collapse multiple spaces
#     name = name.upper()                  # BAY DE VERDE F-67
#     return name


# def get_union_of_curves(las_files):
#     """Scan all LAS files and return the union of all curve names."""
#     all_curves = set()

#     for f in las_files:
#         print(f"Scanning curves in: {f.name}")
#         try:
#             # Force engine="normal" for wrapped LAS
#             las = lasio.read(f, engine="normal")
#             df_curves = las.df()
#             all_curves.update(df_curves.columns.tolist())
#         except Exception as e:
#             print(f"  !! Skipping {f.name} due to read error: {e}")

#     # Remove any curve that is actually the depth column
#     curve_list = sorted(c for c in all_curves if c.lower() != "depth")

#     print("\nUnified curve list across all files (excluding DEPTH as a curve):")
#     print(curve_list)
#     return curve_list


# def setup_database(curve_cols):
#     """
#     Create (or recreate) Wells and LogData tables based on union of curve columns.

#     NOTE: This drops existing Wells/LogData, so each run starts from a clean slate.
#     """
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # Drop existing tables so schema always matches our union
#     cursor.execute("DROP TABLE IF EXISTS LogData")
#     cursor.execute("DROP TABLE IF EXISTS Wells")

#     # Wells table with file_name-based uniqueness
#     cursor.execute("""
#     CREATE TABLE Wells (
#         well_id             INTEGER PRIMARY KEY AUTOINCREMENT,
#         file_name           TEXT NOT NULL UNIQUE,
#         well_name           TEXT NOT NULL,
#         operator            TEXT,
#         reentry_times       INTEGER,
#         surface_lat_nad83   REAL,
#         surface_long_nad83  REAL,
#         land_tenure_area    TEXT,
#         well_classification TEXT,
#         datum               TEXT,
#         datum_elevation     REAL,
#         earliest_spud_date  DATE,
#         latest_release_date DATE
#     );
#     """)

#     # LogData table with one column per curve in the union
#     curve_defs = ", ".join([f'"{c}" REAL' for c in curve_cols])

#     cursor.execute(f"""
#     CREATE TABLE LogData (
#         id       INTEGER PRIMARY KEY AUTOINCREMENT,
#         well_id  INTEGER,
#         depth    REAL,
#         {curve_defs},
#         FOREIGN KEY (well_id) REFERENCES Wells(well_id)
#     );
#     """)

#     conn.commit()
#     conn.close()
#     print("\nDatabase schema created with unified curve columns.\n")


# def ingest_las_file(las_path: Path, curve_cols):
#     """
#     Ingest a single LAS file into Wells + LogData using the unified curve_cols.

#     Deduplication is by file_name: if this file_name is already in Wells,
#     we skip inserting a new well and we also skip log data for this file.
#     """
#     print(f"=== Ingesting: {las_path.name} ===")

#     try:
#         # Force engine="normal" for wrapped LAS
#         las = lasio.read(las_path, engine="normal")
#     except Exception as e:
#         print(f"  !! Failed to read {las_path.name}: {e}")
#         return

#     df_raw = las.df()

#     # Move index (depth) into a 'depth' column
#     df = df_raw.reset_index()
#     depth_col_name = df_raw.index.name or "index"
#     df = df.rename(columns={depth_col_name: "depth"})

#     # Convert all non-depth columns to numeric
#     for col in df.columns:
#         if col != "depth":
#             df[col] = pd.to_numeric(df[col], errors="coerce")

#     # Replace NaNs with None for SQLite
#     df = df.where(pd.notnull(df), None)

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # --- Determine normalized well name (for readability only) ---
#     try:
#         raw_name = las.well.WELL.value
#     except Exception:
#         raw_name = las_path.stem  # fallback to filename if WELL header missing

#     norm_name = normalize_well_name(raw_name)
#     file_name = las_path.name  # used for dedupe

#     print(f"File: {file_name!r}  |  Raw WELL: {raw_name!r}  ->  Norm WELL: {norm_name!r}")

#     # --- CHECK: Has this file already been ingested? ---
#     cursor.execute("SELECT well_id FROM Wells WHERE file_name = ?", (file_name,))
#     row = cursor.fetchone()

#     if row:
#         well_id = row[0]
#         print(f"  -> File {file_name} already ingested as well_id={well_id}. Skipping this file.\n")
#         conn.close()
#         return

#     # --- Insert new well row based on this file ---
#     well_meta = (
#         file_name,          # file_name (unique)
#         norm_name,          # well_name (normalized label)
#         None,               # operator
#         0,                  # reentry_times
#         None, None,         # surface_lat_nad83, surface_long_nad83
#         None,               # land_tenure_area
#         None,               # well_classification
#         None,               # datum
#         None,               # datum_elevation
#         None, None          # earliest_spud_date, latest_release_date
#     )

#     cursor.execute("""
#         INSERT INTO Wells (
#             file_name, well_name, operator, reentry_times,
#             surface_lat_nad83, surface_long_nad83,
#             land_tenure_area, well_classification,
#             datum, datum_elevation,
#             earliest_spud_date, latest_release_date
#         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, well_meta)

#     well_id = cursor.lastrowid
#     print(f"  -> Inserted new well row: well_id={well_id}, well_name={norm_name}")

#     # --- Insert curve data for this file ---
#     col_list = ", ".join([f'"{c}"' for c in curve_cols])
#     placeholders = ", ".join(["?"] * (len(curve_cols) + 2))  # well_id + depth + curves

#     insert_query = f"""
#     INSERT INTO LogData (well_id, depth, {col_list})
#     VALUES ({placeholders})
#     """

#     rows = []
#     for _, row in df.iterrows():
#         values = [well_id, row["depth"]]
#         # For each curve in the unified list, use the value if present in this file, else None
#         for c in curve_cols:
#             values.append(row.get(c, None))
#         rows.append(values)

#     cursor.executemany(insert_query, rows)
#     conn.commit()
#     conn.close()

#     print(f"  -> Inserted {len(rows)} rows for well_id={well_id} ({norm_name}).\n")


# if __name__ == "__main__":
#     LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")

#     las_files = list(LAS_DIR.glob("*.las")) + list(LAS_DIR.glob("*.csv"))
#     print(f"Found {len(las_files)} LAS files to ingest.\n")

#     if not las_files:
#         raise SystemExit("No LAS files found in LAS directory.")

#     # 1) Build union of curves across all files
#     curve_cols = get_union_of_curves(las_files)

#     if not curve_cols:
#         raise SystemExit("No curves found in any LAS file – check files or read errors above.")

#     # 2) Create DB schema with these curve columns (fresh DB each run)
#     setup_database(curve_cols)

#     # 3) Ingest each file (file_name-based dedupe inside a run)
#     for file in las_files:
#         ingest_las_file(file, curve_cols)

#     print("=== Ingestion completed for all files (where readable and not duplicate by file_name) ===")



# import lasio
# import sqlite3
# import pandas as pd
# from pathlib import Path
# import re

# DB_PATH = "toy_las_system.db"
# LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")


# def normalize_well_name(name: str) -> str:
#     """
#     Normalize well names for readability/consistency.
#     We DO NOT use this to detect duplicates anymore (we use file_key for that).
#     """
#     if not name:
#         return "UNKNOWN_WELL"

#     name = str(name).strip()
#     name = name.replace("_", "-")        # B-16_10 -> B-16-10
#     name = " ".join(name.split())        # collapse multiple spaces
#     name = name.upper()                  # BAY DE VERDE F-67
#     return name


# def normalize_file_key(file_name: str) -> str:
#     """
#     Normalize a file name to a logical 'file key' used for deduplicating files.
#     Examples:
#         'LAS-002939.csv'       -> 'las-002939.csv'
#         'LAS-002939 (1).csv'   -> 'las-002939.csv'
#         'Las-002939 (2).LAS'   -> 'las-002939.las'
#     """
#     p = Path(file_name)
#     stem = p.stem        # e.g. 'LAS-002939 (1)'
#     suffix = p.suffix.lower()  # e.g. '.csv' or '.las'

#     # Remove copy suffix like ' (1)', ' (2)' at the end of the stem
#     stem = re.sub(r" \(\d+\)$", "", stem)

#     # Lowercase the whole key for consistency
#     key = f"{stem.lower()}{suffix}"
#     return key


# def get_union_of_curves(las_files):
#     """Scan all LAS files and return the union of all curve names."""
#     all_curves = set()

#     for f in las_files:
#         print(f"Scanning curves in: {f.name}")
#         try:
#             # Force engine="normal" for wrapped LAS
#             las = lasio.read(f, engine="normal")
#             df_curves = las.df()
#             all_curves.update(df_curves.columns.tolist())
#         except Exception as e:
#             print(f"  !! Skipping {f.name} due to read error: {e}")

#     # Remove any curve that is actually the depth column
#     curve_list = sorted(c for c in all_curves if c.lower() != "depth")

#     print("\nUnified curve list across all files (excluding DEPTH as a curve):")
#     print(curve_list)
#     return curve_list


# def setup_database(curve_cols):
#     """
#     Create (or recreate) Wells and LogData tables based on union of curve columns.

#     NOTE: This drops existing Wells/LogData, so each run starts from a clean slate.
#     """
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # Drop existing tables so schema always matches our union
#     cursor.execute("DROP TABLE IF EXISTS LogData")
#     cursor.execute("DROP TABLE IF EXISTS Wells")

#     # Wells table with file_key-based uniqueness
#     cursor.execute("""
#     CREATE TABLE Wells (
#         well_id             INTEGER PRIMARY KEY AUTOINCREMENT,
#         file_name           TEXT NOT NULL,
#         file_key            TEXT NOT NULL UNIQUE,
#         well_name           TEXT NOT NULL,
#         operator            TEXT,
#         reentry_times       INTEGER,
#         surface_lat_nad83   REAL,
#         surface_long_nad83  REAL,
#         land_tenure_area    TEXT,
#         well_classification TEXT,
#         datum               TEXT,
#         datum_elevation     REAL,
#         earliest_spud_date  DATE,
#         latest_release_date DATE
#     );
#     """)

#     # LogData table with one column per curve in the union
#     curve_defs = ", ".join([f'"{c}" REAL' for c in curve_cols])

#     cursor.execute(f"""
#     CREATE TABLE LogData (
#         id       INTEGER PRIMARY KEY AUTOINCREMENT,
#         well_id  INTEGER,
#         depth    REAL,
#         {curve_defs},
#         FOREIGN KEY (well_id) REFERENCES Wells(well_id)
#     );
#     """)

#     conn.commit()
#     conn.close()
#     print("\nDatabase schema created with unified curve columns.\n")


# def ingest_las_file(las_path: Path, curve_cols):
#     """
#     Ingest a single LAS file into Wells + LogData using the unified curve_cols.

#     Deduplication is by file_key: e.g.
#         'LAS-002939.csv' and 'LAS-002939 (1).csv'
#     will share the same file_key 'las-002939.csv', so only the first is ingested.
#     """
#     print(f"=== Ingesting: {las_path.name} ===")

#     try:
#         # Force engine="normal" for wrapped LAS
#         las = lasio.read(las_path, engine="normal")
#     except Exception as e:
#         print(f"  !! Failed to read {las_path.name}: {e}")
#         return

#     df_raw = las.df()

#     # Move index (depth) into a 'depth' column
#     df = df_raw.reset_index()
#     depth_col_name = df_raw.index.name or "index"
#     df = df.rename(columns={depth_col_name: "depth"})

#     # Convert all non-depth columns to numeric
#     for col in df.columns:
#         if col != "depth":
#             df[col] = pd.to_numeric(df[col], errors="coerce")

#     # Replace NaNs with None for SQLite
#     df = df.where(pd.notnull(df), None)

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # --- Determine normalized well name (for readability only) ---
#     try:
#         raw_name = las.well.WELL.value
#     except Exception:
#         raw_name = las_path.stem  # fallback to filename if WELL header missing

#     norm_name = normalize_well_name(raw_name)

#     # --- Compute file_name and file_key for dedupe ---
#     file_name = las_path.name            # e.g. 'LAS-002939 (1).csv'
#     file_key = normalize_file_key(file_name)  # e.g. 'las-002939.csv'

#     print(f"File: {file_name!r}  |  File key: {file_key!r}  |  Raw WELL: {raw_name!r}  ->  Norm WELL: {norm_name!r}")

#     # --- CHECK: Has a file with this logical file_key already been ingested? ---
#     cursor.execute("SELECT well_id FROM Wells WHERE file_key = ?", (file_key,))
#     row = cursor.fetchone()

#     if row:
#         well_id = row[0]
#         print(f"  -> A file with key {file_key!r} already ingested as well_id={well_id}. Skipping this file.\n")
#         conn.close()
#         return

#     # --- Insert new well row based on this file ---
#     well_meta = (
#         file_name,          # original file_name
#         file_key,           # normalized file_key (unique)
#         norm_name,          # human-readable well_name
#         None,               # operator
#         0,                  # reentry_times
#         None, None,         # surface_lat_nad83, surface_long_nad83
#         None,               # land_tenure_area
#         None,               # well_classification
#         None,               # datum
#         None,               # datum_elevation
#         None, None          # earliest_spud_date, latest_release_date
#     )

#     cursor.execute("""
#         INSERT INTO Wells (
#             file_name, file_key, well_name, operator, reentry_times,
#             surface_lat_nad83, surface_long_nad83,
#             land_tenure_area, well_classification,
#             datum, datum_elevation,
#             earliest_spud_date, latest_release_date
#         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, well_meta)

#     well_id = cursor.lastrowid
#     print(f"  -> Inserted new well row: well_id={well_id}, well_name={norm_name}, file_key={file_key}")

#     # --- Insert curve data for this file ---
#     col_list = ", ".join([f'"{c}"' for c in curve_cols])
#     placeholders = ", ".join(["?"] * (len(curve_cols) + 2))  # well_id + depth + curves

#     insert_query = f"""
#     INSERT INTO LogData (well_id, depth, {col_list})
#     VALUES ({placeholders})
#     """

#     rows = []
#     for _, row in df.iterrows():
#         values = [well_id, row["depth"]]
#         # For each curve in the unified list, use the value if present in this file, else None
#         for c in curve_cols:
#             values.append(row.get(c, None))
#         rows.append(values)

#     cursor.executemany(insert_query, rows)
#     conn.commit()
#     conn.close()

#     print(f"  -> Inserted {len(rows)} rows for well_id={well_id} ({norm_name}).\n")


# if __name__ == "__main__":
#     LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")

#     las_files = list(LAS_DIR.glob("*.las")) + list(LAS_DIR.glob("*.csv"))
#     print(f"Found {len(las_files)} LAS files to ingest.\n")

#     if not las_files:
#         raise SystemExit("No LAS files found in LAS directory.")

#     # 1) Build union of curves across all files
#     curve_cols = get_union_of_curves(las_files)

#     if not curve_cols:
#         raise SystemExit("No curves found in any LAS file – check files or read errors above.")

#     # 2) Create DB schema with these curve columns (fresh DB each run)
#     setup_database(curve_cols)

#     # 3) Ingest each file (dedupe by file_key, so 'xxx.csv' and 'xxx (1).csv' count as same)
#     for file in las_files:
#         ingest_las_file(file, curve_cols)

#     print("=== Ingestion completed for all files (where readable and not duplicate by file_key) ===")





# import lasio
# import sqlite3
# import pandas as pd
# from pathlib import Path
# import re

# DB_PATH = "toy_las_system.db"
# LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")


# def normalize_well_name(name: str) -> str:
#     """
#     Normalize well names for readability/consistency.
#     We DO NOT use this to detect duplicates anymore (we use file_key for that).
#     """
#     if not name:
#         return "UNKNOWN_WELL"

#     name = str(name).strip()
#     name = name.replace("_", "-")        # B-16_10 -> B-16-10
#     name = " ".join(name.split())        # collapse multiple spaces
#     name = name.upper()                  # BAY DE VERDE F-67
#     return name


# def normalize_file_key(file_name: str) -> str:
#     """
#     Normalize a file name to a logical 'file key' used for deduplicating files.

#     Examples:
#         'LAS-002939.csv'       -> 'las-002939.csv'
#         'LAS-002939 (1).csv'   -> 'las-002939.csv'
#         'Las-002939 (2).LAS'   -> 'las-002939.las'
#     """
#     p = Path(file_name)
#     stem = p.stem              # e.g. 'LAS-002939 (1)'
#     suffix = p.suffix.lower()  # e.g. '.csv' or '.las'

#     # Remove copy suffix like ' (1)', ' (2)' at the end of the stem
#     stem = re.sub(r" \(\d+\)$", "", stem)

#     # Lowercase the whole key for consistency
#     key = f"{stem.lower()}{suffix}"
#     return key


# def get_union_of_curves(las_files):
#     """Scan all LAS files and return the union of all curve names."""
#     all_curves = set()

#     for f in las_files:
#         print(f"Scanning curves in: {f.name}")
#         try:
#             # Force engine="normal" for wrapped LAS
#             las = lasio.read(f, engine="normal")
#             df_curves = las.df()
#             all_curves.update(df_curves.columns.tolist())
#         except Exception as e:
#             print(f"  !! Skipping {f.name} due to read error: {e}")

#     # Remove any curve that is actually the depth column
#     curve_list = sorted(c for c in all_curves if c.lower() != "depth")

#     print("\nUnified curve list across all files (excluding DEPTH as a curve):")
#     print(curve_list)
#     return curve_list


# def setup_database(curve_cols):
#     """
#     Create (or recreate) Wells and LogData tables based on union of curve columns.

#     NOTE: This drops existing Wells/LogData, so each run starts from a clean slate.
#     """
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # Drop existing tables so schema always matches our union
#     cursor.execute("DROP TABLE IF EXISTS LogData")
#     cursor.execute("DROP TABLE IF EXISTS Wells")

#     # Wells table with file_key-based uniqueness
#     cursor.execute("""
#     CREATE TABLE Wells (
#         well_id             INTEGER PRIMARY KEY AUTOINCREMENT,
#         file_name           TEXT NOT NULL,
#         file_key            TEXT NOT NULL UNIQUE,
#         well_name           TEXT NOT NULL,
#         operator            TEXT,
#         reentry_times       INTEGER,
#         surface_lat_nad83   REAL,
#         surface_long_nad83  REAL,
#         land_tenure_area    TEXT,
#         well_classification TEXT,
#         datum               TEXT,
#         datum_elevation     REAL,
#         earliest_spud_date  DATE,
#         latest_release_date DATE
#     );
#     """)

#     # LogData table with one column per curve in the union
#     curve_defs = ", ".join([f'"{c}" REAL' for c in curve_cols])

#     cursor.execute(f"""
#     CREATE TABLE LogData (
#         id       INTEGER PRIMARY KEY AUTOINCREMENT,
#         well_id  INTEGER,
#         depth    REAL,
#         {curve_defs},
#         FOREIGN KEY (well_id) REFERENCES Wells(well_id)
#     );
#     """)

#     conn.commit()
#     conn.close()
#     print("\nDatabase schema created with unified curve columns.\n")


# def ingest_las_file(las_path: Path, curve_cols):
#     """
#     Ingest a single LAS file into Wells + LogData using the unified curve_cols.

#     Deduplication is by file_key: e.g.
#         'LAS-002939.csv' and 'LAS-002939 (1).csv'
#     will share the same file_key 'las-002939.csv', so only the first is ingested.
#     """
#     print(f"=== Ingesting: {las_path.name} ===")

#     try:
#         # Force engine="normal" for wrapped LAS
#         las = lasio.read(las_path, engine="normal")
#     except Exception as e:
#         print(f"  !! Failed to read {las_path.name}: {e}")
#         return

#     df_raw = las.df()

#     # Move index (depth) into a 'depth' column
#     df = df_raw.reset_index()
#     depth_col_name = df_raw.index.name or "index"
#     df = df.rename(columns={depth_col_name: "depth"})

#     # Convert all non-depth columns to numeric
#     for col in df.columns:
#         if col != "depth":
#             df[col] = pd.to_numeric(df[col], errors="coerce")

#     # Replace NaNs with None for SQLite
#     df = df.where(pd.notnull(df), None)

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # --- Determine normalized well name (for readability only) ---
#     try:
#         raw_name = las.well.WELL.value
#     except Exception:
#         raw_name = las_path.stem  # fallback to filename if WELL header missing

#     norm_name = normalize_well_name(raw_name)

#     # --- Compute file_name and file_key for dedupe ---
#     file_name = las_path.name                 # e.g. 'LAS-002939 (1).csv'
#     file_key = normalize_file_key(file_name)  # e.g. 'las-002939.csv'

#     print(
#         f"File: {file_name!r}  |  File key: {file_key!r}  |  "
#         f"Raw WELL: {raw_name!r}  ->  Norm WELL: {norm_name!r}"
#     )

#     # --- CHECK: Has a file with this logical file_key already been ingested? ---
#     cursor.execute("SELECT well_id FROM Wells WHERE file_key = ?", (file_key,))
#     row = cursor.fetchone()

#     if row:
#         well_id = row[0]
#         print(
#             f"  -> A file with key {file_key!r} already ingested as well_id={well_id}. "
#             f"Skipping this file.\n"
#         )
#         conn.close()
#         return

#     # --- Insert new well row based on this file ---
#     well_meta = (
#         file_name,          # original file_name
#         file_key,           # normalized file_key (unique)
#         norm_name,          # human-readable well_name
#         None,               # operator
#         0,                  # reentry_times
#         None, None,         # surface_lat_nad83, surface_long_nad83
#         None,               # land_tenure_area
#         None,               # well_classification
#         None,               # datum
#         None,               # datum_elevation
#         None,               # earliest_spud_date
#         None                # latest_release_date
#     )

#     cursor.execute("""
#         INSERT INTO Wells (
#             file_name,
#             file_key,
#             well_name,
#             operator,
#             reentry_times,
#             surface_lat_nad83,
#             surface_long_nad83,
#             land_tenure_area,
#             well_classification,
#             datum,
#             datum_elevation,
#             earliest_spud_date,
#             latest_release_date
#         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, well_meta)

#     well_id = cursor.lastrowid
#     print(
#         f"  -> Inserted new well row: well_id={well_id}, "
#         f"well_name={norm_name}, file_key={file_key}"
#     )

#     # --- Insert curve data for this file ---
#     col_list = ", ".join([f'"{c}"' for c in curve_cols])
#     placeholders = ", ".join(["?"] * (len(curve_cols) + 2))  # well_id + depth + curves

#     insert_query = f"""
#     INSERT INTO LogData (well_id, depth, {col_list})
#     VALUES ({placeholders})
#     """

#     rows = []
#     for _, row in df.iterrows():
#         values = [well_id, row["depth"]]
#         # For each curve in the unified list, use the value if present in this file, else None
#         for c in curve_cols:
#             values.append(row.get(c, None))
#         rows.append(values)

#     cursor.executemany(insert_query, rows)
#     conn.commit()
#     conn.close()

#     print(f"  -> Inserted {len(rows)} rows for well_id={well_id} ({norm_name}).\n")


# if __name__ == "__main__":
#     LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")

#     las_files = list(LAS_DIR.glob("*.las")) + list(LAS_DIR.glob("*.csv"))
#     print(f"Found {len(las_files)} LAS files to ingest.\n")

#     if not las_files:
#         raise SystemExit("No LAS files found in LAS directory.")

#     # 1) Build union of curves across all files
#     curve_cols = get_union_of_curves(las_files)

#     if not curve_cols:
#         raise SystemExit("No curves found in any LAS file – check files or read errors above.")

#     # 2) Create DB schema with these curve columns (fresh DB each run)
#     setup_database(curve_cols)

#     # 3) Ingest each file (dedupe by file_key, so 'xxx.csv' and 'xxx (1).csv' count as same)
#     for file in las_files:
#         ingest_las_file(file, curve_cols)

#     print("=== Ingestion completed for all files (where readable and not duplicate by file_key) ===")








import lasio
import sqlite3
import pandas as pd
from pathlib import Path
import re

DB_PATH = "toy_las_system.db"
LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")

# ---------------------------------------------------------
# Canonical mapping for mnemonics → logical parameter name
# ---------------------------------------------------------
CANONICAL_MAP = {
    # Gamma ray family
    "GR": "GAMMA_RAY",
    "GR_CDR": "GAMMA_RAY",
    "SGR": "GAMMA_RAY",
    "GR:1": "GAMMA_RAY",
    "GR:2": "GAMMA_RAY",
    "GR:3": "GAMMA_RAY",

    # Density
    "RHOB": "BULK_DENSITY",

    # Neutron porosity
    "TNPH": "NEUTRON_POROSITY",
    "TNPH_UNC": "NEUTRON_POROSITY",

    # Bit resistivity
    "TAB_RES": "BIT_RESISTIVITY",
    "TAB_RES_BIT": "BIT_RESISTIVITY",

    # Drilling dynamics (examples)
    "ROP5": "DRILLING_RATE",
    "ROP5_RM": "DRILLING_RATE",
    "RPM": "ROTARY_SPEED",

    # Vibration
    "VIB_LAT": "VIBRATION",
    "VIB_TOR": "VIBRATION",
    "VIB_X": "VIBRATION",
}


def canonical_to_family(canonical: str | None) -> str | None:
    """Map canonical_name to a human-readable family label."""
    if canonical is None:
        return None
    if canonical.startswith("GAMMA_RAY"):
        return "Gamma ray"
    if canonical == "BULK_DENSITY":
        return "Density"
    if canonical == "NEUTRON_POROSITY":
        return "Porosity"
    if canonical in ("BIT_RESISTIVITY",):
        return "Resistivity"
    if canonical in ("DRILLING_RATE", "ROTARY_SPEED", "VIBRATION"):
        return "Drilling dynamics"
    return None


def normalize_well_name(name: str) -> str:
    """
    Normalize well names for readability/consistency.
    We DO NOT use this to detect duplicates anymore (we use file_key for that).
    """
    if not name:
        return "UNKNOWN_WELL"

    name = str(name).strip()
    name = name.replace("_", "-")        # B-16_10 -> B-16-10
    name = " ".join(name.split())        # collapse multiple spaces
    name = name.upper()                  # BAY DE VERDE F-67
    return name


def normalize_file_key(file_name: str) -> str:
    """
    Normalize a file name to a logical 'file key' used for deduplicating files.

    Examples:
        'LAS-002939.csv'       -> 'las-002939.csv'
        'LAS-002939 (1).csv'   -> 'las-002939.csv'
        'Las-002939 (2).LAS'   -> 'las-002939.las'
    """
    p = Path(file_name)
    stem = p.stem              # e.g. 'LAS-002939 (1)'
    suffix = p.suffix.lower()  # e.g. '.csv' or '.las'

    # Remove copy suffix like ' (1)', ' (2)' at the end of the stem
    stem = re.sub(r" \(\d+\)$", "", stem)

    # Lowercase the whole key for consistency
    key = f"{stem.lower()}{suffix}"
    return key


def get_union_of_curves(las_files):
    """Scan all LAS files and return the union of all curve names."""
    all_curves = set()

    for f in las_files:
        print(f"Scanning curves in: {f.name}")
        try:
            # Force engine="normal" for wrapped LAS
            las = lasio.read(f, engine="normal")
            df_curves = las.df()
            all_curves.update(df_curves.columns.tolist())
        except Exception as e:
            print(f"  !! Skipping {f.name} due to read error: {e}")

    # Remove any curve that is actually the depth column
    curve_list = sorted(c for c in all_curves if c.lower() != "depth")

    print("\nUnified curve list across all files (excluding DEPTH as a curve):")
    print(curve_list)
    return curve_list


def setup_database(curve_cols):
    """
    Create (or recreate) Wells, CurveMnemonics, and LogData tables
    based on union of curve columns.

    NOTE: This drops existing data, so each run starts from a clean slate.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop existing tables so schema always matches our union
    cursor.execute("DROP TABLE IF EXISTS LogData")
    cursor.execute("DROP TABLE IF EXISTS CurveMnemonics")
    cursor.execute("DROP TABLE IF EXISTS Wells")

    # Wells table with file_key-based uniqueness
    cursor.execute("""
    CREATE TABLE Wells (
        well_id             INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name           TEXT NOT NULL,
        file_key            TEXT NOT NULL UNIQUE,
        well_name           TEXT NOT NULL,
        operator            TEXT,
        reentry_times       INTEGER,
        surface_lat_nad83   REAL,
        surface_long_nad83  REAL,
        land_tenure_area    TEXT,
        well_classification TEXT,
        datum               TEXT,
        datum_elevation     REAL,
        earliest_spud_date  DATE,
        latest_release_date DATE
    );
    """)

    # NEW: Curve mnemonics metadata table
    cursor.execute("""
    CREATE TABLE CurveMnemonics (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        well_id         INTEGER,
        file_key        TEXT,
        mnemonic        TEXT,
        unit            TEXT,
        description     TEXT,
        canonical_name  TEXT,
        family          TEXT,
        FOREIGN KEY (well_id) REFERENCES Wells(well_id)
    );
    """)

    # LogData table with one column per curve in the union
    curve_defs = ", ".join([f'"{c}" REAL' for c in curve_cols])

    cursor.execute(f"""
    CREATE TABLE LogData (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        well_id  INTEGER,
        depth    REAL,
        {curve_defs},
        FOREIGN KEY (well_id) REFERENCES Wells(well_id)
    );
    """)

    conn.commit()
    conn.close()
    print("\nDatabase schema created with unified curve columns.\n")


def ingest_las_file(las_path: Path, curve_cols):
    """
    Ingest a single LAS file into Wells + CurveMnemonics + LogData using the unified curve_cols.

    Deduplication is by file_key: e.g.
        'LAS-002939.csv' and 'LAS-002939 (1).csv'
    will share the same file_key 'las-002939.csv', so only the first is ingested.
    """
    print(f"=== Ingesting: {las_path.name} ===")

    try:
        # Force engine="normal" for wrapped LAS
        las = lasio.read(las_path, engine="normal")
    except Exception as e:
        print(f"  !! Failed to read {las_path.name}: {e}")
        return

    df_raw = las.df()

    # Move index (depth) into a 'depth' column
    df = df_raw.reset_index()
    depth_col_name = df_raw.index.name or "index"
    df = df.rename(columns={depth_col_name: "depth"})

    # Convert all non-depth columns to numeric
    for col in df.columns:
        if col != "depth":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Replace NaNs with None for SQLite
    df = df.where(pd.notnull(df), None)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # --- Determine normalized well name (for readability only) ---
    try:
        raw_name = las.well.WELL.value
    except Exception:
        raw_name = las_path.stem  # fallback to filename if WELL header missing

    norm_name = normalize_well_name(raw_name)

    # --- Compute file_name and file_key for dedupe ---
    file_name = las_path.name                 # e.g. 'LAS-002939 (1).csv'
    file_key = normalize_file_key(file_name)  # e.g. 'las-002939.csv'

    print(
        f"File: {file_name!r}  |  File key: {file_key!r}  |  "
        f"Raw WELL: {raw_name!r}  ->  Norm WELL: {norm_name!r}"
    )

    # --- CHECK: Has a file with this logical file_key already been ingested? ---
    cursor.execute("SELECT well_id FROM Wells WHERE file_key = ?", (file_key,))
    row = cursor.fetchone()

    if row:
        well_id = row[0]
        print(
            f"  -> A file with key {file_key!r} already ingested as well_id={well_id}. "
            f"Skipping this file.\n"
        )
        conn.close()
        return

    # --- Insert new well row based on this file ---
    well_meta = (
        file_name,          # original file_name
        file_key,           # normalized file_key (unique)
        norm_name,          # human-readable well_name
        None,               # operator (can be filled from LAS header later)
        0,                  # reentry_times
        None, None,         # surface_lat_nad83, surface_long_nad83
        None,               # land_tenure_area
        None,               # well_classification
        None,               # datum
        None,               # datum_elevation
        None,               # earliest_spud_date
        None                # latest_release_date
    )

    cursor.execute("""
        INSERT INTO Wells (
            file_name,
            file_key,
            well_name,
            operator,
            reentry_times,
            surface_lat_nad83,
            surface_long_nad83,
            land_tenure_area,
            well_classification,
            datum,
            datum_elevation,
            earliest_spud_date,
            latest_release_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, well_meta)

    well_id = cursor.lastrowid
    print(
        f"  -> Inserted new well row: well_id={well_id}, "
        f"well_name={norm_name}, file_key={file_key}"
    )

    # --- Record mnemonics metadata for this well/file ---
    for curve in las.curves:
        mn = str(curve.mnemonic).strip()
        unit = (curve.unit or "").strip()
        desc = (curve.descr or "").strip()

        canonical = CANONICAL_MAP.get(mn.upper())
        family = canonical_to_family(canonical)

        cursor.execute(
            """
            INSERT INTO CurveMnemonics
                (well_id, file_key, mnemonic, unit, description, canonical_name, family)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (well_id, file_key, mn, unit, desc, canonical, family),
        )

    # --- Insert curve data for this file ---
    col_list = ", ".join([f'"{c}"' for c in curve_cols])
    placeholders = ", ".join(["?"] * (len(curve_cols) + 2))  # well_id + depth + curves

    insert_query = f"""
    INSERT INTO LogData (well_id, depth, {col_list})
    VALUES ({placeholders})
    """

    rows = []
    for _, row in df.iterrows():
        values = [well_id, row["depth"]]
        # For each curve in the unified list, use the value if present in this file, else None
        for c in curve_cols:
            values.append(row.get(c, None))
        rows.append(values)

    cursor.executemany(insert_query, rows)
    conn.commit()
    conn.close()

    print(f"  -> Inserted {len(rows)} rows for well_id={well_id} ({norm_name}).\n")


if __name__ == "__main__":
    LAS_DIR = Path(r"C:\Users\kbaah\Desktop\DB_ToyImp\LAS")

    las_files = list(LAS_DIR.glob("*.las")) + list(LAS_DIR.glob("*.csv"))
    print(f"Found {len(las_files)} LAS files to ingest.\n")

    if not las_files:
        raise SystemExit("No LAS files found in LAS directory.")

    # 1) Build union of curves across all files
    curve_cols = get_union_of_curves(las_files)

    if not curve_cols:
        raise SystemExit("No curves found in any LAS file – check files or read errors above.")

    # 2) Create DB schema with these curve columns (fresh DB each run)
    setup_database(curve_cols)

    # 3) Ingest each file (dedupe by file_key, so 'xxx.csv' and 'xxx (1).csv' count as same)
    for file in las_files:
        ingest_las_file(file, curve_cols)

    print("=== Ingestion completed for all files (where readable and not duplicate by file_key) ===")
