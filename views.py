from flask import Flask,render_template,request,redirect,url_for,session,abort
from xlrd_extra_info import extra_info
from get_schedule import get_schedule
from AddDataToDataBase import add_data_VMI,db_to_dat,add_data_MAXX
from os import urandom
import datetime
import pytz

app = Flask(__name__)
app.secret_key = 'UITJMNAGNAUIGKL'

@app.before_request
def csrf_protect():
    if request.method == 'POST':
        token = session.pop('_csrf_token',None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = urandom(15).encode('hex')
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

@app.before_request
def conn_db():
    pass

@app.route('/index',methods = ['GET','POST'])
@app.route('/',methods = ['GET','POST'])
def index():
    df,df0 = get_schedule()
    print df,df0
    print df.SPEC
    day = df.to_html(classes = "dayshift table-hover")
    night = df0.to_html(classes = "nightshift table-hover")
    tz = pytz.timezone('Asia/Shanghai')
    time = format(datetime.datetime.now(tz),'')
    #request.form get values from HTML attribute 'name',then compare value with attr 'value'
    if request.form.get('go') == 'go':
        if request.form.get('spec') is not None:
            session['spec'] = request.form.get('spec')
            add_data_VMI(session.get('spec'))
            add_data_MAXX(session.get('spec'))
            db_to_dat()
            return redirect(url_for('index'))
    return render_template('index.html',day = day,night = night,time = time)

@app.route('/api/<int:SPEC>')
def api(SPEC):
    data = extra_info(SPEC)
    return render_template('api.html',data = data)

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'),404
#
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'),500

if __name__ == '__main__':
    # from tornado.wsgi import WSGIContainer
    # from tornado.httpserver import HTTPServer
    # from tornado.ioloop import IOLoop
    #
    # http_server = HTTPServer(WSGIContainer(app))
    # http_server.listen(5000)
    # IOLoop.instance().start()
    app.run(threaded = True,host='0.0.0.0')
