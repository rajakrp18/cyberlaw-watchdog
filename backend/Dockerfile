FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Playwright + PDF tools
RUN apt-get update && apt-get install -y \
    curl wget git build-essential \
    libpq-dev gcc \
    libffi-dev libssl-dev \
    libmupdf-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium --with-deps

COPY . .

EXPOSE 8000
