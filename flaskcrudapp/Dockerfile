# Step 1: Select the base image
FROM python:latest

# Step 2: Setting up environment
RUN apt install python3

# Step 3: Configure the software
WORKDIR /app

# copy files
COPY requirements.txt /app

RUN pip3 install -r requirements.txt

# Copying project files.
COPY . /app

# Exposing an internal port
EXPOSE 5001

# Step 4 set default command
CMD ["python3", "restapi.py"]
