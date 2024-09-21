# asynclcron
lightweight cron on asyncio, support python 3.7+. [croniter](https://pypi.org/project/croniter/) is used.

# example
[test schedule app](tests/run_lcron.py)

run test schedule
```bash
# in project root
python3 -m tests.run_lcron
```

# development
## setup dev env
```bash
# in vscode terminal:
python3 -m venv venv
```

```bash
## reopen vscode terminal, venv should show
pip install croniter
```

## unit test
```bash
## run test
python3 -m unittest
```

## packaging and publish
```
python3 -m build
python3 -m twine upload dist/*
```
