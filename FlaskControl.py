from flask import Flask, render_template, redirect, url_for, request
import subprocess
app = Flask(__name__)


@app.route("/")
def index():
    out = subprocess.check_output('ls -l ~/shares/', shell=True)
    return render_template('output.html', output=out)

@app.route("/touch")
def touch():
    fname = request.args.get('f', '')
    if fname != '':
        subprocess.check_output(['touch', fname])
        return redirect(url_for('index'))
    else:
        return render_template('output.html',output="f = nothing")

@app.route("/remount")
def remount():
    out = "output:\n"
    #out += subprocess.check_output(['automount', '-vcu'], stderr=subprocess.STDOUT)
    out += subprocess.check_output(['./remount.sh'], stderr=subprocess.STDOUT)
    return render_template('output.html', output=out)

if __name__ == "__main__":
    app.debug = True
    app.run()