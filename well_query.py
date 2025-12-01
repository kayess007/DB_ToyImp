import lasio
import os
import io
from collections import defaultdict
from db_connect import get_conn
from helper import write_well_info
from helper import write_curve_info
from helper import write_curve_data

conn = get_conn()
cur = conn.cursor()

def get_mnemonic_def(mnemonic_names):
    placeholders = ",".join(["%s"] * len(mnemonic_names))
    cur.execute(f"""
        SELECT 
            m.mnemonic_id,
            mn.name,
            m.unit,
            m.description
        FROM mnemonic m
        JOIN mnemonic_name mn
            ON m.mnemonic_id = mn.mnemonic
        WHERE mn.name in ({placeholders})
        ORDER BY m.mnemonic_id;
    """, mnemonic_names)

    rows = cur.fetchall()
    mnemonic_dict = {}
    for mnemonic_id, name, unit, desc in rows:
        mnemonic_dict[mnemonic_id] = {
            "name": name,    
            "unit": unit,
            "description": desc
        }
    return mnemonic_dict

def get_well_metadata(uwi):
    query = f"""
        SELECT *
        FROM well
        JOIN well_metadata ON well.uwi = well_metadata.uwi
        WHERE well.uwi = %s;
    """
    cur.execute(query, [uwi])
    return cur.fetchall()

def get_well_uwi(uwi, name, lta):
    query = f"""
        SELECT well.uwi
        FROM well
        JOIN well_metadata m ON well.uwi = m.uwi
        WHERE well.uwi = %s
            OR m.well_name = %s
            OR m.land_tenure_area = %s;
    """
    cur.execute(query, [uwi, name, lta])
    return [row[0] for row in cur.fetchall()]

def get_well_info(uwi):
    cur.execute("""
        WITH chosen_name AS (
            SELECT DISTINCT ON (mnemonic)
                mnemonic,
                name
            FROM mnemonic_name
            ORDER BY mnemonic, name
        )
        SELECT 
            wp.uwi,
            wp.mnemonic,
            cn.name AS mnemonic_name,
            m.unit,
            m.description,
            wp.value
        FROM well_param wp
        JOIN mnemonic m
            ON wp.mnemonic = m.mnemonic_id
        LEFT JOIN chosen_name cn
            ON wp.mnemonic = cn.mnemonic
        WHERE wp.uwi = %s
        ORDER BY wp.mnemonic;

    """, (uwi,))
    rows = cur.fetchall()
    result = []
    for uwi, mnemonic_id, name, unit, desc, val in rows:
        result.append({
            "mnemonic_id": mnemonic_id,
            "name": name,    
            "unit": unit,
            "description": desc,
            "value": val
        })
    return result

def get_curve_info(uwi):
    cur.execute("""
        WITH chosen_name AS (
            SELECT DISTINCT ON (mnemonic)
                mnemonic,
                name
            FROM mnemonic_name
            ORDER BY mnemonic, name
        )
        SELECT 
            cp.uwi,
            cp.mnemonic,
            cn.name AS mnemonic_name,
            m.unit,
            m.description
        FROM curve_param cp
        JOIN mnemonic m
            ON cp.mnemonic = m.mnemonic_id
        LEFT JOIN chosen_name cn
            ON cp.mnemonic = cn.mnemonic
        WHERE cp.uwi = %s
        ORDER BY cp.mnemonic;

    """, (uwi,))
    rows = cur.fetchall()
    result = []
    for uwi, mnemonic_id, name, unit, desc in rows:
        result.append({
            "mnemonic_id": mnemonic_id,
            "name": name,    
            "unit": unit,
            "description": desc
        })
    return result

# get certain set of parameters over all depths
def get_curve_data(uwi, mnemonics):
    placeholders = ",".join(["%s"] * len(mnemonics))
    query = f"""
        WITH chosen_name AS (
            SELECT DISTINCT ON (mnemonic)
                mnemonic,
                name
            FROM mnemonic_name
            ORDER BY mnemonic, name
        )
        SELECT 
            wc.row_id,
            cn.name,
            wc.value
        FROM well_curve wc
        JOIN mnemonic m
            ON wc.mnemonic = m.mnemonic_id
        LEFT JOIN chosen_name cn
            ON wc.mnemonic = cn.mnemonic
        WHERE wc.uwi = %s AND wc.mnemonic IN ({placeholders})
        ORDER BY wc.row_id;
    """
    cur.execute(query, [uwi] + mnemonics)
    rows = cur.fetchall()
    grouped = defaultdict(list)

    for row in rows:
        grouped[row[1]].append(row[2])

    return list(grouped.items())

def get_curve_in_range(mnemonic, start, stop, uwi):
    query = r"""
        select row_id
        from well_curve wc
        join mnemonic_name mn on mn.mnemonic = wc.mnemonic
        where wc.uwi = %s
            and mn.name = %s
            and wc.value ~ '^[0-9]+(\.[0-9]+)?$'
            and cast(wc.value as double precision) between %s and %s;
    """
    cur.execute(query, (uwi, mnemonic, start, stop))
    rows = [row[0] for row in cur.fetchall()]

    placeholders = ",".join(["%s"] * len(rows))
    query = f"""
        WITH chosen_name AS (
            SELECT DISTINCT ON (mnemonic)
                mnemonic,
                name
            FROM mnemonic_name
            ORDER BY mnemonic, name
        )
        select 
            wc.row_id,
            cn.name,
            wc.value
        from well_curve wc
        LEFT JOIN chosen_name cn
            ON wc.mnemonic = cn.mnemonic
        where wc.uwi = %s
            and wc.row_id in ({placeholders})
        ORDER BY wc.row_id;
    """
    cur.execute(query, [uwi] + rows)
    rows = cur.fetchall()
    grouped = defaultdict(list)

    for row in rows:
        grouped[row[1]].append(row[2])

    return list(grouped.items())

def get_las_range(mnemonic_name, start, stop, uwi):
    well_info = get_well_info(uwi)
    curve_params = get_curve_info(uwi)
    curve_data = get_curve_in_range(mnemonic_name, start, stop, uwi)
    write_well_info(well_info)
    write_curve_info(curve_params)
    write_curve_data(curve_data)

def get_las(uwi, mnemonic_names):
    well_info = get_well_info(uwi)
    mnemonic_dict = get_mnemonic_def(mnemonic_names)
    curve_params = get_curve_info(uwi)
    mnemonic_ids = [c["mnemonic_id"] for c in curve_params]
    selected = [m_id for m_id in mnemonic_ids if m_id in mnemonic_dict]
    curve_data = get_curve_data(uwi, selected)
    write_well_info(well_info)
    write_curve_info(curve_params)
    write_curve_data(curve_data)

def get_las_metadata(uwi, name, lta):
    uwis = get_well_uwi(uwi, name, lta)
    for uwi in uwis:
        well_info = get_well_info(uwi)
        curve_params = get_curve_info(uwi)
        mnemonic_ids = [c["mnemonic_id"] for c in curve_params]
        curve_data = get_curve_data(uwi, mnemonic_ids)
        write_well_info(well_info)
        write_curve_info(curve_params)
        write_curve_data(curve_data)

if __name__ == "__main__":
    uwi = '302B164650048451'
    #print(get_well_metadata('302B164650048451'))
    # las = get_las(uwi)
    # print(las.well)
    # output_file = f"{uwi}_well.las"
    # las.write(output_file)
    get_curve_in_range('DEPT', 100, 200, uwi)

    cur.close()
    conn.close()
