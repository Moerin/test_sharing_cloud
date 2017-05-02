# Run this with
# PYTHONPATH=</path/to/server> DJANGO_SETTINGS_MODULE=mobile.settings </path/to/server/>tornado_server.py
# Serves by default at

import logging

import django.core.handlers.wsgi

from tornado.options import define
from tornado.options import options
from tornado.options import parse_command_line

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

define('port', type=int, default=8888)
parse_command_line()


def main():

    logger = logging.getLogger(__name__)
    wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
    tornado_app = tornado.web.Application(
        [
            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ], debug=True)
    logger.info("Tornado server starting...")
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
