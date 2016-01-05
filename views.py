from flask import Flask,render_template
from xlrd_extra_info import extra_info
from get_schedule import get_schedule

app = Flask(__name__)

@app.route('/')
def index():
    df = get_schedule()
    return render_template('index.html',schedule = df.to_html(classes = "table table-hover table-striped"))

@app.route('/api/<int:SPEC>')
def api(SPEC):
    data = extra_info(SPEC)
    return render_template('api.html',data = data)

if __name__ == '__main__':
    # from tornado.wsgi import WSGIContainer
    # from tornado.httpserver import HTTPServer
    # from tornado.ioloop import IOLoop

    # http_server = HTTPServer(WSGIContainer(app))
    # http_server.listen(5000)
    # IOLoop.instance().start()

    app.run(host = '0.0.0.0',debug = True,threaded = True)