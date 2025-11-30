import lasio
import os
import io
from db_connect import get_conn
from db_connect import get_cluster
from db_connect import get_session

conn = get_conn()
cur = conn.cursor()
cluster = get_cluster()
session = get_session(cluster)

def get_mnemonics(name_unit_pairs):
    conditions = " OR ".join(["(mnemonic_name.name = %s AND mnemonic.unit = %s)"] * len(name_unit_pairs))

    # Flatten the list of tuples for binding
    params = []
    for name, unit in name_unit_pairs:
        params += [name, unit]

    query = f"""
        SELECT mnemonic_name.name, mnemonic.unit, mnemonic.mnemonic_id
        FROM mnemonic_name
        JOIN mnemonic ON mnemonic_name.mnemonic = mnemonic.mnemonic_id
        WHERE {conditions};
    """
    cur.execute(query, params)
    return cur.fetchall()

def ext_name_unit_pairs(well):
    name_unit_pairs = []
    uwi = ""
    for item in well:
        mnemonic = item.mnemonic.strip()
        unit = (item.unit or "").strip()
        name_unit_pairs.append((mnemonic, unit))
        if mnemonic == "UWI":
            uwi = str(item.value).strip()

    return uwi, name_unit_pairs


def insert_well_info(uwi, well, mnemonic_dict):
    for item in well:
        name = item.mnemonic.strip()
        value = str(item.value).strip()

        if name not in mnemonic_dict:
            continue

        mnemonic_id = mnemonic_dict[name]

        cur.execute(
            """
            INSERT INTO well_param (uwi, mnemonic, value)
            VALUES (%s, %s, %s)
            ON CONFLICT (uwi, mnemonic) DO UPDATE SET value = EXCLUDED.value
            """,
            (uwi, mnemonic_id, value)
        )

    conn.commit()

def ext_name_unit_pairs_curve (curve):
    name_unit_pairs = []
    for item in curve:
        mnemonic = item.mnemonic.strip()
        unit = (item.unit or "").strip()
        name_unit_pairs.append((mnemonic, unit))

    return name_unit_pairs

def insert_curve(uwi, curves, mnemonic_dict):
    chunk_size = 2000
    mnemonic_ids = []
    curve_arrays = []

    for curve in curves:
        name = curve.mnemonic

        if name not in mnemonic_dict:
            continue

        m_id = mnemonic_dict[name]
        mnemonic_ids.append(m_id)

        curve_arrays.append([str(x) for x in curve.data])

    num_rows = len(curve_arrays[0])
    total_chunks = (num_rows + chunk_size - 1) // chunk_size

    insert_stmt = session.prepare("""
        INSERT INTO curve_info (uwi, mnemonics, chunks, chunk_size)
        VALUES (?, ?, ?, ?)
    """)
    session.execute(
        insert_stmt,
        (uwi, mnemonic_ids, total_chunks, chunk_size)
    )

    insert_stmt = session.prepare("""
        INSERT INTO curve_chunk (uwi, chunk_index, chunk_min, chunk_max, mnemonic_id, values)
        VALUES (?, ?, ?, ?, ?, ?)
    """)

    for chunk_index in range(total_chunks):
        start = chunk_index * chunk_size
        end = min(start + chunk_size, num_rows)

        for m_id, arr in zip(mnemonic_ids, curve_arrays):
            chunk_vals = arr[start:end]

            session.execute(
                insert_stmt,
                (uwi, chunk_index, chunk_vals[0], chunk_vals[-1], m_id, chunk_vals)
            )


def process_las(path):
    las = lasio.read(path, ignore_data=False)
    uwi, name_unit_pairs = ext_name_unit_pairs(las.well)
    
    if uwi == "":
        print('LAS file without UWI is not supported')
    
    well_mnemonic_dict = {name: mid for name, unit, mid in get_mnemonics(name_unit_pairs)}
    # insert_well_info(uwi, las.well, well_mnemonic_dict)

    curve_param_name_unit = ext_name_unit_pairs_curve(las.curves)
    curve_mnemonic_dict = {name: mid for name, unit, mid in get_mnemonics(curve_param_name_unit)}
    insert_curve(uwi, las.curves, curve_mnemonic_dict)

if __name__ == "__main__":
    
    input_file = "LAS-017963.csv"  # your file
    process_las(input_file)

    cur.close()
    conn.close()
    cluster.shutdown()
    
