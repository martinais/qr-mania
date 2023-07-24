from flask import Flask, request, redirect
import requests
import os
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/userinfo.profile']

flow = Flow.from_client_secrets_file(
    'martinade.json',
    scopes=SCOPES,
    redirect_uri='http://localhost:5000/run'
)


@app.route('/run')
def add_book():
    flow.fetch_token(code=request.args.get('code'))
    session = flow.authorized_session()
    name = session.get(
        'https://www.googleapis.com/userinfo/v2/me').json()['name']
    return f"I'm {name} and I borrowed {request.args.get('state')}"


@app.route('/loan/<int:book_id>')
def loan(book_id):
    return redirect(flow.authorization_url(state=book_id)[0])


if __name__ == '__main__':
    app.run()
