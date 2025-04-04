FROM python:3.9-slim

WORKDIR /app

COPY . .

CMD ["python", "super_parser.py"]