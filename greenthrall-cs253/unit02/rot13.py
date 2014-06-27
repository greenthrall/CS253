import cgi
import webapp2


rotform="""
<!DOCTYPE html>
<html>
  <head>
    <title>Unit 02 ROT13</title>
  </head>
  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%(userentry)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>
</html>
"""


def escape_html(s):
    return cgi.escape(s, quote=True)


def rot13(char):
    if char.isalpha():
        v_char = char.lower()
        if v_char <= 'm':
            v_shift = 13
        else:
            v_shift = -13
    else:
        v_shift = 0
    return chr(ord(char) + v_shift)


def rot13_concat(string):
    return ''.join(rot13(char) for char in string)


class ROT13Handler(webapp2.RequestHandler):
    def write_form(self, userentry=""):
        self.response.out.write(rotform % {"userentry": userentry})

    def get(self):
        self.write_form()

    def post(self):
        self.write_form(escape_html(rot13_concat(self.request.get("text"))))


app = webapp2.WSGIApplication([('/unit02/rot13', ROT13Handler)
                              ], debug=True)
