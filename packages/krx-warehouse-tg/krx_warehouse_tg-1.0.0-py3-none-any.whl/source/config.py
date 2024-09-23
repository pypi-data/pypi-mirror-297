API_TOKEN = ""

MAIN_SOURCE = r"C:\Users\wkramx\krx_warehouse_bot"
DB_SOURCE = f"{MAIN_SOURCE}/database.db"

ADMIN_ID = 0

status_mapping = {'on_wh': 'in stock', 'pending_confirmation': 'pending confirmation',
                  'sent': 'sent', 'archived': 'archived', 'delivered': 'delivered'}

email_pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
address_pattern = r"^\d{6},?\s*(?:г\.\s*)?[\w\s-]+,?\s*(?:ул\.\s*)?[\w\s-]+,?\s*\d{1,5}(?:\s*,?\s*\d{1,5})?\s*\.?"

box_names = ["mini", "small", "large", "extra large", "y-08", "y-01"]

temp_data = {}

boxes_measurements = {
    "MINI": 23 * 17 * 13 / 5000,
    "SMALL": 36 * 26 * 14 / 5000,
    "LARGE": 40 * 29 * 16 / 5000,
    "EXTRA LARGE": 45 * 34 * 18 / 5000,
    "Y-08": 37 * 29 * 28 / 5000,
    "Y-01": 38 * 48 * 30 / 5000,
}