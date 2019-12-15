import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as setuptools_test

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md")) as f:
    README = f.read()


class test(setuptools_test):
    def run_tests(self):
        import pytest

        sys.exit(pytest.main([]))


setup(
    name="dateorro",
    version="0.0.2",
    description="Working/calendar date/datetime calculations",
    python_requires=">=2.7",
    long_description=README,
    packages=find_packages(),
    tests_require=["pytest"],
    cmdclass={"test": test},
)
