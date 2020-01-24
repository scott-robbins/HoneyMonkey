import os
from flask import Flask, render_template, request

app = Flask(__name__)
app.config.from_pyfile('settings.py')
cache = {}
USERS = []


def swap(fname, destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n',''))
    if destroy:
        os.system('rm '+fname)
    return data


@app.route('/')
def hello_friend():
    client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    print client_ip
    return render_template('index.html')

###########################################################################################


if __name__ == '__main__':
    port = int(os.getenv('PORT', 80))
app.run(debug=True, host='0.0.0.0', port=port)
