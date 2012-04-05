from flask import Flask, render_template, redirect, url_for, request
import subprocess
app = Flask(__name__)
USERNAME = 'miniplex'


@app.route("/")
def index():
    """
    Index view that displays the ls output of the shares dir
    """
    out = subprocess.check_output('ls -l ~/shares/', shell=True)
    lines = out.split("\n")
    return render_template('shares.html', lines=lines, uname=USERNAME)

@app.route("/remount")
def remount():
    """
    Triggers a remount of the shares
    """
    out = "output:\n"
    out += subprocess.check_output(['./remount.sh', USERNAME, '&'], stderr=subprocess.STDOUT)
    return render_template('shares.html', output=out)

@app.route("/kill")
def kill():
    """
    Kills a pid 
    """
    pid = request.args.get('pid')
    subprocess.call(["kill", pid])
    return redirect(url_for('procs',p=pid))

@app.route("/procs")
def procs():
    """
    Displays the output from ps -ef
    -p filters the output 
    """
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
        try:
            output[h] = vals[v]
        except IndexError:
            pass

    return output


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
