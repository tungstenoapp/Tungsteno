FROM python:3.9-buster

RUN mkdir /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app
EXPOSE 8000


RUN sed -i -e "s#all_interfaces=False#all_interfaces=True#" ./tsteno/gui/__init__.py

CMD ["python3", "./app.py"]
