FROM python:3.8 as release
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY src/ /app/src/
COPY static/ /app/static/
COPY templates/ /app/templates/
COPY config.py /app/
COPY app.py /app/
COPY models.py /app/
COPY swagger.yml /app/
COPY entrypoint.sh /app/
COPY gunicorn_config.py /app/
EXPOSE 8000

RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]