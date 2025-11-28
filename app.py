import streamlit as st
import pandas as pd
import lasio

from create_well import create_well
from las_parser import process_las

st.set_page_config(page_title="Well Management System", layout="wide")

st.title("Well Management System")

page = st.sidebar.radio(
    "Navigation",
    ["Create Well", "Upload & Process LAS"],
)

if page == "Create Well":
    st.header("Create Well")

    with st.form("well_form"):
        uwi = st.text_input("UWI")

        col1, col2 = st.columns(2)

        with col1:
            well_name = st.text_input("Well Name")
            re_entry = st.number_input("Re-entry Count", min_value=0, step=1)
            operator = st.text_input("Operator")
            surface_lat = st.text_input("Surface Latitude (N83)")
            land_tenure = st.text_input("Land Tenure Area")
            datum = st.number_input("Datum (m)", step=1.0)

        with col2:
            surface_lon = st.text_input("Surface Longitude (N83)")
            classification = st.text_input("Classification")
            datum_elevation = st.text_input("Datum Elevation")
            spud_date = st.date_input("Spud Date")
            release_date = st.date_input("Release Date")

        submitted = st.form_submit_button("Create Well")

        if submitted:
            if not uwi:
                st.error("UWI is required.")
            elif not well_name:
                st.error("Well Name is required.")
            else:
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
                        str(release_date),
                    )
                    st.success(f"Well '{uwi}' created successfully.")
                except Exception as e:
                    st.error(f"Failed to create well: {e}")

elif page == "Upload & Process LAS":
    st.header("Upload & Process LAS File")

    uploaded = st.file_uploader(
        "Upload LAS file (.las or .csv)",
        type=["las", "csv"],
    )

    if uploaded is not None:
        st.write(f"File uploaded: {uploaded.name}")

        try:
            if uploaded.name.lower().endswith(".las"):
                las = lasio.read(uploaded)
                df = las.df().reset_index()
            else:
                df = pd.read_csv(uploaded)

            st.subheader("Preview")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"Could not preview file: {e}")
            df = None

        if st.button("Process File Into Database"):
            try:
                temp_path = f"temp_{uploaded.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded.getbuffer())

                process_las(temp_path)

                st.success("LAS file processed and stored in database.")
            except Exception as e:
                st.error(f"Error while processing LAS file: {e}")
    else:
        st.info("Please upload a LAS or CSV file.")
