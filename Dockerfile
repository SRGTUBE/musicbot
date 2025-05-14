# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies for certain Python packages (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install the required Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variables from Railway secrets
# Assuming you have your `DISCORD_TOKEN` and other sensitive data in Railway secrets
ENV DISCORD_TOKEN=${DISCORD_TOKEN}

# Expose the port the bot will run on (optional)
EXPOSE 8080

# Run the bot using the provided entry point (main.py)
CMD ["python", "main.py"]
