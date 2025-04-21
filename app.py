from flask import Flask, request, jsonify, render_template
import psycopg2
import psycopg2.extras

#initialize Flask application
app = Flask(__name__, template_folder='templates') #templates folder has front end code

#PostgreSQL Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'zubairrashaad',
    'password': '',
    'dbname': 'ArlingtonOrganicMarket',
    'port': 5432
}

#establishes database connection
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

#Home Route

@app.route('/')
def index():
    return render_template('index.html')

#Create Product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    print("Received data:", data)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
        #add vendor
            cursor.execute("INSERT INTO vendor(vId, Vname, Street, City, StateAb, ZipCode) VALUES (%s,%s,%s,%s,%s,%s)",
                    (data['vId'],data['Vname'],data['Street'],data['City'],data['StateAb'],data['ZipCode']))
            print("Vendor Added.")

        except Exception as e:
            print("Error inserting vendor:", e)
        #insert item
        try:
            cursor.execute("INSERT INTO item(iId, Iname, Sprice, Category) VALUES (%s,%s,%s,%s)",
                   (data['iId'],data['Iname'],data['Sprice'],data['Category']))
            print("Item added.")
        except Exception as e:
            print("Error inserting item:", e)

        #link vendor to item
        try:
            cursor.execute("INSERT INTO vendor_item(vId, iId) VALUES (%s,%s)",
                   (data['vId'],data['iId']))
            print("Vendor-item link added.")
        except Exception as e:
            print("Error linking vendor to item:", e)

        #update the store inventory
        try:
            cursor.execute("INSERT INTO store_item(sId, iId, Scount) VALUES (%s,%s,%s)",
                       (data['storeId'],data['iId_store'],data['Scount']))

            print("Inventory added.")
        except Exception as e:
            print("Error inserting inventory:", e)

        conn.commit()
        return jsonify({'message': 'Product added successfully'}),201

    except Exception as e:
        conn.rollback()
        print("Fatal error", e)
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/products',methods=['GET'])
def get_products():
    store_id = request.args.get('store_id',type=int)
    if not store_id:
        return jsonify({'error': 'missing store id'}), 400
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(""" 
        SELECT i.Iname AS name, i.Sprice AS price, si.Scount AS stock
        FROM store_item si
        JOIN item i ON si.iId = i.iId
        WHERE si.sid = %s
                   """, (store_id,))
    products = cursor.fetchall()
    conn.close()
    return jsonify(products)

@app.route('/products/<int:id>', methods=['PUT'])
def update_price(id):

    data = request.get_json()
    new_price = data.get('new_price')

    if new_price is None:
        return jsonify({'message': 'Missing new price'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE item SET Sprice = %s WHERE iId = %s",(new_price,id))

        if(cursor.rowcount == 0):
            return jsonify({'message': 'Item not found or price already updated'}), 404

        conn.commit()
        return jsonify({'success': True,'message': f'Price updated to ${new_price} for item ID {id}'})
    except Exception as e:
        conn.rollback()
        print("Error updating price:", e)
        return jsonify({'message': 'Server error'}), 500
    finally:
        conn.close()

@app.route('/products/<int:id>',methods=['DELETE'])
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()


        cursor.execute("SELECT vId FROM vendor_item WHERE iId = %s", (id,))
        vendor_result = cursor.fetchone()

        if not vendor_result:
            return jsonify({'success': False, 'message': 'Item not found or not linked to a vendor.'}), 404

        vendor_id = vendor_result[0]


        cursor.execute("DELETE FROM store_item WHERE iId = %s", (id,))
        print(f"Deleted item {id} from store_item")

        cursor.execute("DELETE FROM vendor_item WHERE iId = %s", (id,))
        print(f"Deleted item {id} from vendor_item")

        cursor.execute("DELETE FROM item WHERE iId = %s", (id,))
        print(f"Deleted item {id} from item table")

        cursor.execute("SELECT COUNT(*) FROM vendor_item WHERE vId = %s", (vendor_id,))
        count = cursor.fetchone()[0]
        print(f"Vendor {vendor_id} now supplies {count} items")

        if count == 0:
            cursor.execute("DELETE FROM vendor WHERE vId = %s", (vendor_id,))
            print(f"Vendor {vendor_id} deleted — they had no other items.")

        conn.commit()
        return jsonify({'success': True, 'message': f'Item {id} and related data deleted successfully.'})

    except Exception as e:
        conn.rollback()
        print("Error deleting item:", e)
        return jsonify({'success': False, 'message': 'Error occurred during deletion.'}), 500

    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)