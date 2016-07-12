
# (from https://blog.pythonanywhere.com/121/)
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy  import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="omer",
    password="forecast123",
    hostname="omer.mysql.pythonanywhere-services.com",
    databasename="omer$default",
)
#SQLALCHEMY_DATABASE_URI = "sqlite:////home/omer/WeatherForecast.db"

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
# connection timeouts: Opening a connection from your website code to a MySQL server takes a small amount of time.
# If you opened one for every hit on your website, it would be slightly slower. If your site was really busy, the
# aggregate of all of the small amounts of time opening connections could add up to quite a slowdown. To avoid this,
# SQLAlchemy operates a "connection pool". It keeps a set of connections to the database, and re-uses them. When you
# want a connection, it gives you one from the pool, creating a new one if the pool is empty, and when you're done
# with it, the connection is returned to the pool for future reuse. However, in order to stop people from hogging
# database connections, MySQL servers close unused connections after a particular amount of time. On PythonAnywhere,
# this timeout is set to 300 seconds. If your site is busy and your connections are always busy, this doesn't matter.
# But if it's not, a connection in the pool might be closed by the server because it wasn't being used. The
# SQLALCHEMY_POOL_RECYCLE variable is set to 299 to tell SQLAlchemy that it should throw away connections that haven't
# been used for 299 seconds, so that it doesn't give them to you and cause your code to crash because it's trying to
# use a connection that has already been closed by the server.
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

db = SQLAlchemy(app)

#class Comment(db.Model):
#
#    __tablename__ = "comments"
#
#    id = db.Column(db.Integer, primary_key=True)
#    content = db.Column(db.String(4096))

#@app.route('/')
#def hello_world():
#    return 'Hello from Flask!'

#@app.route('/')
#def index():
#    return render_template("main_page.html")

#@app.route("/", methods=["GET", "POST"])
@app.route("/")
def index():
    from forecastSrc.forecast_db_interface import BbcTable, OwmTable, YrTable, VollTable
    if request.method == "GET":
        return render_template("main_page.html", bbcData=BbcTable.query.all(), owmData=OwmTable.query.all(), yrData=YrTable.query.all(), vollData=VollTable.query.all())

    #comments.append(request.form["contents"])
    #comment = Comment(content=request.form["contents"])
    #db.session.add(comment)
    #db.session.commit()
    return redirect(url_for('index'))
