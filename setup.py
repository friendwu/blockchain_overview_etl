#!/usr/bin/env python

# setup.py
import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="overview-etl",
    version="1.0",
    description="ETL project for blockchain overview",
    long_description=read("README.md") if os.path.isfile("README.md") else "",
    license="MIT",
    packages=find_packages(exclude=["schemas", "tests", "venv"]),
    install_requires=[
        "aenum",
        "boto3",
        "click",
        "clickhouse_connect",
        "kafka",
        "pandas",
        "protobuf",
        "requests",
        "selenium",
        "selenium_stealth",
        "setuptools",
        "six",
        "SQLAlchemy",
        "timeout_decorator",
        "webdriver_manager",
        "psycopg2-binary",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "overviewetl=overviewetl.cli:cli",
        ],
    },
)
