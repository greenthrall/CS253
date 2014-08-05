import jinja2
import os
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

# Used before adding Jinja2
#form_html = """
#<form>
#<h2>Add a Food</h2>
#<input type="text" name="food">
#%s
#<button>Add</button>
#</form>
#"""

# Used before adding Jinja2
#hidden_html = """
#<input type="hidden" name="food" value="%s">
#"""

# Used before adding Jinja2
#item_html = """
#<li>%s</li>
#"""

# Used before adding Jinja2
#shopping_list_html = """
#<br>
#<br>
#<h2>Shopping List</h2>
#<ul>
#%s
#</ul>
#"""


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **kw):
        t = jinja_env.get_template(template)
        return t.render(kw)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
    def get(self):
        n = self.request.get("n")
        if n:
            n = int(n)
        self.render("shopping_list.html", n=n)

        #Used before adding Jinja2
        #output = form_html
        #output_hidden = ""
        #items = self.request.get_all("food")
        #if items:
        #   output_items = ""
        #   for item in items:
        #       output_hidden += hidden_html % item
        #       output_items += item_html % item
        #       output_shopping = shopping_list_html % output_items
        #       output += output_shopping
        #   output = output % output_hidden
        #self.write(output)


class FizzBuzzHandler(Handler):
    def get(self):
        n = self.request.get('n', 0)
        n = n and int(n)
        self.render('fizzbuzz.html', n=n)


app = webapp2.WSGIApplication([
                              ('/', MainPage),
                                  ('/fizzbuzz', FizzBuzzHandler),
                              ], debug=True)