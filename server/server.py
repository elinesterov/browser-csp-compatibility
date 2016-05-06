import sys
import logging

from flask import Flask, render_template, make_response, request, Response


DEFAULT_POLICY = "default-src 'none'"
LOGGER_FILE_NAME = 'access.log'

app = Flask(__name__)

logger = logging.getLogger('werkzeug')
handler = logging.FileHandler(LOGGER_FILE_NAME)
logger.addHandler(handler)

# Also add the handler to Flask's logger for cases
# where Werkzeug isn't used as the underlying WSGI server.
app.logger.addHandler(handler)


def request_handler(template, params):
    """
    Method tha generates response based on given template and set of parameters
    """
    if 'header' not in params.keys():
        params['header'] = None
    print(params)
    response = make_response(render_template(template, params=params))
    if params['header']:
        response.headers['Content-Security-Policy'] = params['policy']
    return response


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/base-uri')
def base_uri():
    """
    Test URI:

    using meta:
    http://127.0.0.1:8000/base-uri?policy=base-uri%20%27self%27
    http://127.0.0.1:8000/base-uri?allow=true&policy=base-uri%20http://example.com

    using header:
    http://127.0.0.1:8000/base-uri?header=true&policy=base-uri%20%27self%27
    http://127.0.0.1:8000/base-uri?header=true&allow=true&policy=base-uri%20http://example.com

    """
    params = {}
    params['meta'] = request.args.get('meta')
    params['allow'] = request.args.get('allow')
    params['header'] = request.args.get('header')
    params['policy'] = request.args.get('policy')

    return request_handler('base-uri.html', params)


@app.route('/child-src')
def child_src():
    # TODO: add frame redirect
    """
    Test URI:
    frame

    Allow:
    http://127.0.0.1:8000/child-src?meta=true&frame=true&allow=true&policy=child-src 'self';
    http://127.0.0.1:8000/child-src?frame=true&allow=true&header=true&policy=child-src 'self';
    Block:
    http://127.0.0.1:8000/child-src?meta=true&frame=true&policy=child-src 'none';
    http://127.0.0.1:8000/child-src?header=true&frame=true&header=true&policy=child-src 'none';

    worker:

    Allow:
    http://127.0.0.1:8000/child-src?worker=true&allow=true&policy=child-src 'self';
    http://127.0.0.1:8000/child-src?worker=true&allow=true&header=true&policy=child-src 'self';
    Block:
    http://127.0.0.1:8000/child-src?worker=true&policy=child-src 'none';
    http://127.0.0.1:8000/child-src?worker=true&header=true&policy=child-src 'none';

    shared:

    Allow:
    http://127.0.0.1:8000/child-src?shared=true&allow=true&policy=child-src 'self';
    http://127.0.0.1:8000/child-src?shared=true&allow=true&header=true&policy=child-src 'self';
    Block:
    http://127.0.0.1:8000/child-src?shared=true&policy=child-src 'none';
    http://127.0.0.1:8000/child-src?shared=true&header=true&policy=child-src 'none';

    """
    params = {}
    params['meta'] = request.args.get('meta')
    params['allow'] = request.args.get('allow')
    params['header'] = request.args.get('header')
    params['policy'] = request.args.get('policy')
    params['frame'] = request.args.get('frame')
    params['worker'] = request.args.get('worker')
    params['shared'] = request.args.get('shared')

    return request_handler('child-src.html', params)


