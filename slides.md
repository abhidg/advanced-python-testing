---
title: Advanced Python Testing
author: Abhishek Dasgupta
date: 3 September 2024
---

# Advanced Python Testing

Tired of waiting for network requests, writing millions of edge cases
and copy pasting outputs for testing? This walkthrough is for you.

Examples are in Python, but there are similar libraries available in
other languages.

https://github.com/abhidg/advanced-python-testing

# Mocking

- Test a code interface without requiring the underlying code to be run
- Useful when testing the actual interface is
  - time-consuming
  - requires network access
  - not possible in an automated way

# Mocking in Python

# Property based testing

- Checks that a particular property is satisfied by the code
- Normally one writes example based tests

```python
import pytest
def fahrenheit_to_celsius(temp): return 5 * (temp - 32) / 9

@pytest.mark.parametrize("f,c", [(212, 100), (32, 0)])
def test_fahrenheit_to_celsius(f,c):
    assert fahrenheit_to_celsius(f) == c
```

- Cons of example based testing is not being exhaustive enough
- What is `fahrenheit_to_celsius(NaN)`?

# Property based testing using `hypothesis`

- Allows one to express properties without providing examples
- Generates random examples and edge cases to test your code
- Number of examples, and search strategies can be customised

# Property based testing using `hypothesis`

```python
from hypothesis import given
from hypothesis.strategies import floats, integers
def divide(x, y): return x / y

@given(integers(), integers())
def test_divide(x, y): assert divide(x, y) < x
```

You can also find counterexamples - assert the inverse of a property
that you know to be true to be only in very few cases, and let
`hypothesis` search through the parameter space to find a failing case.

# Snapshot based testing

- Captures a _snapshot_ of a function or command and tests that it does not change
- Useful for testing outputs, data transformations
- Can be emulated manually (save output to disk, read and test that it is the same), but snapshot testing libraries make this easier

# Snapshot based testing using `syrupy`

- `syrupy` takes snapshots
- easy to use

# Walkthrough: finding the sun!

- **Problem**: Find a block of N hours when it will be sunny and clear, given a location.
- We will try to find a block of sun of two hours in Newcastle over the next week
- OpenMeteo has a nice free API
- Steps: fetch data, process and find the sun block
