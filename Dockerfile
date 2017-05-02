# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM python:2-alpine

MAINTAINER Sebastien

# Install required packages and remove the apt packages cache when done.
RUN apk add --no-cache \
	git \
    supervisor \
	sqlite \
    postgresql-dev \
    gcc \
    musl-dev

COPY app-config/requirements.txt /home/docker/code/app/
RUN pip install -r /home/docker/code/app/requirements.txt

# setup all the configfiles
COPY app-config/supervisor.ini /etc/supervisor.d/

# add (the rest of) our code
COPY . /home/docker/code/

# Django env settings to dev env, change to base for production but need to add pgsl
ENV DJANGO_SETTINGS_MODULE=test_sharing_cloud.settings.dev

# Specific to Django
RUN mkdir -p /var/log/sharing_cloud

WORKDIR /home/docker/code/
RUN python manage.py collectstatic --noinput

# For load balancing purpose eg.
#EXPOSE 8888 1337
#CMD ["supervisord", "-n"]
