# FROM python:3.8-alpine


# WORKDIR /

# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0

# COPY requirements.txt requirements.txt

# RUN apk add --no-cache gcc musl-dev linux-headers
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# RUN pip list | grep pytest

# COPY . .
# WORKDIR /
# RUN coverage run -m pytest /plants/tests
# RUN coverage report -m

# CMD ["python3", "-m", "plants.web_app"]
# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Set the working directory in the container
WORKDIR /

# Set environment variables that are needed
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Install any needed packages specified in requirements.txt
COPY requirements.txt requirements.txt
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /
COPY . .

# Define the command to run the app
CMD ["python3", "-m", "plants.web_app"]
