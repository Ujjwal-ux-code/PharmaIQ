from datetime import datetime

from utils import (
    initialize_data,
    first_time_setup,
    pharmacy_details
)

from medicines import medicine_menu
#from inventory import inventory_menu
#from sales import sales_menu
#from suppliers import supplier_menu
#from reports import reports_menu


def header():

    details = pharmacy_details()

    print("\n")
    print("=" * 60)
    print("                 💊 PHARMAIQ")
    print("=" * 60)

    if details is not None:

        print(f"🏥 Pharmacy : {details['Pharmacy_Name']}")
        print(f"👨 Owner    : {details['Owner_Name']}")

    print(f"📅 Date     : {datetime.today().strftime('%d-%m-%Y')}")

    print("=" * 60)


def main():

    initialize_data()

    first_time_setup()

    while True:

        header()

        print("\n")
        print("1. 💊 Medicine Management")
        print("2. 📦 Inventory")
        print("3. 💰 Sales")
        print("4. 🚚 Suppliers")
        print("5. 📊 Reports")
        print("6. 🚪 Exit")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            medicine_menu()

        elif choice == "2":

            inventory_menu()

        elif choice == "3":

            sales_menu()

        elif choice == "4":

            supplier_menu()

        elif choice == "5":

            reports_menu()

        elif choice == "6":

            print("\nThank you for using PharmaIQ.")
            break

        else:

            print("\nInvalid Choice.")


if __name__ == "__main__":

    main()