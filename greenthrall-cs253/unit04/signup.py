
import hashlib
import hmac
import jinja2
import os
import random
import re
import webapp2

from google.appengine.ext import db
from string import letters

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

secret = 'fart'


#### Page Render Functions ####
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


#### Validation Functions ####
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
PASS_RE = re.compile(r"^.{3,20}$")
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")


def validate_email(email):
    return not email or EMAIL_RE.match(email)


def validate_password(password):
    return password and PASS_RE.match(password)


def validate_username(username):
    return username and USER_RE.match(username)


#### User Hash Functions ####
def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())


def validate_pw_hash(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


#### Database Functions ####
def users_key(group='default'):
    return db.Key.from_path('users', group)


#### Main Class Handler ####
class MainHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and UsersDB.by_id(int(uid))


#### Signup Class Handler ####
class SignupHandler(MainHandler):
    def get(self):
        self.render("signup.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

        if not validate_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not validate_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True

        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not validate_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup.html', **params)

        else:
            self.done()

    def done(self):
        o_username = UsersDB.by_name(self.username)
        if o_username:
            msg = 'That user already exists.'
            self.render('signup.html', error_username=msg)
        else:
            o_username = UsersDB.register(self.username, self.password, self.email)
            o_username.put()

            self.login(o_username)
            self.redirect('/unit04/welcome')


#### Login Class Handler ####
class LoginHandler(MainHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        o_username = UsersDB.login(username, password)
        if o_username:
            self.login(o_username)
            self.redirect('/unit04/welcome')

        else:
            msg = 'Invalid login'
            self.render('login.html', error=msg)


#### Logout Class Handler ####
class LogoutHandler(MainHandler):
    def get(self):
        self.logout()
        self.redirect('/unit04/signup')


#### Welcome Class Handler ####
class WelcomeHandler(MainHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.name)

        else:
            self.redirect('/unit04/signup')


#### Database Class Handler ####
class UsersDB(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return UsersDB.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        o_username = UsersDB.all().filter('name =', name).get()
        return o_username

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return UsersDB(parent=users_key(),
                       name=name,
                       pw_hash=pw_hash,
                       email=email)

    @classmethod
    def login(cls, name, pw):
        o_username = cls.by_name(name)
        if o_username and validate_pw_hash(name, pw, o_username.pw_hash):
            return o_username


app = webapp2.WSGIApplication([
                              ('/unit04/signup', SignupHandler),
                              ('/unit04/welcome', WelcomeHandler),
                              ('/unit04/login', LoginHandler),
                              ('/unit04/logout', LogoutHandler)
                              ], debug=True)
