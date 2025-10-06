# Use a small base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port Render will use
EXPOSE 8000

# Command to run Django
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
