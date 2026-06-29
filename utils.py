import os
import pandas as pd

from settings import *


def initialize_data():

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    files = {

        MEDICINES_FILE: [

            "Medicine_ID",
            "Medicine_Name",
            "Category",
            "Batch_No",
            "Manufacturer",
            "Supplier_ID",
            "Purchase_Price",
            "Selling_Price",
            "Quantity",
            "Expiry_Date"

        ],

        SALES_FILE: [

            "Sale_ID",
            "Medicine_ID",
            "Medicine_Name",
            "Quantity",
            "Total_Amount",
            "Sale_Date"

        ],

        SUPPLIERS_FILE: [

            "Supplier_ID",
            "Supplier_Name",
            "Phone",
            "Email",
            "Address"

        ],

        SETTINGS_FILE: [

            "Pharmacy_Name",
            "Owner_Name",
            "GST_Number"

        ]

    }

    for file, columns in files.items():

        if not os.path.exists(file):

            pd.DataFrame(columns=columns).to_csv(file, index=False)

            print(f"✓ {os.path.basename(file)} created.")


def first_time_setup():

    settings = pd.read_csv(SETTINGS_FILE)

    if not settings.empty:
        return

    print("\n========== PHARMAIQ SETUP ==========\n")

    pharmacy = input("Pharmacy Name : ")
    owner = input("Owner Name : ")
    gst = input("GST Number : ")

    data = pd.DataFrame({

        "Pharmacy_Name": [pharmacy],
        "Owner_Name": [owner],
        "GST_Number": [gst]

    })

    data.to_csv(SETTINGS_FILE, index=False)

    print("\nSetup Completed Successfully.\n")


def pharmacy_details():

    df = pd.read_csv(SETTINGS_FILE)

    if df.empty:
        return None

    return df.iloc[0]


def medicine_id():

    df = pd.read_csv(MEDICINES_FILE)

    if df.empty:
        return "MED001"

    last = df.iloc[-1]["Medicine_ID"]

    number = int(last[3:]) + 1

    return f"MED{number:03d}"


def supplier_id():

    df = pd.read_csv(SUPPLIERS_FILE)

    if df.empty:
        return "SUP001"

    last = df.iloc[-1]["Supplier_ID"]

    number = int(last[3:]) + 1

    return f"SUP{number:03d}"


def sale_id():

    df = pd.read_csv(SALES_FILE)

    if df.empty:
        return "SAL001"

    last = df.iloc[-1]["Sale_ID"]

    number = int(last[3:]) + 1

    return f"SAL{number:03d}"


def clear():

    os.system("cls" if os.name == "nt" else "clear")