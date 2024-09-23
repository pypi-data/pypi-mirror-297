from telebot import types

btn_goods = types.KeyboardButton("👟 Products")
btn_deliveries = types.KeyboardButton("📦 Ship")
btn_calculator = types.KeyboardButton("➕ Calculator")
btn_addresses = types.KeyboardButton("🏠 Addresses")
btn_profile = types.KeyboardButton("👤 Profile")
btn_help = types.KeyboardButton("❔ Help")

main_menu = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                      resize_keyboard=True,
                                      row_width=2)
main_menu.row(btn_goods).row(btn_deliveries).row(btn_addresses, btn_calculator).row(btn_profile, btn_help)


admin_menu = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                      resize_keyboard=True,
                                      row_width=2)
admin_change_status = types.KeyboardButton("Change order status")
admin_check_user = types.KeyboardButton("User data")
admin_check_order = types.KeyboardButton("Order data")
admin_all_orders = types.KeyboardButton("All orders")
admin_all_goods = types.KeyboardButton("All products")
admin_menu.row(admin_change_status).row(admin_check_user,admin_check_order).row(admin_all_orders, admin_all_goods)
