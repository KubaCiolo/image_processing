# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Ensure the binary file has the correct executable permissions
RUN chmod +x /usr/local/lib/python3.9/site-packages/agh_vqis/binaries/agh_vqis_linux_x86_64_mt

# Run the Django development server by default
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]