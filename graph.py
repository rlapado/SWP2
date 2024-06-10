from cgi import parse_qs
from template import html
import matplotlib.pyplot as plt
import os

def application(environ, start_response):
    if environ['PATH_INFO'] == '/graph.png':
        img_dir = './img'
        img_path = os.path.join(img_dir, 'graph.png')

        try:
            with open(img_path, 'rb') as f:
                response_body = f.read()
        except FileNotFoundError:
            response_body = b'Image not found'
            start_response('404 Not Found', [
                ('Content-Type', 'text/plain'),
                ('Content-Length', str(len(response_body)))
            ])
            return [response_body]

        start_response('200 OK', [
            ('Content-Type', 'image/png'),
            ('Content-Length', str(len(response_body)))
        ])
        return [response_body]

    else:
        d = parse_qs(environ['QUERY_STRING'])
        a = d.get('a', [''])[0]
        b = d.get('b', [''])[0]
        c = d.get('c', [''])[0]

        if '' not in [a, b, c]:
            try:
                a, b, c = int(a), int(b), int(c)
            except ValueError:
                response_body = b'Invalid parameters'
                start_response('400 Bad Request', [
                    ('Content-Type', 'text/plain'),
                    ('Content-Length', str(len(response_body)))
                ])
                return [response_body]

            x = [n / 10.0 for n in range(-40, 41)]
            y = [a * n ** 2 + b * n + c for n in x]

            fig = plt.figure()
            plt.plot(x, y)
            plt.grid()

            if not os.path.exists(img_dir):
                os.makedirs(img_dir)

            fig.savefig(img_path)
            plt.close(fig)

            response_body = html
            start_response('200 OK', [
                ('Content-Type', 'text/html'),
                ('Content-Length', str(len(response_body)))
            ])
            return [response_body]

        else:
            response_body = html
            start_response('200 OK', [
                ('Content-Type', 'text/html'),
                ('Content-Length', str(len(response_body)))
            ])
            return [response_body]

