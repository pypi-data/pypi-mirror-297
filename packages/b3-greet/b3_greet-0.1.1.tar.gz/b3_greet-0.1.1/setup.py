"""Setup script for the b3_greet package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="b3_greet",
    version="0.1.1",
    author="Avery",
    author_email="avery@bluebirdback.com",
    description="A simple greeting library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BlueBirdBack/b3_greet",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
