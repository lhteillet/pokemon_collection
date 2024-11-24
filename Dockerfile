# Use the official MariaDB image
FROM mariadb:latest

# Install Python and pip, and install virtualenv
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv

# Create a working directory for your application
WORKDIR /app

# Create and activate a virtual environment
RUN python3 -m venv /app/venv

# Upgrade pip to the latest version
RUN /app/venv/bin/pip install --upgrade pip

# Copy the requirements.txt into the container
COPY requirements.txt /app/requirements.txt

# Install Python dependencies in the virtual environment
RUN /app/venv/bin/pip install -r /app/requirements.txt

# Copy the SQL initialization script and Python script into the container
COPY init-scripts/init.sql /docker-entrypoint-initdb.d/
COPY init-scripts/create_triggers.py /docker-entrypoint-initdb.d/