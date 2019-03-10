FROM python:3.6
RUN mkdir app/
COPY requirements.txt app/requirements.txt
RUN pip install -U pip
WORKDIR app
RUN pip install -r requirements.txt
