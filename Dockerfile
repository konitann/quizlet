FROM python:3.11-bullseye

RUN pip install Flask Flask-SQLAlchemy Flask-Migrate flask-login mysqlclient


WORKDIR /app
COPY app.py app.py
COPY templates templates

EXPOSE 8080

CMD ["python", "app.py"]
