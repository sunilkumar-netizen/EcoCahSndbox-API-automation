# Dockerfile for API Automation Framework

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    openjdk-11-jre \
    && rm -rf /var/lib/apt/lists/*

# Install Allure command-line tool
RUN wget -q https://github.com/allure-framework/allure2/releases/download/2.25.0/allure-2.25.0.tgz && \
    tar -zxvf allure-2.25.0.tgz -C /opt/ && \
    ln -s /opt/allure-2.25.0/bin/allure /usr/bin/allure && \
    rm allure-2.25.0.tgz

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p logs reports/allure-results reports/junit

# Set environment variables
ENV PYTHONPATH=/app
ENV ENVIRONMENT=qa

# Default command
CMD ["behave", "-D", "env=qa", "--tags=smoke"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import behave; print('OK')" || exit 1
