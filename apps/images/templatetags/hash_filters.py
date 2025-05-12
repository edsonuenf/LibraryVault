import hashlib
from django import template

def hash_sha256(value, length=10):
    value = str(value)
    hash_digest = hashlib.sha256(value.encode('utf-8')).hexdigest()
    return hash_digest[:length]

register = template.Library()
register.filter('hash_sha256', hash_sha256)
