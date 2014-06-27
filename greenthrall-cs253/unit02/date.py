import cgi
import webapp2

form="""
<form method="post">
    What is your birthday?
    <br>
    <label>
        Month
        <input type="text" name="month" value="%(month)s">
    </label>
    <label>
        Day
        <input type="text" name="day" value="%(day)s">
    </label>
    <label>
        Year
        <input type="text" name="year" value="%(year)s">
    </label>
    <div style="color: red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""

months = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

month_abbvs = dict((m[:3].lower(), m) for m in months)


def valid_month(month):
    if month:
        v_mon = month[:3].lower()
        return month_abbvs.get(v_mon)


def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day > 0 and day <= 31:
            return day


def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year > 1900 and year < 2020:
            return year


class DateHandler(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error": error,
                                        "month": month,
                                        "day": day,
                                        "year": year})

    def get(self):
        self.write_form()

    def post(self):
        user_month = self.request.get("month")
        user_day = self.request.get("day")
        user_year = self.request.get("year")

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if not (month and day and year):
            self.write_form("That doesn't look valid to me, friend.",
                            user_month, user_day, user_year)
        else:
            self.redirect("/unit02/date/thanks")


class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks!")

app = webapp2.WSGIApplication([
                              ("/unit02/date", DateHandler),
                              ("/unit02/date/thanks", ThanksHandler)
                              ], debug=True)
