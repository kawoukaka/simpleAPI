import os

server_tier = os.environ.get('SERVER_TIER') or 'local'

if server_tier in ['local']:
    pass
if server_tier in ['dev']:
    CORS_ORGINS = 'http://xxx.example.com:8001'

DEBUG = True
SECRET_KEY = 'Sm9obiBTY2hyb20ga2lja3MgYXNz'
