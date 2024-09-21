ruff check --select I --fix
ruff check --fix
ruff format

mypy \
 --ignore-missing-imports \
 --follow-imports=skip \
 --strict-optional \
 .