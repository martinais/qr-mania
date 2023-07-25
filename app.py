import json

from flask import Flask, request, redirect, jsonify
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
    'credentials.json',
    scopes=SCOPES,
    redirect_uri='http://localhost:8000/run'
)


@app.route('/run')
def add_book():
    print('HERE')
    flow.fetch_token(code=request.args.get('code'))
    session = flow.authorized_session()
    print(session)
    bookId = request.args.get('state')
    print(bookId)

    name = session.get('https://www.googleapis.com/userinfo/v2/me').json()['name']

    spreadsheetId = '1VzZQVC9d68j9YyXwDK3_7GC1OedZPV9HTW6PbXgzGxU'  # TODO to parmetrize
    range = 'Library!G' + bookId + ':I' + bookId  # TODO improve the way to write in a specific area

    bookState = \
    session.get(f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{range}').json()['values'][0]
    print(bookState)

    if bookState[0] == 'Emprumté' and bookState[1] != name:
        print('1')
        return f'The previous user {name} has not correctly return the book'
    elif bookState[0] == 'Emprumté' and bookState[1] == name:
        print('2')
        body = jsonify({"values" :"[['Disponible', '', '']]"})
        print(body.json)
        return session.put('https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{range}',
                        #data={"values":[["Disponible","",""]]},
                        #data = {
                        #      "range": range,
                        #      "majorDimension": 'ROWS',
                        #      "values": [["Disponible","",""]]
                        #},
                        data = body.json,
                        params =
                       {'valueInputOption': 'RAW'}
                    ).json()
    elif bookState[0] == 'Disponible':
        print('3')
        return session.put('https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{range}').json()
        # return f"I'm {name} and I borrowed {bookId}"


@app.route('/loan/<int:book_id>')
def loan(book_id):
    return redirect(flow.authorization_url(state=book_id)[0])


if __name__ == '__main__':
    app.run(port=8000)
