from setuptools import setup, find_packages

# Read the contents of the README file (optional)
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="papidweblogin",  # Replace with your package name
    version="0.1.0",  # Initial release version
    author="PR Reddy",
    author_email="dptrealtime@example.com",
    description="This package to validate users and passwords",
    long_description_content_type="text/markdown",  # Content type of long description
    url="https://bitbucket.org/dptrealtime/papid/src/main/"
)
