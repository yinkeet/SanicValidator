# SanicValidator

Sanic validator

## Packages

- [cerberus](http://docs.python-cerberus.org/en/stable/)
- [pylint](https://github.com/PyCQA/pylint)
- [pymongo](https://api.mongodb.com/python/current/)
- [Sanic](https://github.com/huge-success/sanic)

```bash
virtualenv venv && source venv/bin/activate && pip freeze | xargs pip uninstall -y && pip install cerberus pylint pymongo sanic && pip freeze > requirements.txt && deactivate
```

## FAQ

Q: Why are there so many warnings and error after cloning project?
A: The correct python interpreter and libraries that are specified in vscode are not found. Run these commands from project root folder to correct it.

```bash
virtualenv venv && source venv/bin/activate && pip install -r requirements.txt && deactivate
```