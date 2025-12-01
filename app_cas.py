import streamlit as st
import pandas as pd
import lasio
from create_well import create_well
from las_parser_cas import process_las
from well_query_cas import get_las_range
from well_query_cas import get_las
from well_query_cas import get_las_metadata


def search_by_metadata(uwi):
    st.subheader("Search by Metadata")

    col1, col2 = st.columns(2)
    name = col1.text_input("Name")
    lta = col2.text_input("Land Tenure Area")
    
    if st.button("Search Metadata"):
        try:
            get_las_metadata(uwi, name, lta)
            st.success("Query successfully to output.txt.")
        except Exception as e:
            st.error(f"Error: {e}")


def search_by_params(uwi):
    st.subheader("Search by Set of Params")

    col1 = st.columns(1)
    mnemonics = col1[0].text_input("Mnemonics (separated by colon)")

    if st.button("Search Params"):
        try:
            get_las(uwi, [x.strip() for x in mnemonics.split(",")])
            st.success("Query successfully to output.txt.")
        except Exception as e:
            st.error(f"Error: {e}")


def search_by_range(uwi):
    st.subheader("Search by Range (Depth/Time)")

    col1, col2, col3 = st.columns(3)
    
    mnemonic = col1.text_input("Indexed by")
    start = col2.number_input("Start", format="%.10f")
    stop = col3.number_input("Stop", format="%.10f")

    if st.button("Search Range"):
        try:
            get_las_range(mnemonic,  start, stop, uwi)
            st.success("Query successfully to output.txt.")
        except Exception as e:
            st.error(f"Error: {e}")

def search_page():

    st.header("Search")
    col1 = st.columns(1)
    uwi = col1[0].text_input("UWI")
    st.divider()
    search_by_metadata(uwi)

    st.divider()
    search_by_params(uwi)

    st.divider()
    search_by_range(uwi)


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
