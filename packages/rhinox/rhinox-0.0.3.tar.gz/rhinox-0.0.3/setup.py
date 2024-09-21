from pathlib import Path

from setuptools import find_packages, setup

setup(
    name="rhinox",
    version="0.0.3",
    author="Alejo Prieto Dávalos",
    author_email="alejoprietodavalos@gmail.com",
    packages=find_packages(),
    description="http://api.rhinox.io/api/documentation",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/rhinox/",
    project_urls={
        "Source": "https://github.com/AlejoPrietoDavalos/rhinox/"
    },
    python_requires=">=3.11",
    install_requires=[
        "requests>=2.32",
        "pydantic>=2.8",
    ],
    include_package_data=True
)
