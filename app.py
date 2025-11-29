import streamlit as st
import pandas as pd
import lasio
from create_well import create_well
from las_parser import process_las
from db_connect import get_conn


def run_query(query, params=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return pd.DataFrame(rows, columns=colnames)


def search_by_metadata():
    st.subheader("Search by Metadata")

    col1, col2 = st.columns(2)
    uwi = col1.text_input("UWI (Metadata)")
    name = col2.text_input("Name")

    if st.button("Search Metadata"):
        query = """
            SELECT * FROM well
            WHERE (%s = '' OR uwi = %s)
              AND (%s = '' OR well_name ILIKE %s)
        """
        df = run_query(query, (uwi, uwi, name, f"%{name}%"))
        st.dataframe(df)


def search_by_params():
    st.subheader("Search a Set of Params")

    col1, col2 = st.columns(2)
    uwi = col1.text_input("UWI (Param)")
    mnemonic = col2.text_input("Mnemonic")

    if st.button("Search Params"):
        query = """
            SELECT wp.uwi, cp.mnemonic, wp.row_id, wp.value
            FROM well_curve wp
            JOIN curve_param cp ON wp.curve_id = cp.id
            WHERE (%s = '' OR wp.uwi = %s)
              AND (%s = '' OR cp.mnemonic = %s)
        """
        df = run_query(query, (uwi, uwi, mnemonic, mnemonic))
        st.dataframe(df)


def search_by_range():
    st.subheader("Search by Depth Range")

    col1, col2, col3 = st.columns(3)
    uwi = col1.text_input("UWI (Range)")
    start = col2.number_input("Start Row", step=1.0)
    stop = col3.number_input("Stop Row", step=1.0)

    if st.button("Search Range"):
        query = """
            SELECT wp.uwi, cp.mnemonic, wp.row_id, wp.value
            FROM well_curve wp
            JOIN curve_param cp ON wp.curve_id = cp.id
            WHERE (%s = '' OR wp.uwi = %s)
              AND wp.row_id BETWEEN %s AND %s
        """
        df = run_query(query, (uwi, uwi, start, stop))
        st.dataframe(df)


def search_page():
    st.header("Search")

    st.divider()
    search_by_metadata()

    st.divider()
    search_by_params()

    st.divider()
    search_by_range()


st.set_page_config(page_title="Well Management System", layout="wide")

st.title("Well Management System")

page = st.sidebar.radio(
    "Navigation",
    ["Create Well", "Upload LAS", "Search"]
)

if page == "Create Well":
    st.header("Create Well")

    with st.form("well_form"):
        uwi = st.text_input("UWI")
        col1, col2 = st.columns(2)

        with col1:
            well_name = st.text_input("Well Name")
            re_entry = st.number_input("Re-entry", min_value=0, step=1)
            operator = st.text_input("Operator")
            surface_lat = st.text_input("Surface Lat (N83)")
            land_tenure = st.text_input("Land Tenure")
            datum = st.number_input("Datum", step=1.0)

        with col2:
            surface_lon = st.text_input("Surface Lon (N83)")
            classification = st.text_input("Classification")
            datum_elevation = st.text_input("Datum Elevation")
            spud_date = st.date_input("Spud Date")
            release_date = st.date_input("Release Date")

        submitted = st.form_submit_button("Create Well")

        if submitted:
            try:
                create_well(
                    uwi,
                    well_name,
                    re_entry,
                    operator,
                    surface_lat,
                    surface_lon,
                    land_tenure,
                    classification,
                    datum,
                    datum_elevation,
                    str(spud_date),
                    str(release_date)
                )
                st.success("Well created successfully.")
            except Exception as e:
                st.error(f"Error: {e}")


elif page == "Upload LAS":
    st.header("Upload & Process LAS File")

    uploaded = st.file_uploader("Upload LAS file (.las or .csv)", type=["las", "csv"])

    if uploaded is not None:
        st.write(f"Successfully Uploaded File: {uploaded.name}")

        try:
            if uploaded.name.lower().endswith(".las"):
                las = lasio.read(uploaded)
                df = las.df().reset_index()
            else:
                df = pd.read_csv(uploaded)

            st.subheader("Preview")
            st.dataframe(df.head())

        except Exception as e:
            st.error(f"Preview failed: {e}")
            df = None

        if st.button("Process File"):
            try:
                temp_path = f"temp_{uploaded.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded.getbuffer())

                process_las(temp_path)
                st.success("LAS processed into DB.")
            except Exception as e:
                st.error(f"Error: {e}")

elif page == "Search":
    search_page()
