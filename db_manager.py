import psycopg2
from psycopg2.extras import RealDictCursor
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="restaurant_db",
        user="postgres",
        password="password"
    )
def get_all_menu():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from menu order by id asc")
    data = cur.fetchall()
    conn.close()
    return data
def add_menu_item(name, price, cost, image_path):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "insert into menu (name, price, cost, image_path) values (%s, %s, %s, %s)",
        (name, price, cost, image_path)
    )
    conn.commit()
    conn.close()
def update_table_status(table_id, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("update tables set status = %s where id = %s", (status, table_id))
    conn.commit()
    conn.close()
def save_order_to_db(table_id, total_revenue, profit):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "insert into orders (table_id, total_revenue, profit) values (%s, %s, %s)",
        (table_id, total_revenue, profit)
    )
    order_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return order_id