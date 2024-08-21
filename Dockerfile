FROM python:3.9-slim

# ... other Dockerfile instructions ...

# Mount the Cloud Storage bucket as a volume
VOLUME /mnt/data

# Copy your Python code to the container
COPY . /app

# Set the working directory
WORKDIR /app

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV PORT 8080

# Install dependencies
RUN pip install -r requirements.txt

# Define the entry point for your application
CMD ["python", "main.py"]
