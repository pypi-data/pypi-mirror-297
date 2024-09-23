from setuptools import setup
from setuptools.command.install import install

setup(
    name="pyprettifier",
    version="0.1.1",
    packages=["pyprettifier"],
    description="A simple Python utility to improve python output from simple string.",
    author="Sandra Gutierrez",
    author_email="help@pyprettifier.com",
    install_requires=[
        "requests"
    ],
    python_requires='>=3.6'
)
