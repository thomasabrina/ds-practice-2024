FROM python:3.11
WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app"
COPY ./book_database/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install reloadium
CMD reloadium run "book_database/src/app.py"