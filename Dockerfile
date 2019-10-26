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
COPY test_server.py /usr/src/
COPY swagger.yml /usr/local/lib/python2.7/dist-packages/flask_swagger_ui/dist/
COPY templates/index.html /usr/src/templates/

# run the test suite
CMD ["unit2", "discover", "-v", "-s", "/usr/src/"]

# tell the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python", "/usr/src/server.py"]
