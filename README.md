# qr-mania

## Usage

### Dev

Building the project

```bash
podman build --target dev --tag qrmania .
podman run \
  --publish 8000:8000 \
  --env X_PAGE_NAME='...' \
  --env X_SHEET_UID='...' \
  --env X_BORROWED_LABEL='...' \
  --env X_AVAILABLE_LABEL='...' \
  --env X_BOOK_NAME_COL='...' \
  --env X_BOOK_STATUS_COL='...' \
  --env X_USERNAME_COL='...' \
  --env X_DATE_COL='...' \
  qrmania
```

### Prod

```bash
podman build --target prod --tag qrmania .
podman run \
  --publish 8000:80 \
  --env X_PAGE_NAME='...' \
  --env X_SHEET_UID='...' \
  --env X_BORROWED_LABEL='...' \
  --env X_AVAILABLE_LABEL='...' \
  --env X_BOOK_NAME_COL='...' \
  --env X_BOOK_STATUS_COL='...' \
  --env X_USERNAME_COL='...' \
  --env X_DATE_COL='...' \
  qrmania
```
