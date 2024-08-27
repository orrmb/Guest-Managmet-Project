FROM python:3.11.9-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip \
    pip install -r requirements.txt
COPY Guest_management .
RUN ls
ENTRYPOINT [ "python app.py" ]