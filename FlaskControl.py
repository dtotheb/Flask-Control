from flask import Flask, render_template, redirect, url_for, request
import subprocess
app = Flask(__name__)
USERNAME = 'miniplex'


@app.route("/")
def index():
    out = subprocess.check_output('ls -l ~/shares/', shell=True)
    lines = out.split("\n")
    return render_template('output.html', lines=lines, uname=USERNAME)

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
    out += subprocess.check_output(['./remount.sh', USERNAME, '&'], stderr=subprocess.STDOUT)
    return render_template('output.html', output=out)

@app.route("/procs")
def procs():
    pname = request.args.get('p', '')
    procs = []

    out = subprocess.check_output(['ps -ef'], shell=True)
    lines = out.split("\n")
    headers = lines[0].split()


    for l in lines[1:]:
        if pname != '' and pname in l:
            procs.append(splitproc(l,headers))
        elif pname == '':
            procs.append(splitproc(l,headers))

    

    return render_template('procs.html', procs=procs, headers=headers)


def splitproc(input, headers):
    """
    Takes a line of output from ps & column headers
    Returns a dict using the headers as keys
    """
    vals = input.split(None,len(headers)-1)
    output = {}

    for v,h in enumerate(headers):
        output[h] = vals[v]

    return output


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
