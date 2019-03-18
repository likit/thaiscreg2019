FROM python:3.6
RUN mkdir /app
COPY requirements.txt /app/requirements.txt
RUN pip install -U pip
RUN pip install -r /app/requirements.txt
CMD ["gunicorn", "app.app:app", "-b", "0.0.0.0:5000"]
