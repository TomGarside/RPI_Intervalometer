import flask
import timelapseWeb as tl

app = flask.Flask(__name__)

app.config["DEBUG"] = True

app.interval = 30
app.timel = tl.TimeLapse(app.interval, "/home/pi/Timelapse_Photos/")


@app.route('/', methods=['GET', 'POST'])
def home():

    if flask.request.method == 'POST':
        app.interval = int(flask.request.form['Interval'])
        app.timel.interval = app.interval
        app.timel.timelapse_on = True
        app.timel.start_timelapse()

    return flask.render_template('index.html', interval=app.interval, count=app.timel.count)


@app.route('/timelapseOff', methods=['POST'])
def off():
    app.timel.timelapse_on = False
    return flask.render_template('index.html', interval=app.interval, count=app.timel.count)


app.run()