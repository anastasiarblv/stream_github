# https://konstantinklepikov.github.io/myknowlegebase/notes/sqlalchemy-docs.html
# https://planetscale.com/blog/using-mysql-with-sql-alchemy-hands-on-examples
# https://pythonru.com/biblioteki/crud-sqlalchemy-core
from os import environ ## для чтения переменных среды, для подключения к базе данных
from kafka import KafkaConsumer
import json
import psycopg2
from sqlalchemy import create_engine, text
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()

DATABASE_URL = environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL)

kafka_nodes = "kafka:9092"
myTopic = "sentence"

consumer = KafkaConsumer(myTopic,
                        bootstrap_servers=kafka_nodes,
                        value_deserializer=lambda x: json.loads(x.decode('utf-8')))
with engine.connect() as conn:
    for message in consumer:
        data = message.value
        print(data)
        #sentence = data['sentence']
        scores = analyzer.polarity_scores(data['sentence'])
        #compound = scores['compound']
        print(scores['compound'])
        #Вставляем данные в Postgres
        insert_query_string = f"INSERT INTO sentences (sentence, sentiment) VALUES(:sentence, :sentiment)"
        #conn.execute(text(insert_query_string),your_parameters)
        conn.execute(text(insert_query_string), dict(sentence = data['sentence'], sentiment = scores['compound']))
        #                          parameters = dict(sentence = sentence, sentiment = compound)
        conn.commit()

#import sqlalchemy
#from sqlalchemy import create_engine
#engine = create_engine('mysql://admin:passkey@svc-3nb226d8-ee13-47f0-8ca4-2dc820773442-dml.aws-oregon-2.svc.singlestore.com:3306/dbTest')
#conn = engine.connect()
#conn.execute(text("CREATE TABLE stock (ID INT, Code VARCHAR(4), Qty INT)"))
#conn.execute(text("INSERT INTO stock VALUES (1,'xvfg',23)"))
#conn.execute(text("INSERT INTO stock VALUES (2,'dtsi',12)"))
#conn.execute(text("INSERT INTO stock VALUES (3,'rtky',8)"))
#conn.close()

#with db.connect() as conn:
#    conn.execute(statement=query, parameters=dict(_age=5, _country='US'))

#with db.connect() as conn:
#    conn.execute(statement=query, parameters=dict(_age=5, _country='US'))

#connection = st.experimental_connection(name = 'ghost', type = 'sql', autocommit = True)
#with connection.session as session:
#    session.execute('INSERT INTO document (ID, SENTENCE) VALUES(:id, :sen);', params = dict(id = id, sen = answer))
#    session.commit()

# "commit as you go"
#with engine.connect() as conn:
#    conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x :y)"),[{"x": 1, "y": 1}, {"x": 2, "y": 4}])
#    conn.commit()


