import os

server_tier = os.environ.get('SERVER_TIER') or 'local'

if server_tier in ['local']:
    DEBUG = True
if server_tier in ['dev']:
    # example for deployment on dev server
    DEBUG = False
    SERVER_NAME = 'http://127.0.0.1:8001'
    CORS_ORGINS = 'http://127.0.0.1:8001'


SECRET_KEY = 'Sm9obiBTY2hyb20ga2lja3MgYXNz'
