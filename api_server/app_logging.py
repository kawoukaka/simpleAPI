from flask import g, request

import datetime
import time
import json


class AppLogging():
    def set_logging(self, app):
        @app.before_request
        def start_timer():
            g.start = time.time()
            requests = {
                'request': {
                    'content_length': len(request.data),
                    'headers': dict(request.headers),
                    'method': request.method,
                    'payload': request.json,
                    'url': request.url
                }
            }

            app.logger.info(json.dumps(requests, indent=4))

        @app.after_request
        def log_request(response):
            now = time.time()
            duration = round(now - g.start, 2)
            dt = datetime.datetime.fromtimestamp(now)

            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            host = request.host.split(':', 1)[0]
            args = request.get_json()

            responses = {
                'response': {
                    'method': request.method,
                    'path': request.path,
                    'status': response.status_code,
                    'duration': duration,
                    'time': str(dt),
                    'ip': ip,
                    'host': host,
                    'result': args
                }
            }

            app.logger.info(json.dumps(responses, indent=4))

            return response
