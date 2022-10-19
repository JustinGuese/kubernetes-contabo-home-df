FROM python:alpine
RUN mkdir -p /app/persistent
WORKDIR /app
COPY ./src/requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
COPY ./src/app.py /app/app.py
CMD ["python3", "app.py"]