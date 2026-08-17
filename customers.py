import psycopg2
from Database import get_conn

class Customer:
    @staticmethod
    def create_table():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            contact VARCHAR(100) NOT NULL
        )''')
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def insert_customer(name, contact):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('''INSERT INTO customers (name, contact)
                       VALUES (%s, %s)''',
                    (name, contact))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def update_customer(customer_id, name=None, contact=None):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM customers WHERE id = %s', (customer_id,))
        customer = cur.fetchone()
        if not customer:
            print("Customer not found")
            cur.close()
            conn.close()
            return

        update_fields = []
        params = []

        if name:
            update_fields.append("name = %s")
            params.append(name)
        if contact:
            update_fields.append("contact = %s")
            params.append(contact)

        if update_fields:
            params.append(customer_id)
            update_query = f"UPDATE customers SET {', '.join(update_fields)} WHERE id = %s"
            cur.execute(update_query, tuple(params))
            conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete_customer(customer_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('DELETE FROM customers WHERE id = %s', (customer_id,))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_all_customers():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM customers')
        customers = cur.fetchall()
        cur.close()
        conn.close()
        return customers

    @staticmethod
    def view_customers():
        customers = Customer.get_all_customers()
        for customer in customers:
            print(customer)

    @staticmethod
    def view_customer_by_id(customer_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM customers WHERE id = %s', (customer_id,))
        customer = cur.fetchone()
        cur.close()
        conn.close()
        if customer:
            print(customer)
        else:
            print("Customer not found")

    @staticmethod
    def get_sales_by_customer(customer_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('''SELECT s.id, s.date, s.total_amount FROM sales s
                       JOIN customers c ON s.customer_id = c.id
                       WHERE c.id = %s''', (customer_id,))
        sales = cur.fetchall()
        for sale in sales:
            print(sale)
        cur.close()
        conn.close()

    @staticmethod
    def search_customer(name):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM customers WHERE name ILIKE %s', ('%' + name + '%',))
        customers = cur.fetchall()
        for customer in customers:
            print(customer)
        cur.close()
        conn.close()

    @staticmethod
    def customer_menu():
        while True:
            print("\n1. Create Table\n2. Insert Customer\n3. Update Customer")
            print("4. Delete Customer\n5. View Customers\n6. View Customer by ID")
            print("7. Get Sales by Customer\n8. Search Customer\n0. Exit")
            choice = input("Enter choice: ")

            if choice == '1':
                Customer.create_table()
                print("Table created")
            elif choice == '2':
                name = input("Enter customer name: ")
                contact = input("Enter customer contact: ")
                Customer.insert_customer(name, contact)
                print("Customer inserted")
            elif choice == '3':
                customer_id = int(input("Enter customer id: "))
                name = input("Enter customer name (leave blank to keep current): ")
                contact = input("Enter customer contact (leave blank to keep current): ")
                Customer.update_customer(customer_id, name, contact)
                print("Customer updated")
            elif choice == '4':
                customer_id = int(input("Enter customer id: "))
                Customer.delete_customer(customer_id)
                print("Customer deleted")
            elif choice == '5':
                Customer.view_customers()
            elif choice == '6':
                customer_id = int(input("Enter customer id: "))
                Customer.view_customer_by_id(customer_id)
            elif choice == '7':
                customer_id = int(input("Enter customer id: "))
                Customer.get_sales_by_customer(customer_id)
            elif choice == '8':
                name = input("Enter customer name: ")
                Customer.search_customer(name)
            elif choice == '0':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == '__main__':
    Customer.customer_menu()
