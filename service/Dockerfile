FROM python:3.9.16-slim-buster

WORKDIR /service

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./src ./src
COPY ./config.py ./config.py
COPY ./main.py ./main.py

EXPOSE 8001

CMD ["python", "main.py"]

