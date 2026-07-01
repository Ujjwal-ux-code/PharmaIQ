import pandas as pd
from datetime import datetime

from settings import MEDICINES_FILE
from utils import medicine_id, generate_sku


def add_medicine():

    medicines = pd.read_csv(MEDICINES_FILE)

    print("\n")
    print("=" * 55)
    print("              ➕ ADD MEDICINE")
    print("=" * 55)

    medicine_name = input("Medicine Name : ").strip()

    generic_name = input("Generic Name : ").strip()

    category = input(
        "Category (Tablet/Syrup/Capsule/etc.) : "
    ).strip()

    batch = input("Batch Number : ").strip()

    manufacturer = input("Manufacturer : ").strip()

    supplier = input("Supplier ID : ").strip()

    if not medicines.empty:

        if batch in medicines["Batch_No"].astype(str).values:

            print("\n❌ Batch already exists.")

            return

    try:

        purchase = float(input("Purchase Price : ₹"))

        selling = float(input("Selling Price : ₹"))

        quantity = int(input("Quantity : "))

    except ValueError:

        print("Invalid numeric value.")

        return

    expiry = input("Expiry Date (DD-MM-YYYY) : ")

    try:

        datetime.strptime(expiry, "%d-%m-%Y")

    except ValueError:

        print("Invalid date format.")

        return

    sku = generate_sku(
        category,
        medicine_name,
        medicines
    )

    new_row = {

        "Medicine_ID": medicine_id(),

        "SKU": sku,

        "Medicine_Name": medicine_name,

        "Generic_Name": generic_name,

        "Category": category,

        "Batch_No": batch,

        "Manufacturer": manufacturer,

        "Supplier_ID": supplier,

        "Purchase_Price": purchase,

        "Selling_Price": selling,

        "Quantity": quantity,

        "Expiry_Date": expiry

    }

    medicines = pd.concat(

        [

            medicines,

            pd.DataFrame([new_row])

        ],

        ignore_index=True

    )

    medicines.to_csv(
        MEDICINES_FILE,
        index=False
    )

    print("\n✅ Medicine Added Successfully!")

    print("Medicine ID :", new_row["Medicine_ID"])

    print("SKU :", sku)

def view_medicines():

    medicines = pd.read_csv(MEDICINES_FILE)

    print("\n")
    print("=" * 100)
    print("                     MEDICINES")
    print("=" * 100)

    if medicines.empty:

        print("\nNo medicines available.")

        return

    print(medicines.to_string(index=False))

def search_medicine():

    medicines = pd.read_csv(MEDICINES_FILE)

    if medicines.empty:

        print("\nNo medicines found.")

        return

    keyword = input(
        "\nEnter Medicine ID, Name, Batch or Manufacturer : "
    ).strip().lower()

    result = medicines[

        medicines["Medicine_ID"].astype(str).str.lower().str.contains(keyword)

        |

        medicines["Medicine_Name"].astype(str).str.lower().str.contains(keyword)

        |

        medicines["Batch_No"].astype(str).str.lower().str.contains(keyword)

        |

        medicines["Manufacturer"].astype(str).str.lower().str.contains(keyword)

    ]

    print("\n")
    print("=" * 100)
    print("                 SEARCH RESULT")
    print("=" * 100)

    if result.empty:

        print("\nNo medicine found.")

    else:

        print(result.to_string(index=False))

def update_medicine():

    medicines = pd.read_csv(MEDICINES_FILE)

    if medicines.empty:

        print("\nNo medicines available.")

        return

    medicine_id = input("\nEnter Medicine ID to update : ").strip().upper()

    if medicine_id not in medicines["Medicine_ID"].values:

        print("\nMedicine not found.")

        return

    index = medicines[medicines["Medicine_ID"] == medicine_id].index[0]

    print("\nLeave blank to keep existing value.\n")

    fields = [
        "Medicine_Name",
        "Generic_Name",
        "Category",
        "Batch_No",
        "Manufacturer",
        "Supplier_ID",
        "Purchase_Price",
        "Selling_Price",
        "Quantity",
        "Expiry_Date"
    ]

    for field in fields:

        current = medicines.loc[index, field]

        value = input(f"{field} ({current}) : ").strip()

        if value == "":
            continue

        if field == "Purchase_Price":
            medicines.loc[index, field] = float(value)

        elif field == "Selling_Price":
            medicines.loc[index, field] = float(value)

        elif field == "Quantity":
            medicines.loc[index, field] = int(value)

        elif field == "Expiry_Date":

            try:
                datetime.strptime(value, "%d-%m-%Y")
                medicines[field] = medicines[field].astype("object")
                medicines.loc[index, field] = value

            except ValueError:
                print("Invalid Date. Keeping old value.")

        else:
            medicines[field] = medicines[field].astype("object")
            medicines.loc[index, field] = value

    medicines.to_csv(MEDICINES_FILE, index=False)

    print("\nMedicine Updated Successfully!")

def medicine_menu():

    while True:

        print("\n")
        print("=" * 55)
        print("💊 MEDICINE MANAGEMENT")
        print("=" * 55)

        print("1. Add Medicine")
        print("2. View Medicine")
        print("3. Search Medicine")
        print("4. Update Medicine")
        print("5. Back")

        choice = input("\nEnter Choice : ")
        if choice == "1":
            add_medicine()
        elif choice == "2":
            view_medicines()
        elif choice == "3":
            search_medicine()
        elif choice == "4":
            update_medicine()
        elif choice == "5":
            break
        else:
            print("Invalid Choice.")