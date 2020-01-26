FROM python:3.7

ENV PYTHONUNBUFFERED 1

# Install dependencies required for psycopg2 python package
RUN set -xe \
  && apt-get update \
  && apt-get install -y gcc python3-dev musl-dev

# create root directory for our project in the container
RUN mkdir /bazinga

# Set the working directory to /bazinga
WORKDIR /bazinga

# Copy the current directory contents into the container at /bazinga
ADD . /bazinga/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements/base.txt