@app.route('/connect-src')
def connect_src():
    """
    Test URI:

    Beacon:

    Allow:
    http://127.0.0.1:8000/connect-src?beacon=true&allow=true&meta=true&policy=connect-src http://127.0.0.1:8000
    http://127.0.0.1:8000/connect-src?beacon=true&allow=true&header=true&policy=connect-src http://127.0.0.1:8000
    Block:
    http://127.0.0.1:8000/connect-src?beacon=true&meta=true&policy=connect-src http://localhost:8000;
    http://127.0.0.1:8000/connect-src?beacon=true&header=true&policy=connect-src http://localhost:8008;

    XHR

    Allow:
    http://127.0.0.1:8000/connect-src?allow=true&xhr=true&policy=connect-src http://127.0.0.1:8000
    http://127.0.0.1:8000/connect-src?allow=true&xhr=true&header=true&policy=connect-src http://127.0.0.1:8000
    Block:
    http://127.0.0.1:8000/connect-src?xhr=true&policy=connect-src http://localhost:8000;
    http://127.0.0.1:8000/connect-src?xhr=true&header=true&policy=connect-src http://localhost:8000;
    """
    params = {}
    params['meta'] = request.args.get('meta')
    params['allow'] = request.args.get('allow')
    params['header'] = request.args.get('header')
    params['policy'] = request.args.get('policy')
    params['beacon'] = request.args.get('beacon')
    params['event'] = request.args.get('event')
    params['websocket'] = request.args.get('websocket')
    params['xhr'] = request.args.get('xhr')

    return request_handler('connect-src.html', params)


@app.route('/form-action')
def form_action():
    """
    Test uri for form-action directive:
    Allow:
    http://127.0.0.1:8000/form-action?allow=true&meta=true&policy=form-action 'self'
    http://127.0.0.1:8000/form-action?allow=true&header=true&policy=form-action 'self'
    Block:
    http://127.0.0.1:8000/form-action?meta=true&policy=form-action 'none'
    http://127.0.0.1:8000/form-action?header=true&policy=form-action 'none'

    """

    params = {}
    params['meta'] = request.args.get('meta')
    params['allow'] = request.args.get('allow')
    params['header'] = request.args.get('header')
    params['policy'] = request.args.get('policy')
    params['method'] = request.args.get('method')

    return request_handler('form-action.html', params)


@app.route('/font-src')
def font_src():
    """
    Test URI for font-src directive
    """
    params = {}
    params['meta'] = request.args.get('meta')
    params['allow'] = request.args.get('allow')
    params['header'] = request.args.get('header')
    params['policy'] = request.args.get('policy')

    return request_handler('font-src.html', params)


@app.route('/csp-header')
def csp_header_send():
    meta = {}
    policy = request.args.get('policy')
    if policy:
        meta['policy'] = policy
    response = make_response(render_template('csp-send.html', meta=meta))
    return response


@app.route('/alert/<state>')
def alert(state):
    params = {}
    params['state'] = state
    return request_handler('alert.html', params)


@app.route('/echo', methods=['GET', 'POST'])
def echo():
    params = {}
    response_headers = {}
    for k, v in request.headers.iteritems():
        response_headers[k] = v
    resp_headers = [(v, k) for k, v in response_headers.iteritems()]
    if request.method == 'POST':
        for param in request.form:
            params[param] = request.form.getlist(param)
    elif request.method == 'GET':
        for param in request.args:
            params[param] = request.args.getlist(param)
    response = make_response(render_template('echo.html', params=params,
                             headers=response_headers))
    return response


@app.route('/js/alert/<state>')
def alert_js(state):
    data = '''
    onconnect = function(e) {
    var port = e.ports[0];

    port.addEventListener('message', function(e) {
      var workerResult = 'Result: ' + (e.data);
      console.log('Result: ' + e.data);
      port.postMessage(workerResult);
    });

    port.start();
    }
    '''
    data = data + 'console.log("{0}")'.format(state)
    resp = Response(response=data, status=200, mimetype="text/javascript")
    return(resp)


@app.route('/events')
def events():
    data = 'event:ping\ndata: hello\n\n'
    resp = Response(response=data, status=200, mimetype="text/event-stream")
    return(resp)


@app.route('/test-header/<header>/<value>')
def test_header(header, value):
    """
    Returns 200 if header exists with given value sent with request
    and 404 if not
    """
    resp = Response(status=404)

    for k, v in request.headers.iteritems():
        if k.lower() == header.lower() and v.lower() == value.lower():
            resp = Response(status=200)
    return(resp)


@app.route('/jsonp')
def jsonp():
    response = make_response(render_template('jsonp.html'))
    return response


@app.route('/ping')
def ping():
    response = Response(response='pong', status=200)
    return response

if __name__ == "__main__":

    port = 8000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])

    print('Starting test server on port {0}'.format(port))
    app.debug = True
    # app.run('0.0.0.0', port=port)
    app.run(port=port)
