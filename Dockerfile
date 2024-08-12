# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
# COPY X509-cert-8417019844152440938.pem /run/secrets/mongo_cert.pem

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
# EXPOSE 8000

# Define environment variable
# ENV FLASK_APP=app.py

# Cleanup
RUN rm -rf X509*

# Run flask when the container launches
CMD ["python", "app.py"]
# CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
