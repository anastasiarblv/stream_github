import streamlit as st
import time
import psycopg2
from psycopg2 import OperationalError
import logging

logging.basicConfig(level=logging.INFO)

POSTGRES_DB='postgres'
POSTGRES_USER= 'postgres'
POSTGRES_PASSWORD='postgres'
container_name_postgres ='postgres'
PORT = '5432'

def fetch_data():
    try:
        conn = psycopg2.connect(dbname=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=container_name_postgres, port = PORT)
        cur = conn.cursor()
        cur.execute("SELECT * FROM sentences")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except OperationalError as e:
        st.err(f"OperationalError : {e}")
        return 
    except Exception as e:
        return []
    
def main():
    st.title("Sentence Data dashboard")
    st.write("Here is your sentiment analysis on sentence data:")
    unique_id = set()
    while True:
        data = fetch_data()
        if data:
            for row in data:
                id = row[0]
                if id in unique_id:
                    continue
                st.write(row)
                unique_id.add(id)
        else:
            st.write("")
        time.sleep(5)

if __name__=="__main__":
    main()
    
