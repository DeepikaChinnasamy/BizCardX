import psycopg2

# Function to connect to the PostgreSQL database
def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        database="bizcardx_db",
        user="postgres",
        password="Deepika1630"
    )
    return conn

# Function to create the necessary table in the database
def create_table(c, conn):
    c.execute('''
    CREATE TABLE IF NOT EXISTS business_cards (
        id SERIAL PRIMARY KEY,
        company_name TEXT,
        card_holder_name TEXT,
        designation TEXT,
        mobile_number VARCHAR(50),
        email_address TEXT,
        website_url TEXT,
        area TEXT,
        city TEXT,
        state TEXT,
        pin_code VARCHAR(10),
        image BYTEA,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    conn.commit()


def insert_or_update_data(c, conn, data, images):
    """
    Inserts or updates extracted data into the database.
    
    Args:
        c (cursor): The database cursor.
        conn (connection): The database connection.
        data (dict): The extracted data.
        image (binary): The binary image data.
    
    Returns:
        str: Status message indicating whether the data was inserted or updated.
    """
    # Check if a record with the same company name already exists
    c.execute('''SELECT id FROM business_cards WHERE company_name = %s''', (data['company_name'],))
    record = c.fetchone()
    
    if record:
        # If record exists, update the existing record
        c.execute('''UPDATE business_cards SET 
                    card_holder_name = %s, 
                    designation = %s, 
                    mobile_number = %s, 
                    email_address = %s, 
                    website_url = %s, 
                    area = %s, 
                    city = %s, 
                    state = %s, 
                    pin_code = %s, 
                    image = %s
                    WHERE company_name = %s;''',
                    (data['card_holder_name'], data['designation'], data['mobile_number'], 
                     data['email_address'], data['website_url'], data['area'], data['city'], 
                     data['state'], data['pin_code'], psycopg2.Binary(images), data['company_name']))
        status = "Record updated successfully."
    else:
        # If record does not exist, insert a new record
        c.execute('''INSERT INTO business_cards 
                    (company_name, card_holder_name, designation, mobile_number, 
                    email_address, website_url, area, city, state, pin_code, image) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);''', 
                    (data['company_name'], data['card_holder_name'], data['designation'], 
                     data['mobile_number'], data['email_address'], data['website_url'], 
                     data['area'], data['city'], data['state'], data['pin_code'], 
                     psycopg2.Binary(images)))
        status = "Record inserted successfully."
    
    conn.commit()
    return status