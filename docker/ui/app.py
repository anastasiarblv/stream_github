# https://konstantinklepikov.github.io/myknowlegebase/notes/sqlalchemy-docs.html
# https://pythonru.com/biblioteki/crud-sqlalchemy-core
from os import environ ## для чтения переменных среды, для подключения к базе данных
import streamlit as st
import time
import psycopg2
from psycopg2 import OperationalError
from sqlalchemy import create_engine, text

def fetch_data():
    try:
        DATABASE_URL = environ.get('DATABASE_URL')
        engine = create_engine(DATABASE_URL)
        conn = engine.connect() 
        select_query_string = f"SELECT * FROM sentences"
        result = conn.execute(text(select_query_string))
        rows = result.fetchall()
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
    
