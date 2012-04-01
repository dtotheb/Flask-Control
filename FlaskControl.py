from flask import Flask, render_template
import subprocess
app = Flask(__name__)


@app.route("/")
def index():
    out = subprocess.check_output(['ls', '-la'])
    return render_template('output.html', output=out)

if __name__ == "__main__":
    app.debug = True
    app.run()