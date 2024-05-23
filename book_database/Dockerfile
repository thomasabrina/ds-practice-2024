FROM python:3.11
WORKDIR /app
COPY ./book_database/requirements.txt .
RUN pip install -r requirements.txt
COPY ./book_database/src/ .
COPY ./utils /app/utils
CMD ["python", "app.py"]