import os

server_tier = os.environ.get('SERVER_TIER') or 'local'

if server_tier in ['local']:
    DEBUG = True
if server_tier in ['dev']:
    DEBUG = False
    # example for deployment on dev server
    CORS_ORGINS = 'http://xxx.example.com:8001'


SECRET_KEY = 'Sm9obiBTY2hyb20ga2lja3MgYXNz'
