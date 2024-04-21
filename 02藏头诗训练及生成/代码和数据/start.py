import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import json
import os
from tornado.ioloop import IOLoop
from tornado import web
import shutil
from Handle import *



application = web.Application([
    (r'/', IndexHandler),
    ],
    static_path="static",
    template_path='templates',
    autoreload = True)

if __name__ == "__main__":
    application.listen(8765)
    IOLoop.current().start()