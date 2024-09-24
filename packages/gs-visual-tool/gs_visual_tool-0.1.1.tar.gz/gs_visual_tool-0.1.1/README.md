## init step

- python -m venv .venv

- source .venv/bin/activate

- pip install -e .

## example

- python example/app.py

## Deploy

```bash
pip install build
python -m build
twine upload dist/*
```
