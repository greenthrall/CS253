
import webapp2

class HelloHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Hello, Udacity!')

app = webapp2.WSGIApplication([
                              ('/unit01/hello', HelloHandler),
                              ], debug=True)
