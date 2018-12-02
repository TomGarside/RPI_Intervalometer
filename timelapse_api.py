import flask

app = flask.Flask(__name__)

app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return """
<h1>Raspberry Pi Intervalometer</h1>
<h3>Timelapse</h3>
<form>
    interval:
    <br>
    <input type="number"
         id="start"
         name="Interval"
         min="10" max="999" value="30">
    <br><br>
    <input type="submit" value="Start Timelapse">
</form>"""

app.run()