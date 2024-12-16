from kafka import KafkaConsumer
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import psycopg2
import nltk

nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()


POSTGRES_DB='postgres'
POSTGRES_USER= 'postgres'
POSTGRES_PASSWORD='postgres'
container_name_postgres ='postgres'
PORT = '5432'
conn = psycopg2.connect(dbname=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=container_name_postgres, port = PORT)
cur = conn.cursor()

kafka_nodes = "kafka:9092"
myTopic = "sentence"

consumer = KafkaConsumer(myTopic,
                        bootstrap_servers=kafka_nodes,
                        value_deserializer=lambda x: json.loads(x.decode('utf-8')))
for message in consumer:
    data = message.value
    print(data)
    scores = analyzer.polarity_scores(data['sentence'])
    print(scores['compound'])
    #Вставляем данные в Postgres
    cur.execute("INSERT INTO sentences (sentence, sentiment) VALUES(%s, %s)", (data['sentence'], scores['compound']))
    conn.commit()