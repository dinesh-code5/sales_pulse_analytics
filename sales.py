import psycopg2
from Database import get_conn

class Sale:
    @staticmethod
    def create_table():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS sales (
                        id SERIAL PRIMARY KEY,
                        customer_id INTEGER NOT NULL,
                        date DATE NOT NULL,
                        total_amount DECIMAL(10, 2) NOT NULL
                    )''')
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def insert_sale(customer_id, date, total_amount):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('''INSERT INTO sales (customer_id, date, total_amount)
                       VALUES (%s, %s, %s)''',
                    (customer_id, date, total_amount))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def view_sales():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM sales')
        sales = cur.fetchall()
        for sale in sales:
            print(sale)
        cur.close()
        conn.close()

    @staticmethod
    def view_sale_by_id(sale_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM sales WHERE id = %s', (sale_id,))
        sale = cur.fetchone()
        print(sale)
        cur.close()
        conn.close()

    @staticmethod
    def generate_bill(sale_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM sale_items WHERE sale_id = %s', (sale_id,))
        sale_items = cur.fetchall()

        print("Bill for Sale ID:", sale_id)
        total_amount = 0

        for item in sale_items:
            print("Product ID:", item[2], "Quantity:", item[3], "Price:", item[4])
            total_amount += item[3] * item[4]

        print("Total Amount:", total_amount)
        cur.close()
        conn.close()
        return total_amount

    @staticmethod
    def add_sale_items(sale_id, product_id, quantity, price):
        from sales_items import SaleItem
        SaleItem.add_item(sale_id, product_id, quantity, price)

    @staticmethod
    def update_inventory(product_id, quantity_sold):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('''
            UPDATE products
            SET quantity = quantity - %s
            WHERE id = %s
        ''', (quantity_sold, product_id))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_total_sales_by_date(start_date, end_date):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('''SELECT SUM(total_amount) FROM sales
                       WHERE date BETWEEN %s AND %s''',
                    (start_date, end_date))
        total_sales = cur.fetchone()[0]
        cur.close()
        conn.close()
        return total_sales

    @staticmethod
    def get_top_selling_products():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('''SELECT product_id, SUM(quantity)
                       FROM sale_items
                       GROUP BY product_id
                       ORDER BY SUM(quantity) DESC
                       LIMIT 5''')
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    @staticmethod
    def get_sales_by_customer(customer_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM sales WHERE customer_id = %s', (customer_id,))
        sales = cur.fetchall()
        for sale in sales:
            print(sale)
        cur.close()
        conn.close()
        return sales

    @staticmethod
    def sale_menu():
        while True:
            print("\n1. Create Table\n2. Insert Sale\n3. View Sales")
            print("4. View Sale by ID\n5. Add Sale Items\n6. Update Inventory")
            print("7. Generate Bill\n8. Get Total Sales by Date\n9. Get Top Selling Products")
            print("10. Get Sales by Customer\n0. Exit")

            choice = input("Enter choice: ")

            if choice == '1':
                Sale.create_table()
                print("Table created")
            elif choice == '2':
                customer_id = int(input("Enter customer id: "))
                date = input("Enter date (YYYY-MM-DD): ")
                total_amount = float(input("Enter total amount: "))
                Sale.insert_sale(customer_id, date, total_amount)
            elif choice == '3':
                Sale.view_sales()
            elif choice == '4':
                sale_id = int(input("Enter sale id: "))
                Sale.view_sale_by_id(sale_id)
            elif choice == '5':
                sale_id = int(input("Enter sale id: "))
                product_id = int(input("Enter product id: "))
                quantity = int(input("Enter quantity: "))
                price = float(input("Enter price: "))
                Sale.add_sale_items(sale_id, product_id, quantity, price)
            elif choice == '6':
                product_id = int(input("Enter product id: "))
                quantity_sold = int(input("Enter quantity sold: "))
                Sale.update_inventory(product_id, quantity_sold)
            elif choice == '7':
                sale_id = int(input("Enter sale id: "))
                total_amount = Sale.generate_bill(sale_id)
            elif choice == '8':
                start = input("Start date: ")
                end = input("End date: ")
                print(Sale.get_total_sales_by_date(start, end))
            elif choice == '9':
                for p in Sale.get_top_selling_products():
                    print(p)
            elif choice == '10':
                cid = int(input("Enter customer id: "))
                sales = Sale.get_sales_by_customer(cid)
                for s in sales:
                    print("Bill:", Sale.generate_bill(s[0]))
            elif choice == '0':
                break
            else:
                print("Invalid choice")

if __name__ == '__main__':
    Sale.sale_menu()
