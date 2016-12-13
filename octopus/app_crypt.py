
import uuid
import hashlib
 
def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


# print '====='
# v =  hash_password('today')
# print v
# print type(v)

# print len(v)