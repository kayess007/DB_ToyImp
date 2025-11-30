from db_connect import get_cluster
from db_connect import get_session
from db_connect import get_conn
from well_query import get_well_uwi
from well_query import get_mnemonic_def
import bisect

conn = get_conn()
cur = conn.cursor()
cluster = get_cluster()
session = get_session(cluster)

def get_mnemonic_def_id(mnemonic_ids):
    placeholders = ",".join(["%s"] * len(mnemonic_ids))
    cur.execute(f"""
        WITH chosen_name AS (
            SELECT DISTINCT ON (mnemonic)
                mnemonic,
                name
            FROM mnemonic_name
            ORDER BY mnemonic, name
        )
        select 
            m.mnemonic_id,
            cn.name,
            m.unit,
            m.description
        from mnemonic m
        LEFT JOIN chosen_name cn
            ON m.mnemonic_id = cn.mnemonic
        where m.mnemonic_id in ({placeholders})
        ORDER BY m.mnemonic_id;
    """, mnemonic_ids)

    rows = cur.fetchall()
    mnemonic_dict = {}
    for mnemonic_id, name, unit, desc in rows:
        mnemonic_dict[mnemonic_id] = {
            "name": name,    
            "unit": unit,
            "description": desc
        }
    return mnemonic_dict

def get_curve_info(uwi):
    info_stmt = session.prepare(
        "SELECT mnemonics, chunks FROM curve_info WHERE uwi = ?"
    )
    info_row = session.execute(info_stmt, [uwi]).one()

    mnemonics = info_row.mnemonics
    total_chunks = info_row.chunks
    return mnemonics, total_chunks

def get_curve_data(uwi, chunks, mnemonics):
    placeholders = ",".join(["?"] * len(mnemonics))
    chunk_query = f"""
        SELECT mnemonic_id, values
        FROM curve_chunk
        WHERE uwi = ?
          AND chunk_index = ?
          AND mnemonic_id IN ({placeholders})
    """
    chunk_stmt = session.prepare(chunk_query)

    result = {mnemonic_id: [] for mnemonic_id in mnemonics}

    for chunk_index in range(chunks):
        params = [uwi, chunk_index] + mnemonics
        rows = session.execute(chunk_stmt, params)

        for row in rows:
            result[row.mnemonic_id].extend(row.values)

    return result

def get_chunks(mnemonic, start, stop, uwi, chunks):
    chunk_query = f"""
        SELECT chunk_index, chunk_min, chunk_max
        FROM curve_chunk
        WHERE uwi = ?
            AND chunk_index = ?
            AND mnemonic_id = ?
    """
    chunk_stmt = session.prepare(chunk_query)

    valid_chunks = []
    for chunk_index in range(chunks):
        row = session.execute(chunk_stmt, (uwi, chunk_index, mnemonic)).one()
        cmin = float(row.chunk_min)
        cmax = float(row.chunk_max)
        start_included = cmin <= start and start <= cmax
        stop_included = cmin <= stop and stop <= cmax
        if start_included or stop_included:
            valid_chunks.append(chunk_index)
        if start_included and stop_included:
            break

    chunk_query = f"""
        SELECT mnemonic_id, values
        FROM curve_chunk
        WHERE uwi = ?
            AND chunk_index = ?
    """
    chunk_stmt = session.prepare(chunk_query)
    result = {}

    for chunk_index in valid_chunks:
        rows = session.execute(chunk_stmt, (uwi, chunk_index))
        for row in rows:
            result.setdefault(row.mnemonic_id, []).extend(row.values)

    cast = [float(x) for x in result[mnemonic]]
    start_idx = bisect.bisect_left(cast, start)
    stop_idx = bisect.bisect_right(cast, stop)
    for m in result:
        result[m] = result[m][start_idx:stop_idx]
    return result
        

def get_las_range(mnemonic_name, start, stop, uwi):
    mnemonics, chunks = get_curve_info(uwi)
    mnemonic_dict = get_mnemonic_def_id(mnemonics)

    mnemonic_id = next((k for k, v in mnemonic_dict.items() if v['name'] == mnemonic_name), None)
    curve_data = get_chunks(mnemonic_id, start, stop, uwi, chunks)
    curve_ascii = {mnemonic_dict[mid]['name']: curve_data[mid] for mid in mnemonics}
    print(curve_ascii)


def get_las(uwi, mnemonic_names):
    mnemonic_dict = get_mnemonic_def(mnemonic_names)
    mnemonic_ids, total_chunks = get_curve_info(uwi)
    selected = [m_id for m_id in mnemonic_ids if m_id in mnemonic_dict]
    curve_data = get_curve_data(uwi, total_chunks, selected)
    curve_ascii = {mnemonic_dict[mid]['name']: curve_data[mid] for mid in selected}
    print(curve_ascii)

def get_las_metadata(uwi, name, lta):
    uwis = get_well_uwi(uwi, name, lta)
    for uwi in uwis:
        mnemonics, chunks = get_curve_info(uwi)
        mnemonic_dict = get_mnemonic_def_id(mnemonics)
        curve_data = get_curve_data(uwi, chunks, mnemonics)
        curve_ascii = {mnemonic_dict[mid]['name']: curve_data[mid] for mid in mnemonics}
        print(curve_ascii)

if __name__ == "__main__":
    uwi = '302B164650048451'

    # get_las(uwi, ['DEPT','TIME'])
    get_las_range('TIME_1900',  45725.3750000000, 45725.9027777778, uwi)

    cur.close()
    conn.close()
    cluster.shutdown()