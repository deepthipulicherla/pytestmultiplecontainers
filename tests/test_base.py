import pytest

from base import get_weather
from divadd import add, div
from dataprovider import prime


@pytest.fixture(scope="module")
def setupteardownclass():
    print("set up class")
    yield
    print("tear down class")


@pytest.fixture()
def setupteardown():
    print("setup")
    yield
    print("tear down")

@pytest.mark.order(2)
@pytest.mark.parametrize("actual,expected",[(21,"HOT"),(13,"COLD")])
def test_weather(actual,expected,setupteardownclass, setupteardown):
    assert get_weather(actual) == expected

@pytest.mark.order(3)
@pytest.mark.sanity
def test_add(setupteardownclass, setupteardown):
    assert add(2, 3) == 5

@pytest.mark.order(1)
@pytest.mark.regression
def test_div(setupteardownclass, setupteardown):
    with pytest.raises(ValueError, match="division by zero"):
        div(3, 0)

@pytest.mark.order(4)
@pytest.mark.parametrize("actual,expected",[(1,False),(2,True),(3,True),(4,False),(5,True),(6,False),(7,True),(8,False),(9,False)])
def test_prime(actual,expected,setupteardownclass, setupteardown):
    assert prime(actual) == expected
