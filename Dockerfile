FROM python:3.8.10-slim

# Creation of the working directory called color_match
WORKDIR color_match

RUN apt-get update && apt-get install -y python-opencv

# Update pip
RUN pip install --upgrade pip

# Copy of the requirements in the working folder
COPY requirements.txt .

# Install required packages
RUN pip install -r requirements.txt

# Copy of the source files
COPY src/ .

# Run the flask app (not in production !)
CMD [ "python", "app.py"]
