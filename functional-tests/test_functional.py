"""
Functional tests for the Simple Calculator web app.

Unlike the unit tests (tests/test_calc.py) which test the safe_divide function in isolation,
these functional tests exercise the Flask application end-to-end using Flask's built-in
**test client** -- driving real HTTP requests against the app in-process (no browser, no
deployment). They run in the CI pipeline and their results appear in the pipeline's Tests tab.
"""
import pytest
from python_calc import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_homepage_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Simple Calculator" in resp.data


def test_addition(client):
    resp = client.post("/", data={"a": "4", "b": "5", "op": "+"})
    assert resp.status_code == 200
    assert b"Result" in resp.data
    assert b"9" in resp.data


def test_subtraction(client):
    resp = client.post("/", data={"a": "10", "b": "3", "op": "-"})
    assert b"Result" in resp.data
    assert b"7" in resp.data


def test_division_by_zero_shows_error(client):
    resp = client.post("/", data={"a": "10", "b": "0", "op": "/"})
    assert b"Error" in resp.data
    assert b"Division by zero is not allowed" in resp.data
