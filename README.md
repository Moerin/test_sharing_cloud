# Django, Tornado and Nginx in containers, using Supervisord

This project contains a microblogging Django application with
Tornado as wsgi server and websocket provider.
Nginx is used as reverse_proxy and Supervisord managed python process.

### Build and run
#### Build with python2
* `./launch.sh`
* go to test.sharing.cloud to see if works

Config file are presents in nginx and app-config folders
