FROM python:3.11.9-slim-bullseye
WORKDIR /app
COPY ["requirements.txt", "Guest_management/"] .
RUN pip install -r requirements.txt
RUN ls
ENTRYPOINT [ "python3 Guest_management/app.py" ]