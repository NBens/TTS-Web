from uuid import uuid4
from hashlib import md5

def generate_salt():
    """ Generates a random string to use for password generation """
    return uuid4().hex[:8].upper()

def generate_password_from_salt(salt, password):
    string = salt + password + "KEY123"
    return md5(string.encode('utf-8')).hexdigest()

def empty(string):
    return not bool(string.strip())

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions