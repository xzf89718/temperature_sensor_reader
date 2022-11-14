rm dist/* -f
python -m build
pip install dist/*tar.gz --upgrade
