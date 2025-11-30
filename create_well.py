import io
from db_connect import get_conn

conn = get_conn()
cur = conn.cursor()

def create_well(uwi, name, re, op, lat, lon, lta, classification, datum, datum_e, spud, release):
    cur.execute(
        """
        INSERT INTO well (uwi)
        VALUES (%s)
        """,
        (uwi,)
    )
    cur.execute(
        """
        INSERT INTO well_metadata (uwi, well_name, re_entry, operator, surface_lat_n83, surface_lon_n83,
                                    land_tenure_area, classification, datum, datum_elevation, spud_date, release_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (uwi, name, re, op, lat, lon, lta, classification, datum, datum_e, spud, release)
    )
    conn.commit()

if __name__ == "__main__":
    
    create_well('302B164650048451', 'Hibernia B-16 2Z', 0, 'HMDC', '46° 45\' 02.08"', '48° 46\' 54.45"',
     "Jeanne d'Arc", 'Development', 76.0, 'RT', '2025-11-30', '2025-11-30')																																	

    cur.close()
    conn.close()
