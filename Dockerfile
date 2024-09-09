# Use the official Python base image
FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . /app

