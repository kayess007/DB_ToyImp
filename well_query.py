import lasio
import os
import io
from db_connect import get_conn

conn = get_conn()
cur = conn.cursor()

def get_well_metadata(uwi):
    query = f"""
        SELECT *
        FROM well
        JOIN well_metadata ON well.uwi = well_metadata.uwi
        WHERE well.uwi = %s;
    """
    cur.execute(query, [uwi])
    return cur.fetchall()

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
            cn.name AS mnemonic_name,
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
    print(rows)

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
            cn.name AS mnemonic_name,
            wc.value
        from well_curve wc
        LEFT JOIN chosen_name cn
            ON wc.mnemonic = cn.mnemonic
        where wc.uwi = %s
            and wc.row_id in ({placeholders})
        ORDER BY wc.row_id;
    """
    cur.execute(query, [uwi] + rows)
    print(cur.fetchall())

def get_las(uwi):
    las = lasio.LASFile()
    las.well.clear()
    # Well Info Section
    for item in get_well_info(uwi):
        name = item["name"] or f"M{item['mnemonic_id']}"
        unit = item["unit"] or ""
        value = item["value"] or ""
        descr = item["description"] or ""

        las.well.append(lasio.HeaderItem(
            mnemonic =name,
            value=value,
            descr=descr,
            unit=unit
        ))

    curve_params = get_curve_info(uwi)
    for item in curve_params:
        name = item["name"] or f"M{item['mnemonic_id']}"
        unit = item["unit"] or ""
        descr = item["description"] or ""

        las.curves.append(lasio.CurveItem(
            mnemonic =name,
            descr=descr,
            unit=unit
        ))

    mnemonic_ids = [c["mnemonic_id"] for c in curve_params]
    get_curve_data(uwi, mnemonic_ids)

    return las

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
