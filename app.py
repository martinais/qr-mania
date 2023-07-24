from flask import Flask
import requests


response = requests.get("https://www.googleapis.com/oauth2/v1/userinfo?alt=json")


print(response)

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
