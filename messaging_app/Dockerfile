FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose Django default port
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
