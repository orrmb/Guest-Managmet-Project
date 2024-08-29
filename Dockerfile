FROM python:3.11.9-slim-bullseye
WORKDIR /app
COPY Guest_management .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3","app.py" ]