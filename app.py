from flask import Flask, jsonify, request, send_from_directory, g
from flask_cors import CORS
from Database import get_conn
from sales import Sale
from customers import Customer
from products import Product
from sales_items import SaleItem

app = Flask(__name__, static_folder='.')
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# ── Per-request DB connection ─────────────────────────────────────────────────
def get_db():
    """Open one fresh connection per request, reuse within the same request."""
    if 'db' not in g:
        g.db = get_conn()
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    """Automatically close the connection when the request finishes."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# ── SERVE FRONTEND ────────────────────────────────────────────────────────────
@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

# ── SALES ─────────────────────────────────────────────────────────────────────
@app.route('/api/sales', methods=['GET'])
def get_sales():
    customer_id = request.args.get('customer_id')
    cur = get_db().cursor()
    if customer_id:
        cur.execute("SELECT * FROM sales WHERE customer_id = %s", (customer_id,))
    else:
        cur.execute("SELECT * FROM sales")
    data = cur.fetchall()
    cur.close()
    return jsonify([{"id": s[0], "customer_id": s[1], "date": str(s[2]), "total_amount": float(s[3])} for s in data])

@app.route('/api/sales', methods=['POST'])
def add_sale():
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO sales (customer_id, date, total_amount) VALUES (%s, %s, %s)",
        (data['customer_id'], data['date'], data['total_amount'])
    )
    db.commit()
    cur.close()
    return jsonify({"message": "Sale added successfully"})

@app.route('/api/sales/<int:sale_id>/bill', methods=['GET'])
def get_bill(sale_id):
    cur = get_db().cursor()
    cur.execute('SELECT * FROM sale_items WHERE sale_id = %s', (sale_id,))
    items = cur.fetchall()
    cur.close()
    return jsonify([{"product_id": i[2], "quantity": i[3], "price": float(i[4])} for i in items])

# ── CUSTOMERS ─────────────────────────────────────────────────────────────────
@app.route('/api/customers', methods=['GET'])
def get_customers():
    cur = get_db().cursor()
    cur.execute('SELECT * FROM customers')
    data = cur.fetchall()
    cur.close()
    return jsonify([{"id": c[0], "name": c[1], "contact": c[2]} for c in data])

@app.route('/api/customers/<int:id>', methods=['GET'])
def get_customer_by_id(id):
    cur = get_db().cursor()
    cur.execute('SELECT * FROM customers WHERE id = %s', (id,))
    c = cur.fetchone()
    cur.close()
    if c:
        return jsonify({"id": c[0], "name": c[1], "contact": c[2]})
    return jsonify({"error": "Customer not found"}), 404

@app.route('/api/customers/search', methods=['GET'])
def search_customers():
    name = request.args.get('name', '')
    cur = get_db().cursor()
    cur.execute('SELECT * FROM customers WHERE name ILIKE %s', ('%' + name + '%',))
    data = cur.fetchall()
    cur.close()
    return jsonify([{"id": c[0], "name": c[1], "contact": c[2]} for c in data])

@app.route('/api/customers', methods=['POST'])
def add_customer():
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO customers (name, contact) VALUES (%s, %s)",
        (data['name'], data['contact'])
    )
    db.commit()
    cur.close()
    return jsonify({"message": "Customer added"})

# ── PRODUCTS ──────────────────────────────────────────────────────────────────
@app.route('/api/products', methods=['GET'])
def get_products():
    cur = get_db().cursor()
    cur.execute('SELECT * FROM products')
    data = cur.fetchall()
    cur.close()
    return jsonify([{"id": p[0], "name": p[1], "description": p[2], "price": float(p[3]), "quantity": p[4]} for p in data])

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO products (name, description, price, quantity) VALUES (%s, %s, %s, %s)",
        (data['name'], data['description'], data['price'], data['quantity'])
    )
    db.commit()
    cur.close()
    return jsonify({"message": "Product added"})

# ── SALE ITEMS ────────────────────────────────────────────────────────────────
@app.route('/api/sale_items', methods=['POST'])
def add_sale_item():
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
        (data['sale_id'], data['product_id'], data['quantity'], data['price'])
    )
    cur.execute(
        "UPDATE products SET quantity = quantity - %s WHERE id = %s",
        (data['quantity'], data['product_id'])
    )
    db.commit()
    cur.close()
    return jsonify({"message": "Item added to sale"})

# ── ANALYTICS ─────────────────────────────────────────────────────────────────
@app.route('/api/analytics/revenue', methods=['GET'])
def get_revenue():
    start = request.args.get('start')
    end = request.args.get('end')
    cur = get_db().cursor()
    cur.execute(
        "SELECT SUM(total_amount) FROM sales WHERE date BETWEEN %s AND %s",
        (start, end)
    )
    total = cur.fetchone()[0]
    cur.close()
    return jsonify({"total_sales": float(total) if total else 0})

# ── RUN ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
