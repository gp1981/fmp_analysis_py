[flake8]
max-line-length = 120
exclude = .venv,venv,env

[pylint]
disable=
    C0111, # missing-docstring
    C0103  # invalid-name

[mypy]
ignore_missing_imports = True