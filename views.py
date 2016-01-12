from flask import Flask,render_template,request,redirect,url_for
from flask.ext.cache import Cache
from xlrd_extra_info import extra_info
from get_schedule import get_schedule
from AddDataToDataBase import add_data,db_to_dat

app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})


@app.route('/',methods = ['GET','POST'])
@cache.cached(timeout = 100)
def index():
    df,df0 = get_schedule()
    #request.form get values from HTML attribute 'name',then compare value with attr 'value'
    if request.form.get('go') == 'go':
        if request.form.get('spec') is not None:
            spec = request.form.get('spec')
            add_data(spec)
            db_to_dat()
            redirect(url_for('index'))

    return render_template('index.html',
                           day = df.to_html(classes = "table table-hover table-striped table-condensed table-responsive dayshift"),
                           night = df0.to_html(classes = "table table-hover table-striped table-condensed table-responsive nightshift"))

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
    app.run(debug = True,threaded = True)
