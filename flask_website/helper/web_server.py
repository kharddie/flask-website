"""
import asyncio
import tornado.web

class WebServer(tornado.web.Application):

    def __init__(self):
        handlers = [ (r"/test", TestHandler), ]
        settings = {'debug': True}
        super().__init__(handlers, **settings)

    def run(self, port=5000):
        print("port listening to",{port})
        self.listen(port)
        tornado.ioloop.IOLoop.instance().start()

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("test success")

        """