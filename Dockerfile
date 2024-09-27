# First stage: Build environment
FROM python:3.11-slim AS builder

# Set the working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*


# Copy only the requirements file to install dependencies
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Second stage: Final runtime environment
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install runtime dependencies
RUN apt update && apt install -y \
    nano \
    telnet \
    iputils-ping \
    libpq-dev  # This is needed for psycopg2 or psycopg2-binary

# Copy only the installed dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy the application code to the working directory
COPY . /app

# Expose port 8080 (or any other port you choose)
EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

