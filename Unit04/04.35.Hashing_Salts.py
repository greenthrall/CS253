
import hashlib
import random
import string


def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

# implement the function make_pw_hash(name, pw) that returns a hashed password 
# of the format: 
# HASH(name + pw + salt),salt
# use sha256


def make_pw_hash(name, pw):
    v_salt = make_salt()
    v_hash = hashlib.sha256(name + pw + v_salt).hexdigest()
    return "%s,%s" % (v_hash, v_salt)


print make_pw_hash("Travis", "123")