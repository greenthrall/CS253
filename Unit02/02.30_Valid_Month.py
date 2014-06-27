# -----------
# User Instructions
# 
# Modify the valid_month() function to verify 
# whether the data a user enters is a valid 
# month. If the passed in parameter 'month' 
# is not a valid month, return None. 
# If 'month' is a valid month, then return 
# the name of the month with the first letter 
# capitalized.
#

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

month_abbvs = dict((m[:3].lower(), m) for m in months)

def valid_month(month):
# Updated test answer
    if month:
        v_mon = month[:3].lower()
        return month_abbvs.get(v_mon)

# Original test answer
#    if month:
#        v_mon = month.capitalize()
#        if v_mon in months:
#            return v_mon

# My original answer
#    v_mon = ''.join(word.capitalize() for word in month.split())
#    if v_mon in months:
#        return v_mon
#    else:
#        return None

print valid_month("January")
# => "January"
print valid_month("january")
# => "January"    
print valid_month("foo")
# => None
print valid_month("")
# => None
