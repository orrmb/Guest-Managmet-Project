FROM python:3.11.9-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY Guest_management .
RUN ls
ENTRYPOINT [ "python3 Guest_management/app.py" ]