import lasio
import json
import os

def ascii(df):
    # Replace nulls (-999.25 is standard LAS null)
    df = df.replace(-999.25, None)

    # Ensure DEPT exists as a column
    df = df.reset_index()  # DEPT becomes a column again

    # Set DEPT as index, then convert to JSON
    depth_json = df.set_index("DEPT").to_json(orient="index")

    # Convert JSON string → object
    return json.loads(depth_json)

def parse_las_to_json(path):
    # lasio automatically detects encoding and LAS formatting
    las = lasio.read(path, ignore_data=False)
    # ---- Extract well metadata ----
    well_info = {}
    for item in las.well:
        key = item.mnemonic.strip()
        well_info[key] = {
            "value": item.value,
            "unit": item.unit,
            "description": item.descr
        }

    # ---- Extract curve information ----
    curve_info = {}
    for curve in las.curves:
        curve_info[curve.mnemonic] = {
            "unit": curve.unit,
            "description": curve.descr
        }

    # ---- Extract data for each curve ----
    # las.curves[i].data gives a numpy array
    # data = {}
    # for curve in las.curves:
    #     data[curve.mnemonic] = las[curve.mnemonic].tolist()

    # ---- Construct the final JSON object ----
    json_obj = {
        "filename": os.path.basename(path),
        "well_information": well_info,
        "curve_information": curve_info,
        "ascii": ascii(las.df())
    }

    return json_obj


if __name__ == "__main__":
    input_file = "LAS-017959.csv"  # your file
    output_file = "LAS-017959.json"

    parsed = parse_las_to_json(input_file)

    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(parsed, out, indent=4)

    print(f"Saved JSON to {output_file}")
