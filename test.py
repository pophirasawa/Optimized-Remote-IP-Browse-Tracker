from flask import Flask ,request

app = Flask(__name__)


@app.route('/')
def hello_world():
    print(request.form)
    return request.form

if __name__ == '__main__':
    app.run(host='localhost',port=1234)