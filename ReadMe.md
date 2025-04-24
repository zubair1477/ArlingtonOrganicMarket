# Arlington Organic Market 

This project is a **web-based inventory management system** for the Arlington Organic Market. It allows store administrators to add, update, view, and delete product and vendor data. The application is built using **Flask** for the backend and **HTML/CSS/JavaScript** for the frontend, with **PostgreSQL** as the database.

---

##  Project Structure

```
arlington-organic-market/
│
├── app.py                 # Flask backend with RESTful API endpoints
├── templates/
│   └── index.html         # Frontend interface for inventory management
├── static/                # Place for static assets like CSS/JS if added
├── README.md              # Project overview and setup instructions
└── requirements.txt       # Python dependencies
```

---

## Features

### Inventory Management
- Add new products with vendor and store stock data
- Update item prices
- Remove items and auto-clean vendor if no more products are associated

### Store Lookup
- Search available products in a specific store by ID
- Displays item name, price, and stock count

### Database Operations
- Manages four main tables: `vendor`, `item`, `store_item`, `vendor_item`
- Handles cascading deletions and insert conflicts gracefully

---

## Tech Stack

| Component      | Technology         |
|----------------|--------------------|
| Backend        | Python (Flask)     |
| Frontend       | HTML, CSS, JS      |
| Database       | PostgreSQL         |
| ORM/Driver     | psycopg2           |

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/arlington-organic-market.git
cd arlington-organic-market
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install Flask psycopg2
```

### 4. Configure PostgreSQL
Ensure you have a PostgreSQL database named `ArlingtonOrganicMarket` and the following tables:

```sql
CREATE TABLE vendor (
    vId INT PRIMARY KEY,
    Vname TEXT,
    Street TEXT,
    City TEXT,
    StateAb TEXT,
    ZipCode TEXT
);

CREATE TABLE item (
    iId INT PRIMARY KEY,
    Iname TEXT,
    Sprice DECIMAL,
    Category TEXT
);

CREATE TABLE vendor_item (
    vId INT REFERENCES vendor(vId),
    iId INT REFERENCES item(iId),
    PRIMARY KEY (vId, iId)
);

CREATE TABLE store_item (
    sId INT,
    iId INT REFERENCES item(iId),
    Scount INT,
    PRIMARY KEY (sId, iId)
);
```

Update your credentials in `app.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'dbname': 'ArlingtonOrganicMarket',
    'port': 5432
}
```

### 5. Run the App
```bash
python app.py
```

Then open: [http://localhost:5000](http://localhost:5000)

---

## Sample API Endpoints

- `POST /products` – Add a new item and its associations  
- `GET /products?store_id=<id>` – View items for a given store  
- `PUT /products/<item_id>` – Update item price  
- `DELETE /products/<item_id>` – Delete an item and related records  

---

## Contributions

Feel free to fork the repo and submit pull requests.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

Thanks to the Professor and TA for guiding us through this project.

