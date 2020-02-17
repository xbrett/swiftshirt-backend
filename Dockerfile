FROM python:3.6-alpine

WORKDIR /usr/src/app

EXPOSE 5000

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt


COPY . .

CMD ["python", "application.py"]