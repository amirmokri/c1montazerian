# Use the official Python image from the Docker Hub
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libmariadb-dev-compat \
    libmariadb-dev \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /siwan_store/
RUN apt-get install -y pkg-config python3-dev default-libmysqlclient-dev build-essential
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the project files
COPY . /store/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]