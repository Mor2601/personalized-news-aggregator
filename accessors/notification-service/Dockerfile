# Use an official Python runtime as a parent image
FROM python:3.11.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install dotenv package to load environment variables
RUN pip install python-dotenv



# Define environment variables for Dapr
ENV DAPR_HTTP_PORT=$DAPR_HTTP_PORT
    

CMD [ "python","src/main.py" ]