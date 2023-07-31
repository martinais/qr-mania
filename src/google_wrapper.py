import os
from datetime import date
from googleapiclient.discovery import build

BORROWED_LABEL = os.environ.get('X_BORROWED_LABEL')
AVAILABLE_LABEL = os.environ.get('X_AVAILABLE_LABEL')

BOOK_NAME_COL = os.environ.get('X_BOOK_NAME_COL')
BOOK_STATUS_COL = os.environ.get('X_BOOK_STATUS_COL')
USERNAME_COL = os.environ.get('X_USERNAME_COL')
DATE_COL = os.environ.get('X_DATE_COL')


if not BORROWED_LABEL:
    print("Missing environnement variable X_BORROWED_LABEL")
    exit(1)
if not AVAILABLE_LABEL:
    print("Missing environnement variable X_AVAILABLE_LABEL")
    exit(1)

if not BOOK_NAME_COL:
    print("Missing environnement variable X_BOOK_NAME_COL")
    exit(1)
if not BOOK_STATUS_COL:
    print("Missing environnement variable X_BOOK_STATUS_COL")
    exit(1)
if not USERNAME_COL:
    print("Missing environnement variable X_USERNAME_COL")
    exit(1)
if not DATE_COL:
    print("Missing environnement variable X_DATE_COL")
    exit(1)


def build_range(page, col, row):
    return f"{page}!{col}{row}:{col}{row}"


def read(conn, col, row):
    session, _, sheet, page = conn
    domain = 'sheets.googleapis.com'
    path = f'/v4/spreadsheets/{sheet}/values/{build_range(page, col, row)}'
    url = f'https://{domain}/{path}'
    response = session.get(f'https://{domain}/{path}')

    if response.status_code != 200:
        # TODO : raise ??
        return response.json()
    return response.json().get('values')[0][0]


def write(conn, col, row, content):
    _, flow, sheet, page = conn
    service = build(
        'sheets', 'v4', credentials=flow.credentials
    ).spreadsheets()
    return service.values().update(
        spreadsheetId=sheet,
        range=build_range(page, col, row),
        valueInputOption='RAW',
        body=content
    ).execute()


def get_owner(conn, book_id):
    return read(conn, USERNAME_COL, book_id)


def get_book_name(conn, book_id):
    return read(conn, BOOK_NAME_COL, book_id)


def whoami(conn):
    session, _, _, _ = conn
    response = session.get('https://www.googleapis.com/userinfo/v2/me')

    if response.status_code != 200:
        return response.json()
    else:
        return response.json().get('name')


def return_book(conn, book_id):
    write(conn, BOOK_STATUS_COL, book_id, {"values": [[AVAILABLE_LABEL]]})
    write(conn, USERNAME_COL, book_id, {"values": [['']]})
    write(conn, DATE_COL, book_id, {"values": [['']]})


def book_available(conn, book_id):
    print("here")
    return read(conn, BOOK_STATUS_COL, book_id) == AVAILABLE_LABEL


def borrow_book(conn, book_id, user):
    d = date.today().strftime("%d/%m/%Y")
    write(conn, BOOK_STATUS_COL, book_id, {"values": [[BORROWED_LABEL]]})
    write(conn, USERNAME_COL, book_id, {"values": [[user]]})
    write(conn, DATE_COL, book_id, {"values": [[d]]})
