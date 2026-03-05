FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
  && addgroup --system api \
  && adduser --system --ingroup api api

COPY app.py .

USER api
EXPOSE 5000
CMD ["python", "app.py"]
