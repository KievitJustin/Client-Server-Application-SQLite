import sqlite3
import datetime

CREATE_ITEMS_TABLE = ''' CREATE TABLE IF NOT EXISTS items (
    name TEXT PRIMARY KEY,
    manufacturer TEXT,
    category TEXT,
    price TEXT,
    deliveryperson TEXT,
    deliverydate REAL
    );'''

CREATE_DELIVERIES_TABLE = ''' CREATE TABLE IF NOT EXISTS deliveries (
    items_name TEXT,
    deliveryperson TEXT,
    personnumber TEXT,
    FOREIGN KEY (items_name) REFERENCES items(name)
    );'''


CREATE_MANU_TABLE = ''' CREATE TABLE IF NOT EXISTS manufacturers (
    items_manufacturer TEXT,
    manufactureradd TEXT,
    manufacturerdeliverydays REAL,
    FOREIGN KEY (items_manufacturer) REFERENCES items(manufacturer)
    );'''


INSERT_ITEM = "INSERT INTO items (name, manufacturer, category, price, deliveryperson, deliverydate) VALUES (?,?,?,?,?,?);"
INSERT_MANU = "INSERT INTO manufacturers (items_manufacturer, manufacturerdeliverydays) VALUES (?,?);"
INSERT_DELIVERY = "INSERT INTO deliveries (items_name, deliveryperson) VALUES (?,?);"

REMOVE_ITEM = "DELETE FROM items WHERE name = ?;"
SELECT_ITEMS = "SELECT * FROM items;"
VIEW_OUTOFSTOCK_ITEMS = "SELECT * FROM items WHERE deliverydate > ?;"
VIEW_DELIVERED_ITEMS = "SELECT * FROM items WHERE deliverydate < ?;"
CHANGE_DELIVERY_PERSON = "UPDATE deliveries SET deliveryperson = ? WHERE items_name = ?;" #, personnumber = ?
NAME_SEARCH = "SELECT * FROM items WHERE name = ?;"
CATEGORY_SEARCH = "SELECT * FROM items WHERE category = ?;"

# VIEW_DELIVERY_INFO = "SELECT items.name, deliveries.deliveryperson FROM items INNER JOIN deliveries ON items.itemname=deliveries.itemname"

connection = sqlite3.connect('justinstore.db')

def create_tables():
    with connection:
        connection.execute(CREATE_ITEMS_TABLE)
        connection.execute(CREATE_DELIVERIES_TABLE)
        connection.execute(CREATE_MANU_TABLE)


def add_item(name, manufacturer, category, price, deliveryperson, delivery_timestamp):
    with connection:
        connection.execute(INSERT_ITEM, (name, manufacturer, category, price, deliveryperson, delivery_timestamp))

def add_manu(items_manufacturer, manufacturerdeliverydays):
    with connection:
        connection.execute(INSERT_MANU, (items_manufacturer, manufacturerdeliverydays))

def add_delivery(items_name, deliveryperson):
    with connection:
        connection.execute(INSERT_DELIVERY, (items_name, deliveryperson,))
#
def remove_item(name):
    with connection:
        connection.execute(REMOVE_ITEM, (name,))

def view_items(upcoming=False):
    cursor = connection.cursor()
    if not upcoming:
        cursor.execute(SELECT_ITEMS)
    else:
        today_timestamp = datetime.datetime.today().timestamp()
        cursor.execute(VIEW_OUTOFSTOCK_ITEMS, (today_timestamp,))
    return cursor.fetchall()

def view_in_stock_items():
    cursor = connection.cursor()
    cursor.execute(VIEW_DELIVERED_ITEMS)
    return cursor.fetchall()

def update_delivery_person(items_name, deliveryperson, personnumber):
    with connection:
        connection.execute(CHANGE_DELIVERY_PERSON, (deliveryperson, items_name)) #personnumber

def name_search(name):
    cursor = connection.cursor()
    cursor.execute(NAME_SEARCH, (name,))
    results = cursor.fetchall()
    print(results)

def category_search(category):
    cursor = connection.cursor()
    cursor.execute(CATEGORY_SEARCH, (category,))
    results = cursor.fetchall()
    print(results)


# def view_delivery_info():
#     cursor = connection.cursor()
#     cursor.execute(VIEW_DELIVERY_INFO)
#     return cursor.fetchone()