# Use a base Python image
FROM python:3.7

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script to the working directory
COPY check_f5_ssl_monitoring.py .

# Set the entrypoint to execute the Python script
ENTRYPOINT ["python", "/app/check_f5_ssl_monitoring.py"]

