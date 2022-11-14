rm dist/* -f
python -m build
python -m twine upload  ./dist/* --verbose --repository-url https://upload.pypi.org/legacy/
