PY_PACKAGE="server"

flask8 --max-line-length=130 \
    --exclude=".git, __pycache__" \
    "${PY_PACKAGE}"

coverage run --omit=tests */site-packages/* -m unittest discover
coverage html
