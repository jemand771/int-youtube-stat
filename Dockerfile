FROM python:3
WORKDIR /tmp
RUN pip install gunicorn
COPY ./requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app", "-w", "1", "--threads", "1"]
