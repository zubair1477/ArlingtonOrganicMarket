from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__, template_folder='templates') #define the templates folder


DB_CONFIG = {
    'host': '',
    'user': '',
    'password': '',
    'database': '',
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

#Home Route

@app.route('/')
def index():
    return render_template('index.html')

#Create Product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    conn = get_db_connection()
    cursor = conn.curson()
    cursor.execute("INSERT INTO products(name, price, quantity) VALUES (%s,%s,%s)",
                   (data['name'],data['price'],data['quantity']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product added successfully'}),201



#Read Products
@app.route('/prodcuts',methods=['GET'])
def get_product():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return jsonify(products)


#update product
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name=%s, price=%s, quanity=%s WHERE id=%s",
                   (data['name'], data['price'], data['quantity'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)