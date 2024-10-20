# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Set the working directory to the root of the project
WORKDIR /app

# Run the Django development server by default
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]