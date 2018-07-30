
# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3.6

# If you prefer miniconda:
#FROM continuumio/miniconda3

LABEL Name=meta-music Version=0.0.1
EXPOSE 5000

ADD ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN apt-get -y update
RUN apt-get install -y ffmpeg
RUN apt-get install -y libportaudio2 
RUN pip install -r requirements.txt
RUN apt-get install -y nano
ADD . /app 

# Using apt:
# Using pip:
CMD ["python3", "app.py"]

# Using pipenv:
#RUN python3 -m pip install pipenv
#RUN pipenv install --ignore-pipfile
#CMD ["pipenv", "run", "python3", "-m", "meta-music"]

# Using miniconda (make sure to replace 'myenv' w/ your environment name):
#RUN conda env create -f environment.yml
#CMD /bin/bash -c "source activate myenv && python3 -m meta-music"
