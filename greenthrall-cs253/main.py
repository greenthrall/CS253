
import cgi
import webapp2

menu = """
<nav>
    <ul>
        <li><a href="/unit01/hello">Unit 01 Hello World</a></li>
        <li><a href="/unit02/date">Unit 02 Birthday Entry</a></li>
        <li><a href="/unit02/rot13">Unit 02 Rot13</a></li>
        <li><a href="/unit02/signup">Unit 02 Signup</a></li>
        <li><a href="/unit03/ascii">Unit 03 Ascii Art</a></li>
        <li><a href="/unit03/blog">Unit 03 Blog</a></li>
        <li><a href="/unit04/signup">Unit 04 Signup</a></li>
        <li><a href="/unit05/ascii">Unit 05 Ascii Art</a></li>
        <li><a href="/unit05/blog">Unit 05 JSON Blog</a></li>
        <li><a href="/unit06/ascii">Unit 06 Ascii Art</a></li>
        <li><a href="/unit06/blog">Unit 06 Cache Blog</a></li>
        <li><a href="/unit07/wiki">Unit 07 Wiki</a></li>
    </ul>
</nav>
"""


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(menu)

app = webapp2.WSGIApplication([('/', MainHandler)
                              ], debug=True)
