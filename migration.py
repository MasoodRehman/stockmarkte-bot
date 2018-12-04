import sqlite3

conn = sqlite3.connect('database.db')
print "Opened database successfully";

conn.execute("""
    CREATE TABLE companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker_symbol TEXT, 
        business TEXT, 
        listing_bourse TEXT, 
        company_name TEXT, 
        company_url TEXT, 
        company_street_address TEXT, 
        country TEXT, 
        company_description TEXT, 
        company_phone_number TEXT, 
        company_website TEXT, 
        company_email TEXT, 
        financial_summary TEXT, 
        business_registration TEXT, 
        auditing_company TEXT, 
        crawled_at TEXT
    )
""")

print "Table created successfully";
conn.close()
