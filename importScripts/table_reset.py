"""
This file contains script to erase data from a selected table.
"""
import glob
import json
import os
import psycopg2


# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres.seqkcnapvgkwqbqipqqs",
                        password="IT Web Server12", host="aws-0-ap-southeast-2.pooler.supabase.com", port=6543)
cur = conn.cursor()

#TRUNCATE TABLE [name of the table] CASCADE;
cur.execute("""TRUNCATE TABLE subjects CASCADE;""")

#Commit the transaction    
conn.commit()

#Close the cursor
cur.close()
conn.close()
    