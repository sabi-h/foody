# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /foody

# Copy the current directory contents into the container at /app
COPY . /foody

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 7007

# Define environment variable
ENV NAME World

# Run main.py when the container launches
CMD ["python", "main.py"]
