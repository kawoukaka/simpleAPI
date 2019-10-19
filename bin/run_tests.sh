PY_PACKAGE="api_server"

flake8 --max-line-length=130 \
    --exclude=".git, __pycache__" \
    "${PY_PACKAGE}"

coverage run --omit=tests -m unittest discover
coverage html
