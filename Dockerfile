FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p reports

ENV PYTHONPATH=/app

# More flexible CMD to allow Jenkins to pass extra flags
CMD ["python", "-m", "pytest"]
