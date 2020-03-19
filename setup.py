# encoding: utf-8
from setuptools import setup

def readme():
    """Import README for use as long_description."""
    with open("README.rst") as f:
        return f.read()

with open("VERSION.txt", "r") as f:
    version = f.read().strip()

setup(
    name="uc_scraper",
    version=version,
    description="A scraper of statistical data from uc.se, built on top of Statscraper.",
    long_description=readme(),
    url="https://github.com/jplusplus/uc_scraper",
    author="Jens Finnäs",
    author_email="jens.finnas@gmail.com",
    license="MIT",
    packages=["uc"],
    zip_safe=False,
    install_requires=[
        "statscraper",
        "requests",
        "beautifulsoup4",
    ],
    test_suite="nose.collector",
    tests_require=["nose"],
    include_package_data=True,
    download_url="https://github.com/jplusplus/uc_scraper/archive/%s.tar.gz"
                 % version,
)
