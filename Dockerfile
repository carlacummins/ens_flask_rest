# our base image
FROM debian:jessie-slim

# Install python and pip
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y python python-pip
RUN apt-get install -y python-dev libmysqlclient-dev
RUN apt-get clean all

# upgrade pip
RUN pip install --upgrade pip

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/
RUN pip install --no-cache-dir -r /usr/src/requirements.txt

# copy files required for the app to run
COPY server.py /usr/src/
COPY templates/index.html /usr/src/templates/

# tell the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python", "/usr/src/server.py"]
