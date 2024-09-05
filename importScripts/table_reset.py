"""
This file contains a script to erase data from a selected table.
"""
import argparse
import psycopg2

# Parse the table name from command-line arguments
parser = argparse.ArgumentParser(description="Truncate a specific table in the database.")
parser.add_argument('table_name', type=str, help='The name of the table to truncate.')
args = parser.parse_args()

# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres.seqkcnapvgkwqbqipqqs",
                        password="IT Web Server12", host="aws-0-ap-southeast-2.pooler.supabase.com", port=6543)
cur = conn.cursor()

# Build and execute the SQL query with the specified table name
truncate_query = f"TRUNCATE TABLE {args.table_name} CASCADE;"
cur.execute(truncate_query)

# Commit the transaction
conn.commit()

# Close the cursor and the connection
cur.close()
conn.close()

print(f"Table '{args.table_name}' has been truncated.")
