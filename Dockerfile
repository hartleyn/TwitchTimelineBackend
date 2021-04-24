FROM python:3.7.4 as app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ARG FLASK_ENV="production"
ENV FLASK_ENV="${FLASK_ENV}" \
    FLASK_APP="app" \
    PYTHONUNBUFFERED="true"

COPY . .

RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["/app/docker-entrypoint.sh"]

EXPOSE 5001

CMD gunicorn -w 4 -b 0.0.0.0:5001 'app:create_app()' --reload --access-logfile -
