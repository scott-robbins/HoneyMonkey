import os
from flask import Flask, render_template

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

# def get_page(dir, file):
#     filename = (file)
#
#     if filename in cache:
#         return cache[filename]
#
#     path = os.path.abspath(os.path.join(os.path.dirname(__file__), dir,filename))
#     try:
#         file_contents = open(path, encoding='utf-8').read()
#     except:
#         return None
#
#     data, text = file_contents.split('---\n', 1)
#     page = yaml.load(data)
#     page['content'] = Markup(markdown.markdown(text))
#     page['path'] = file
#
#     cache[filename] = page
#     return page
# @app.route('/')
# def login():
#     return render_template('sample.html')
#
#
# @app.route('/login')
# def flask_captive():
#     return render_template('login.html')


@app.route('/')
def hello_friend():
    cmd = "GET https://ipinfo.io/$(GET 'https://api.ipify.org?format=json' | jq -r .'ip')"
    os.system(cmd + ' >> user.txt')
    os.system('echo $(' + cmd + ")")
    data = ''
    for line in swap('user.txt', True):
        data += line
    print 'CLICKED BY ' + data
    return render_template('index.html')

###########################################################################################


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
app.run(debug=True, host='0.0.0.0', port=port)
