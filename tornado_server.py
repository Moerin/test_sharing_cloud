# Run this with
# PYTHONPATH=</path/to/server> DJANGO_SETTINGS_MODULE=mobile.settings </path/to/server/>tornado_server.py
# Serves by default at
# http://localhost:8080/hello-tornado

from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

define('port', type=int, default=8888)
parse_command_line()


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello from tornado')


def main():

    logger = logging.getLogger(__name__)
    wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
    tornado_app = tornado.web.Application(
        [
            ('/hello-tornado', HelloHandler),
            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ], debug=True)
    logger.info("Tornado server starting...")
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
