import pandas as pd

from datetime import datetime
from settings import MEDICINES_FILE
from settings import (
    MEDICINES_FILE,
    LOW_STOCK_LIMIT,
    EXPIRY_ALERT_DAYS
)


def inventory_menu():

    while True:

        print("\n")
        print("=" * 60)
        print("📦 INVENTORY MANAGEMENT")
        print("=" * 60)

        print("1. 📋 View Current Inventory")
        print("2. ➕ Restock Medicine")
        print("3. ⚠️ Low Stock Medicines")
        print("4. ❌ Out of Stock Medicines")
        print("5. 📅 Expired Medicines")
        print("6. ⏰ Near Expiry Medicines")
        print("7. 📊 Inventory Dashboard")
        print("8. ⬅️ Back")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            view_inventory()

        elif choice == "2":

            restock_medicine()

        elif choice == "3":

            low_stock_report()

        elif choice == "4":

            out_of_stock()

        elif choice == "5":

            expired_medicines()

        elif choice == "6":

            near_expiry()

        elif choice == "7":

            inventory_dashboard()

        elif choice == "8":

            break

        else:

            print("\nInvalid Choice.")


def view_inventory():

    medicines = pd.read_csv(MEDICINES_FILE)

    print("\n")
    print("=" * 120)
    print("                         CURRENT INVENTORY")
    print("=" * 120)

    if medicines.empty:

        print("\nNo medicines available.")

        return

    inventory = medicines.copy()

    inventory["Quantity"] = inventory["Quantity"].astype(int)

    def stock_status(quantity):

        if quantity == 0:
            return "Out of Stock"

        elif quantity <= LOW_STOCK_LIMIT:
            return "Low Stock"

        else:
            return "In Stock"

    inventory["Stock_Status"] = inventory["Quantity"].apply(stock_status)

    print(

        inventory[
            [
                "Medicine_ID",
                "Medicine_Name",
                "Category",
                "Quantity",
                "Purchase_Price",
                "Selling_Price",
                "Expiry_Date",
                "Stock_Status"
            ]
        ].to_string(index=False)

    )

def restock_medicine():

    medicines = pd.read_csv(MEDICINES_FILE)

    if medicines.empty:

        print("\nNo medicines available.")

        return

    medicine_id = input("\nEnter Medicine ID : ").strip().upper()

    if medicine_id not in medicines["Medicine_ID"].values:

        print("\nMedicine not found.")

        return

    index = medicines[medicines["Medicine_ID"] == medicine_id].index[0]

    current_stock = int(medicines.loc[index, "Quantity"])

    print(f"\nCurrent Stock : {current_stock}")

    try:

        quantity = int(input("Enter Quantity to Add : "))

        if quantity <= 0:

            print("Quantity must be greater than zero.")

            return

    except ValueError:

        print("Invalid quantity.")

        return

    medicines.loc[index, "Quantity"] = current_stock + quantity

    medicines.to_csv(MEDICINES_FILE, index=False)

    print("\n✅ Stock Updated Successfully!")

    print(f"New Stock : {current_stock + quantity}")


def low_stock_report():

    medicines = pd.read_csv(MEDICINES_FILE)

    print("\n")
    print("=" * 100)
    print("                  ⚠️ LOW STOCK MEDICINES")
    print("=" * 100)

    if medicines.empty:

        print("\nNo medicines available.")

        return

    medicines["Quantity"] = medicines["Quantity"].astype(int)

    low_stock = medicines[
        medicines["Quantity"] <= LOW_STOCK_LIMIT
    ]

    if low_stock.empty:

        print("\n🎉 Great! No medicines are running low.")

        return

    print(

        low_stock[
            [
                "Medicine_ID",
                "Medicine_Name",
                "Category",
                "Quantity",
                "Expiry_Date"
            ]
        ].to_string(index=False)

    )

    print("\nTotal Low Stock Medicines :", len(low_stock))


def out_of_stock():

    medicines = pd.read_csv(MEDICINES_FILE)

    print("\n")
    print("=" * 100)
    print("                  ❌ OUT OF STOCK MEDICINES")
    print("=" * 100)

    if medicines.empty:

        print("\nNo medicines available.")

        return

    medicines["Quantity"] = medicines["Quantity"].astype(int)

    out_stock = medicines[
        medicines["Quantity"] == 0
    ]

    if out_stock.empty:

        print("\n🎉 No medicines are out of stock.")

        return

    print(

        out_stock[
            [
                "Medicine_ID",
                "Medicine_Name",
                "Category",
                "Manufacturer",
                "Expiry_Date"
            ]
        ].to_string(index=False)

    )

    print("\nTotal Out of Stock Medicines :", len(out_stock))


def expired_medicines():

    medicines = pd.read_csv(MEDICINES_FILE)

    print("\n")
    print("=" * 110)
    print("                    📅 EXPIRED MEDICINES")
    print("=" * 110)

    if medicines.empty:

        print("\nNo medicines available.")

        return

    today = datetime.today().date()

    expired_list = []

    for _, medicine in medicines.iterrows():

        expiry = datetime.strptime(
            medicine["Expiry_Date"],
            "%d-%m-%Y"
        ).date()

        if expiry < today:

            days_expired = (today - expiry).days

            expired_list.append({

                "Medicine_ID": medicine["Medicine_ID"],

                "Medicine_Name": medicine["Medicine_Name"],

                "Category": medicine["Category"],

                "Expiry_Date": medicine["Expiry_Date"],

                "Days_Expired": days_expired

            })

    if len(expired_list) == 0:

        print("\n🎉 No expired medicines found.")

        return

    expired_df = pd.DataFrame(expired_list)

    print(expired_df.to_string(index=False))

    print("\nTotal Expired Medicines :", len(expired_df))


def near_expiry():

    medicines = pd.read_csv(MEDICINES_FILE)

    print("\n")
    print("=" * 115)
    print(f"          ⏰ MEDICINES EXPIRING WITHIN {EXPIRY_ALERT_DAYS} DAYS")
    print("=" * 115)

    if medicines.empty:

        print("\nNo medicines available.")

        return

    today = datetime.today().date()

    near_expiry_list = []

    for _, medicine in medicines.iterrows():

        expiry = datetime.strptime(
            medicine["Expiry_Date"],
            "%d-%m-%Y"
        ).date()

        days_left = (expiry - today).days

        if 0 <= days_left <= EXPIRY_ALERT_DAYS:

            near_expiry_list.append({

                "Medicine_ID": medicine["Medicine_ID"],

                "Medicine_Name": medicine["Medicine_Name"],

                "Category": medicine["Category"],

                "Expiry_Date": medicine["Expiry_Date"],

                "Days_Left": days_left

            })

    if len(near_expiry_list) == 0:

        print(f"\n🎉 No medicines expiring within {EXPIRY_ALERT_DAYS} days.")

        return

    near_expiry_df = pd.DataFrame(near_expiry_list)

    near_expiry_df = near_expiry_df.sort_values("Days_Left")

    print(near_expiry_df.to_string(index=False))

    print("\nTotal Near Expiry Medicines :", len(near_expiry_df))