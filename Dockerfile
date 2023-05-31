FROM python:3.10

WORKDIR /app

VOLUME /app/shared

COPY . /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["python3", "server.py"]
