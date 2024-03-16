FROM python:3.9-slim-bullseye

WORKDIR /app
COPY . /app
RUN pip3 --no-cache-dir install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]