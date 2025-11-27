import lasio
import os
import io
import psycopg2

conn = psycopg2.connect(
    dbname="welllogs",
    user="admin",
    password="admin",
    host="localhost",
)

cur = conn.cursor()

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
        # value = str(item.value).strip()
        # descr = (item.descr or "").strip()
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

def insert_curve_param(uwi, curves, mnemonic_dict):
    for item in curves:
        name = item.mnemonic.strip()

        if name not in mnemonic_dict:
            continue

        mnemonic_id = mnemonic_dict[name]

        cur.execute(
            """
            INSERT INTO curve_param (uwi, mnemonic)
            VALUES (%s, %s)
            """,
            (uwi, mnemonic_id)
        )

    conn.commit()

def insert_ascii (uwi, curves, mnemonic_dict):
    buf = io.StringIO()
    for item in curves:
        if item.mnemonic not in mnemonic_dict:
            continue

        mnemonic_id = mnemonic_dict[item.mnemonic]
        values = item.data

        for row_id, value in enumerate(values):
            buf.write(f"{uwi}\t{mnemonic_id}\t{row_id + 1}\t{value}\n")

    buf.seek(0)

    cur.copy_from(
        file=buf,
        table="well_curve",
        columns=("uwi", "mnemonic", "row_id", "value"),
        sep="\t"
    )

    conn.commit()

def process_las(path):
    las = lasio.read(path, ignore_data=False)
    uwi, name_unit_pairs = ext_name_unit_pairs(las.well)
    
    if uwi == "":
        print('LAS file without UWI is not supported')
    
    well_mnemonic_dict = {name: mid for name, unit, mid in get_mnemonics(name_unit_pairs)}
    insert_well_info(uwi, las.well, well_mnemonic_dict)

    curve_param_name_unit = ext_name_unit_pairs_curve(las.curves)
    curve_mnemonic_dict = {name: mid for name, unit, mid in get_mnemonics(curve_param_name_unit)}
    insert_curve_param(uwi, las.curves, curve_mnemonic_dict)
    insert_ascii(uwi, las.curves, curve_mnemonic_dict)


if __name__ == "__main__":
    

    input_file = "LAS-017963.csv"  # your file
    process_las(input_file)

    cur.close()
    conn.close()
