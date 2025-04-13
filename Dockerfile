FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements-backend.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements-backend.txt

# Copy application code and rename to valid Python module name
COPY backend_code.py .
COPY ticker.json .
COPY .env .
COPY wsgi.py .

# Expose port
EXPOSE 5000

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"] 