FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["streamlit", "run", "--server.enableCORS", "false", "app.py"]