# Advanced Python Testing

Accompanying repository for the RSECon24 talk "Advanced Python Testing -
mocking, property based testing, snapshot testing"

[Link to slides](https://github.com/abhidg/advanced-python-testing/releases/download/v1.0/RSECon24_Advanced_Python_Testing.pdf)

## Setup

Setup requires Python 3 (>=3.10)

```shell
git clone https://github.com/abhidg/advanced-python-testing && cd advanced-python-testing
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

To run the tests:

```shell
python3 -m pytest -v
```

You can also run test files individually:

```shell
python3 -m pytest tests/<file> -v
```

## Further reading

### Mocking

- Standard library has extensive documentation:
  https://docs.python.org/3/library/unittest.mock-examples.html
- Specialised libraries [moto](https://docs.getmoto.org/en/latest/)
  (AWS),
  [requests-mock](https://requests-mock.readthedocs.io/en/latest/),
  [freezegun](https://pypi.org/project/freezegun/) (datetime mocking)
- Mocks can automatically match specs, see
  [`autospec`](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.create_autospec)

### Property-based testing

- The `hypothesis` site has introductory articles:
  https://hypothesis.works/articles/getting-started-with-hypothesis/
- Extensions to `hypothesis`:
  [`schemathesis`](https://schemathesis.readthedocs.io/en/stable/) for
  API testing,
  [`hypothesis-jsonschema`](https://github.com/python-jsonschema/hypothesis-jsonschema)
  for generating JSON complying with a JSON Schema.
