# Dockerfile for Django FaceValue project

# Use official Python image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project code
COPY . /app/

# Copy and set execute permission on entrypoint
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Expose port and start server
EXPOSE 8000

# Entrypoint to handle migrations and collectstatic
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "facevalue.wsgi:application", "--bind", "0.0.0.0:8000"]
