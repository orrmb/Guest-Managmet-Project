FROM python:3.11.9-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY Guest_management .
ENTRYPOINT [ "python3 app.py" ]