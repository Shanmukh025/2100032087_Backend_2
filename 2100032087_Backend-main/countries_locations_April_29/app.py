from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS locations (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        street_address TEXT,
        postal_code TEXT,
        city TEXT NOT NULL,
        state_province TEXT,
        country_id INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        country_id TEXT NOT NULL,
        country_name TEXT NOT NULL,
        region_id INTEGER
    )
''')

conn.commit()

@app.route('/')
def home():
    with app.app_context():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM locations")
        locations = cursor.fetchall()

        cursor.execute("SELECT * FROM countries")
        countries = cursor.fetchall()

        conn.commit()
        conn.close()

    return render_template('index.html', locations=locations, countries=countries)

@app.route('/join', methods=['POST'])
def query_country_using_join():
    country_name = request.form['country_name']
    with app.app_context():
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT locations.*, countries.country_name, countries.region_id 
                FROM locations 
                JOIN countries ON locations.country_id = countries.country_id 
                WHERE countries.country_name = ?
            ''', (country_name,))
            result = cursor.fetchall()
    return render_template('result.html', result=result)

@app.route('/not_join', methods=['POST'])
def query_country_not_using_join():
    country_name = request.form['country_name']
    with app.app_context():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM countries WHERE country_name = ?", (country_name,))
        result = cursor.fetchall()
    return render_template('result.html', result=result)

@app.route('/add_location', methods=['POST'])
def add_location():
    if request.method == 'POST':
        country_id = request.form['country_id']
        country_name = request.form['country_name']
        region_id = request.form['region_id']
        street_address = request.form['street_address']
        city = request.form['city']
        state_province = request.form['state_province']
        postal_code = request.form['postal_code']

        with app.app_context():
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO locations (street_address, postal_code, city, state_province, country_id)
                VALUES (?, ?, ?, ?, ?)
            """, (street_address, postal_code, city, state_province, 1))

            country_id = request.form['country_id'].upper()
            country_name = request.form['country_name']
            region_id = request.form['region_id']
            
            cursor.execute("INSERT INTO countries (country_id, country_name, region_id) VALUES (?, ?, ?)",
                           (country_id, country_name, region_id))
            conn.commit()
            conn.close()

        return f"Location '{street_address}' added successfully!" 

    return f"Invalid request method: {request.method}" 


if __name__ == '__main__':
    app.run(debug=True)
