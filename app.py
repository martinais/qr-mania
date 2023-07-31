import os
import json
from flask import Flask, request, redirect
from google_auth_oauthlib.flow import Flow

from google_wrapper import return_book, book_available, borrow_book, get_owner, get_book_name, whoami

from google_wrapper import read

app = Flask(__name__)

PAGE_NAME = os.environ.get('X_PAGE_NAME')
SHEET_UID = os.environ.get('X_SHEET_UID')

if not PAGE_NAME:
    print("Missing environnement variable X_PAGE_NAME")
    exit(1)
if not SHEET_UID:
    print("Missing environnement variable X_SHEET_UID")
    exit(1)


SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/userinfo.profile']

flow = Flow.from_client_secrets_file(
    'credentials.json',
    scopes=SCOPES,
    redirect_uri='http://localhost:8000/run'
)


@ app.route('/run')
def add_book():
    bookId = request.args.get('state')
    authFlowCode = request.args.get('code')

    flow.fetch_token(code=authFlowCode)
    session = flow.authorized_session()

    conn = (session, flow, SHEET_UID, PAGE_NAME)
    name = whoami(conn)
    book_name = get_book_name(conn, bookId)

    if book_available(conn, bookId):
        borrow_book(conn, bookId, name)
        return f"Book '{book_name}' borrowed by {name}"
    else:
        owner = get_owner(conn, bookId)
        if owner == name:
            return_book(conn, bookId)
            return f"Book '{book_name}' returned by {name}"
        return f"Previous user {owner} did not return '{book_name}'"


@ app.route('/loan/<int:book_id>')
def loan(book_id):
    return redirect(flow.authorization_url(state=book_id)[0])


if __name__ == '__main__':
    app.run(port=8000)
