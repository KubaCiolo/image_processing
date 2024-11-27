# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set execute permissions for the AGH VQIS binary
RUN chmod +x /usr/local/lib/python3.9/site-packages/agh_vqis/binaries/agh_vqis_linux_x86_64_mt

# Create the media/uploads and media/results directories
RUN mkdir -p /app/media/uploads /app/media/results

# Create the media/uploads and media/results directories
RUN mkdir -p /app/media/uploads /app/media/results

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]