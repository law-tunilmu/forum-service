# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 8000

# Set environment variables
ARG SUPABASE_URL
ARG SUPABASE_KEY
ARG DATABASE_HOST
ARG DATABASE_USER
ARG DATABASE_NAME
ARG DATABASE_PORT
ARG DATABASE_PASSWORD
ARG PRODUCTION

# set environment variables
ENV SUPABASE_URL=${SUPABASE_URL}
ENV SUPABASE_KEY=${SUPABASE_KEY}
ENV DATABASE_HOST=${DATABASE_HOST}
ENV DATABASE_USER=${DATABASE_USER}
ENV DATABASE_NAME=${DATABASE_NAME}
ENV DATABASE_PORT=${DATABASE_PORT}
ENV DATABASE_PASSWORD=${DATABASE_PASSWORD}
ENV PRODUCTION=${PRODUCTION}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]