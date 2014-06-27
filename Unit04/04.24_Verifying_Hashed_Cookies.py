import hashlib

def hash_str(s):
    return hashlib.md5(s).hexdigest()

def make_secure_val(s):
    return "%s,%s" % (s, hash_str(s))

# -----------------
# User Instructions
# 
# Implement the function check_secure_val, which takes a string of the format 
# s,HASH
# and returns s if hash_str(s) == HASH, otherwise None 

def check_secure_val(h):
    v_result = h.split(',')[0]
    if h == make_secure_val(v_result):
        return v_result

# Original answer
#    v_pos = h.find(',')
#    if v_pos:
#        v_orig = h[:v_pos]
#        v_hash = h[v_pos+1:]
#        if hash_str(v_orig) == v_hash:
#            return v_orig

print check_secure_val(make_secure_val('cool'))