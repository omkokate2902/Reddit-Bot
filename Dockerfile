# Use the official Python image as a parent image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Create a virtual environment inside the container
RUN python -m venv /app/myenv

# Activate the virtual environment and install the required packages
RUN /app/myenv/bin/pip install --upgrade pip && \
    /app/myenv/bin/pip install -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Set environment variable for virtual environment
ENV VIRTUAL_ENV=/app/myenv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Run your application
CMD ["python", "app.py"]