FROM python:3

RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
WORKDIR /usr/src/app
RUN pip install -r requirements.txt

COPY . /usr/src/app

CMD ["python", "bot.py"]