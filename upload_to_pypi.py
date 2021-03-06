#!/usr/bin/env python3
from subprocess import call

with open("VERSION.txt", "r") as f:
    v = f.read().strip()

call(["python3", "setup.py", "sdist", "bdist_wheel"])
call(["python3", "-m", "twine", "upload", "dist/uc_scraper-{}*".format(v)])
