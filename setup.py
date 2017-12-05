#!/usr/bin/env python3

from setuptools import setup

setup(
    name = "radicale_auth_seafile",
    version = "0.1.2",
    author = "Klemens Schölhorn",
    author_email = "klemens@schoelhorn.eu",
    description = (" Authenticate Radicale 2 requests against Seafile "),
    license = "GPLv3",
    keywords = "radicale seafile auth",
    url = "https://github.com/klemens/radicale-auth-seafile",
    packages = ["radicale_auth_seafile"],
    install_requires = [
        "passlib>=1.7.0",
        "psycopg2",
    ],
)
