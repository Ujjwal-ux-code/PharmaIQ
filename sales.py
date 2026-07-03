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

    unit_price = float(medicine["Selling_Price"])
    purchase_price = float(medicine["Purchase_Price"])

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
    
    discount = 0.0

    total_amount = (unit_price * quantity) - discount

    profit = (unit_price - purchase_price) * quantity
    
    unit_price = float(medicine["Selling_Price"])
    purchase_price = float(medicine["Purchase_Price"])

    discount = 0.0

    total_amount = (unit_price * quantity) - discount

    profit = (unit_price - purchase_price) * quantity

    medicines.loc[index, "Quantity"] = current_stock - quantity

    medicines.to_csv(MEDICINES_FILE, index=False)

    sale = {

        "Sale_ID": sale_id(),

        "Medicine_ID": medicine["Medicine_ID"],

        "Medicine_Name": medicine["Medicine_Name"],

        "Quantity": quantity,

        "Unit_Price": unit_price,

        "Discount": discount,

        "Total_Amount": total_amount,

        "Profit": profit,

        "Sale_Date": datetime.today().strftime("%d-%m-%Y"),

        "Sale_Time": datetime.today().strftime("%H:%M:%S")

    }

    sales = pd.concat(
        [sales, pd.DataFrame([sale])],
        ignore_index=True
    )

    sales.to_csv(SALES_FILE, index=False)

    print("\n")
    print("=" * 60)
    print("                 🧾 PHARMAIQ INVOICE")
    print("=" * 60)

    print(f"Sale ID        : {sale['Sale_ID']}")
    print(f"Date           : {sale['Sale_Date']}")
    print(f"Time           : {sale['Sale_Time']}")

    print("-" * 60)

    print(f"Medicine       : {medicine['Medicine_Name']}")
    print(f"Medicine ID    : {medicine['Medicine_ID']}")
    print(f"Quantity       : {quantity}")
    print(f"Unit Price     : ₹{unit_price:.2f}")
    print(f"Discount       : ₹{discount:.2f}")

    print("-" * 60)

    print(f"Total Amount   : ₹{total_amount:.2f}")
    print(f"Profit Earned  : ₹{profit:.2f}")

    print("=" * 60)
    print("       Thank you for choosing PharmaIQ!")
    print("=" * 60)

def sales_history():

    sales = pd.read_csv(SALES_FILE)

    print("\n")
    print("=" * 90)
    print("                     📜 SALES HISTORY")
    print("=" * 90)

    if sales.empty:

        print("\nNo sales found.")
        return

    print(

    sales[
        [
            "Sale_ID",
            "Medicine_Name",
            "Quantity",
            "Total_Amount",
            "Sale_Date"
        ]
    ].to_string(index=False)

)