from setuptools import setup, find_packages
from os import path

working_dir = path.abspath(path.dirname(__file__))

with open(path.join(working_dir, "README.md"), "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="pyenvloadermeta",
    version="1.0.2",
    author="Praveen",
    author_email="pvnt20@gmail.com",
    description="A metaclass for automatically loading and converting environment variables.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Praveensenpai/pyenvloadermeta",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "python-dotenv>=1.0.1",
    ],
)
