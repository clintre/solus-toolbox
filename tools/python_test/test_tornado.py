import unittest
import tornado.web
from tornado.testing import AsyncHTTPTestCase

# A simple Web Handler
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Tornado is working on Solus!")

# Our test class inheriting from Tornado's built-in testing tools
class TestSolusTornadoApp(AsyncHTTPTestCase):
    def get_app(self):
        # This returns the application to be tested
        return tornado.web.Application([(r"/", MainHandler)])

    def test_homepage(self):
        # Fetch the route and assert the results
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b"Tornado is working on Solus!")

if __name__ == '__main__':
    unittest.main()
