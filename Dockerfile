FROM python:3

COPY . /app
WORKDIR /app

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install slackclient
RUN pip install flask
RUN pip install requests

EXPOSE 5000

CMD ["python", "./app/app.py"]