FROM python:3.11-slim
LABEL maintainer="TheUCP"
LABEL build_date="2024-12-8"
WORKDIR /Todo

COPY . .

RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "main.py"]