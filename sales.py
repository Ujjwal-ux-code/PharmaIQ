import pandas as pd
from datetime import datetime

from settings import (
    MEDICINES_FILE,
    SALES_FILE
)

from utils import sale_id


def sales_menu():

    while True:

        print("\n")
        print("=" * 60)
        print("💰 SALES & BILLING")
        print("=" * 60)

        print("1. 🛒 Sell Medicine")
        print("2. 📜 Sales History")
        print("3. 📈 Sales Analytics")
        print("4. 🏆 Best Selling Medicines")
        print("5. ⬅ Back")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            sell_medicine()

        elif choice == "2":

            sales_history()

        elif choice == "3":

            sales_analytics()

        elif choice == "4":

            best_selling()

        elif choice == "5":

            break

        else:

            print("\nInvalid Choice.")


def sell_medicine():

    medicines = pd.read_csv(MEDICINES_FILE)
    sales = pd.read_csv(SALES_FILE)

    print("\n")
    print("=" * 65)
    print("                 🛒 SELL MEDICINE")
    print("=" * 65)

    if medicines.empty:

        print("\nNo medicines available.")
        return

    print("\nAvailable Medicines\n")

    print(
        medicines[
            [
                "Medicine_ID",
                "Medicine_Name",
                "Quantity",
                "Selling_Price"
            ]
        ].to_string(index=False)
    )

    medicine_id = input("\nEnter Medicine ID : ").strip().upper()

    if medicine_id not in medicines["Medicine_ID"].values:

        print("\nMedicine not found.")
        return

    index = medicines[
        medicines["Medicine_ID"] == medicine_id
    ].index[0]

    medicine = medicines.loc[index]

    current_stock = int(medicine["Quantity"])

    print(f"\nCurrent Stock : {current_stock}")

    try:

        quantity = int(input("Quantity to Sell : "))

    except ValueError:

        print("Invalid quantity.")
        return

    if quantity <= 0:

        print("Quantity must be greater than zero.")
        return

    if quantity > current_stock:

        print("\nInsufficient Stock.")
        return