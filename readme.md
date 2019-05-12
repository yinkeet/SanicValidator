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