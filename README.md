# Django, Tornado and Nginx in containers, using Supervisord

This project contains a microblogging Django application with
Tornado as wsgi server and websocket provider.
Nginx is used as reverse_proxy and Supervisord managed python process.

### Build and run
#### Build with python2
Please add 'test.sharing.cloud' to your /etc/hosts binded to lo
* `127.0.0.1 test.sharing.cloud`
* `docker-compose build`
* `docker-compose up`
* go to test.sharing.cloud to see if works

Config file are presents in nginx and app-config folders
