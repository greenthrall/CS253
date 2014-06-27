
import cgi
import re
import webapp2

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

signup_page = """
<!DOCTYPE html>
<html>
    <head>
        <title>Unit 02 Signup</title>
        <style type="text/css">
            .label {text-align: right}
            .error {color: red}
        </style>
    </head>
    <body>
        <h2>Signup</h2>
        <form method="post">
            <table>
                <tr>
                    <td class="label">
                        Username
                    </td>
                    <td>
                        <input type="text" name="username" value="%(username)s">
                    </td>
                    <td class="error">
                        %(error_username)s
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        Password
                    </td>
                    <td>
                        <input type="password" name="password" value="">
                    </td>
                    <td class="error">
                        %(error_password)s
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        Verify Password
                    </td>
                    <td>
                        <input type="password" name="verify" value="">
                    </td>
                    <td class="error">
                        %(error_verify)s
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        Email (optional)
                    </td>
                    <td>
                        <input type="text" name="email" value="%(email)s">
                    </td>
                    <td class="error">
                        %(error_email)s
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>
    </body>
</html>
"""

welcome_page = """
<!DOCTYPE html>
<html>
    <head>
        <title>Unit 02 Welcome</title>
    </head>
    <body>
        <h2>Welcome, %(username)s!</h2>
    </body>
</html>
"""


def validate_username(username):
    return username and USER_RE.match(username)


def validate_password(password):
    return password and PASS_RE.match(password)


def validate_email(email):
    return not email or EMAIL_RE.match(email)


class SignUpHandler(webapp2.RequestHandler):
    def write_form(self,
                   username="",
                   error_username="",
                   error_password="",
                   error_verify="",
                   email="",
                   error_email=""):
        self.response.out.write(signup_page % {"username": username,
                                               "error_username": error_username,
                                               "error_password": error_password,
                                               "error_verify": error_verify,
                                               "email": email,
                                               "error_email": error_email})

    def get(self):
        self.write_form()

    def post(self):
        err_flag = False
        err_username = ""
        err_password = ""
        err_verify = ""
        err_email = ""
        v_username = self.request.get("username")
        v_password = self.request.get("password")
        v_verify = self.request.get("verify")
        v_email = self.request.get("email")

        if not validate_username(v_username):
            err_username = "That's not a valid username."
            err_flag = True

        if not validate_password(v_password):
            err_password = "That wasn't a valid password."
            err_flag = True

        elif v_password != v_verify:
            err_verify = "Your passwords didn't match."
            err_flag = True

        if not validate_email(v_email) and v_email != "":
            err_email = "That's not a valid email."
            err_flag = True

        if err_flag:
            self.write_form(v_username,
                            err_username,
                            err_password,
                            err_verify,
                            v_email,
                            err_email)

        else:
            self.redirect("/unit02/welcome?username=" + v_username)


class WelcomeHandler(webapp2.RequestHandler):
    def write_form(self, username=""):
        self.response.out.write(welcome_page % {"username": username})

    def get(self):
        v_username = self.request.get("username")
        if validate_username(v_username):
            self.write_form(v_username)
        else:
            self.redirect("/unit02/signup")


app = webapp2.WSGIApplication([
                              ("/unit02/signup", SignUpHandler),
                              ("/unit02/welcome", WelcomeHandler)
                              ], debug=True)
