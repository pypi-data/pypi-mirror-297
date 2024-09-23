import sqlite3
from config import *

con = sqlite3.connect(database=DB_SOURCE,
                      check_same_thread=False)
cur = con.cursor()

def is_user(tID):
    try:
        cur.execute(f"SELECT tID FROM users WHERE tID ={tID}")
        print(f"SELECT tID FROM users WHERE tID ={tID}")
        data = cur.fetchall()
    except Exception:
        return False
    return len(data) == 1

def reg_user(tID, firstname, lastname, email):
    try:
        cur.execute(f"INSERT INTO users (tID, lastname, firstname, email)"
                    f"VALUES ({tID}, '{lastname}', '{firstname}', '{email}')")
        con.commit()
    except Exception:
        return False
    return True

def get_user(tID):
    try:
        cur.execute(f"SELECT * FROM users WHERE tID = {tID}")
        data = cur.fetchone()
    except Exception:
        return False
    return data

def delete_user(tID):
    try:
        cur.execute(f"DELETE FROM users WHERE tID = {tID}")
        cur.execute(f"DELETE FROM orders WHERE tID = {tID}")
        cur.execute(f"DELETE FROM addresses WHERE tID = {tID}")
        con.commit()
    except Exception:
        return False
    return True

def create_goods(id, tID, name, price):
    try:
        cur.execute(f"INSERT INTO orders (id, tID, name, price)"
                    f"VALUES ('{id}', {tID}, '{name}', {price})")
        con.commit()
    except Exception:
        return False
    return True

def get_order(tID, id):
    try:
        cur.execute(f"SELECT * FROM orders WHERE id = {id} AND tID = {tID}")
        data = cur.fetchall()
    except Exception:
        return False
    return data

def get_status(tID, id):
    try:
        cur.execute(f"SELECT status FROM orders WHERE id = {id} AND tID = {tID}")
        data = cur.fetchone()
    except Exception:
        return False
    data = status_mapping.get(data[0], data[0])
    return data

def change_order_status(id, status):
    try:
        cur.execute(f"UPDATE orders SET status = '{status}' WHERE id = {id}")
        con.commit()
    except Exception:
        return False
    return True

def get_all_goods(tID):
    try:
        cur.execute(f"SELECT id, name, price, status FROM orders WHERE tID = {tID} AND status = 'pending_confirmation'")
        data = cur.fetchall()
    except Exception:
        return False
    orders = "Products:\n\n"
    for row in data:
        id, name, price, status = row
        status_translation = status_mapping.get(status, status)
        orders += f"ID: {id}\nName: {name}\nPrice: {price} $\nStatus: {status_translation}\n\n"
    return orders

def get_all_orders(tID):
    try:
        cur.execute(f"SELECT id, name, price, status FROM orders WHERE tID = {tID} AND status != 'pending_confirmation'")
        data = cur.fetchall()
    except Exception:
        return False
    orders = "Orders:\n\n"
    for row in data:
        id, name, price, status = row
        status_translation = status_mapping.get(status, status)
        orders += f"ID: {id}\nName: {name}\nPrice: {price} $\nStatus: {status_translation}\n\n"
    return orders

def reg_address(tID, address):
    try:
        cur.execute(f"INSERT INTO addresses (tID, address)"
                    f"VALUES ({tID}, '{address}')")
        con.commit()
    except Exception:
        return False
    return True

def change_address(tID, address, old_address):
    try:
        cur.execute(f"UPDATE addresses SET address = '{address}' WHERE tID = {tID} AND address = '{old_address}'")
        con.commit()
    except Exception:
        return False
    return True

def get_addresses(tID):
    try:
        cur.execute(f"SELECT address FROM addresses WHERE tID = {tID}")
        data = cur.fetchall()
    except Exception:
        return False
    return data

def delete_address(address, tID):
    try:
        cur.execute(f"DELETE FROM addresses WHERE address = '{address}' AND tID = {tID}")
        con.commit()
    except Exception:
        return False
    return True

def change_name(firstname, lastname, tID):
    try:
        cur.execute(f"UPDATE users SET lastname = '{lastname}', firstname = '{firstname}' WHERE tID = {tID}")
        con.commit()
    except Exception as e:
        return False
    return True

def change_email(email, tID):
    try:
        cur.execute(f"UPDATE users SET email = '{email}' WHERE tID = {tID}")
        con.commit()
    except Exception:
        return False
    return True