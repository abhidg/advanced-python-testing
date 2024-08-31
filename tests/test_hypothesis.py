"""
Property based testing
Testing module using hypothesis
"""
from hypothesis import given, reject, settings
from hypothesis.strategies import floats, integers

from sunblock import fahrenheit_to_celsius

# In property based testing, we encode assumptions or properties of the
# system that should always be true, regardless of parameter values a
# function takes. Often this reveals edge cases that are not handled in
# the code, which might not have been caught by example-based testing if
# our list of examples was not exhaustive enough.

# Here we check that no matter what temperature in degrees fahrenheit we
# are given, we never return a value less than absolute zero (0 K) which
# is equivalent to -273.15 degrees celsius.


@given(floats())
def test_fahrenheit_to_celsius(temp):
    try:
        assert fahrenheit_to_celsius(temp) > -273.15  # absolute zero
    except ValueError:
        reject()


# hypothesis can also be used to intentionally find counter-examples
# here we are trying to find an example where the numerical values of a
# temperature in celsius and fahrenheit are the same. This should fail
# as there is a counterexample (-40 F = -40 C) but hypothesis may not
# find it. Try increasing the max_examples setting to make hypothesis
# stumble upon the correct answer!
@given(integers(min_value=-450))
@settings(max_examples=5)
def test_fahrenheit_differs_from_celsius(temp):
    try:
        assert fahrenheit_to_celsius(temp) != temp
    except ValueError:
        reject()
