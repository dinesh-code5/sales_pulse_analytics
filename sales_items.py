import psycopg2
from Database import get_conn

class SaleItem:
    @staticmethod
    def create_table():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS sale_items (
                        id SERIAL PRIMARY KEY,
                        sale_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        price DECIMAL(10, 2) NOT NULL
                    )''')
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def add_item(sale_id, product_id, quantity, price):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('''INSERT INTO sale_items (sale_id, product_id, quantity, price)
                       VALUES (%s, %s, %s, %s)''',
                    (sale_id, product_id, quantity, price))
        conn.commit()
        cur.close()
        conn.close()
        print("Item added to sale")

    @staticmethod
    def get_items_by_sale(sale_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM sale_items WHERE sale_id = %s', (sale_id,))
        items = cur.fetchall()
        cur.close()
        conn.close()
        return items

    @staticmethod
    def view_sale_items(sale_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM sale_items WHERE sale_id = %s', (sale_id,))
        items = cur.fetchall()
        cur.close()
        conn.close()

        total_amount = 0
        for item in items:
            print(item)
            total_amount += item[3] * item[4]

        print("Total Amount for Sale ID", sale_id, ":", total_amount)
        return total_amount

    @staticmethod
    def sale_item_menu():
        while True:
            print("\n1. Create Table\n2. Add Item to Sale\n3. View Sale Items\n0. Exit")
            choice = input("Enter choice: ")

            if choice == '1':
                SaleItem.create_table()
                print("Table created")
            elif choice == '2':
                sale_id = int(input("Enter sale id: "))
                product_id = int(input("Enter product id: "))
                quantity = int(input("Enter quantity: "))
                price = float(input("Enter price: "))
                SaleItem.add_item(sale_id, product_id, quantity, price)
            elif choice == '3':
                sale_id = int(input("Enter sale id: "))
                total_amount = SaleItem.view_sale_items(sale_id)
            elif choice == '0':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == '__main__':
    SaleItem.sale_item_menu()
