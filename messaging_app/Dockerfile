FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Optional EXPOSE (still good practice)
EXPOSE 8000

# Correct CMD (no -p flag)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
