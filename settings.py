import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

MEDICINES_FILE = os.path.join(DATA_DIR, "medicines.csv")
SALES_FILE = os.path.join(DATA_DIR, "sales.csv")
SUPPLIERS_FILE = os.path.join(DATA_DIR, "suppliers.csv")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.csv")

LOW_STOCK_LIMIT = 10
GST = 18
EXPIRY_ALERT_DAYS = 90