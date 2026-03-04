"""Reset config cache between tests."""
from orb.utils import config

def pytest_runtest_setup(item):
    config.reset()
