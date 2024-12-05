FROM python:3.11-slim

WORKDIR /Todo

COPY requirements.txt /Todo/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /Todo/

CMD ["python", "main.py"]