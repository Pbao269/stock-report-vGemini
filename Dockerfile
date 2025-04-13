FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements-backend.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend_code.py .
COPY ticker.json .
COPY .env.example .env
COPY wsgi.py .

# Expose port
EXPOSE 5000

# Set default environment variables
ENV BACKEND_URL_PROD=https://api.stockreport.example.com
ENV FRONTEND_URL_PROD=https://fin-crack-frontend.vercel.app
ENV FLASK_ENV=development

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]