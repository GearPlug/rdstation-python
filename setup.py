import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="rdstation-python",
    version="0.2.0",
    description="API wrapper for RD Station written in Python",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/GearPlug/rdstation-python",
    author="Juan Carlos Rios",
    author_email="juankrios15@gmail.com",
    license="MIT",
    packages=["rdstation"],
    install_requires=[
        "requests",
    ],
    zip_safe=False,
)
