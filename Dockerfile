FROM centos:7

LABEL maintainer "tiagocostaloureiro@gmail.com"

RUN yum -y update && yum -y install epel-release && \
    yum -y install python34-devel \
    python34-pip \
    gcc-c++ \
    gettext \
    npm \
    git

# Disable Python Output Buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH $PYTHONPATH:/api/watergenius_api
ENV TERM=linux

# Create app directory
RUN mkdir /api
WORKDIR /api

# Add all files [Except the ones in dockerignore file]
COPY . /api/

RUN chmod +x /api/docker-entrypoint.sh

RUN ls -lsa

# update pip and setuptools
RUN pip3.6 install pip setuptools --upgrade
# install project dependencies
RUN pip3.6 install -r requirements/docker.txt --upgrade
RUN pip3.6 install djangorestframework
RUN pip3.6 install markdown       # Markdown support for the browsable API.
RUN pip3.6 install django-filter  # Filt

EXPOSE 8000

#ENTRYPOINT ["/api/docker-entrypoint.sh"]

CMD ["python3.6", "watergenius_api/manage.py", "runserver", "0.0.0.0:8000"]
