from setuptools import setup, find_packages

setup (
    name = "Py_Simple_Select",
    version = "1.0.0",
	author = "Gloacking",
    description = "A lightweight ORM for SQLite with advanced and simplified select capabilities.",
    long_description = open ("README.md").read (),
    long_description_content_type = "text/markdown",
    url = "https://github.com/gloacking/Py_Simple_Select",
    packages = find_packages (),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.10',
    include_package_data = True,
)
