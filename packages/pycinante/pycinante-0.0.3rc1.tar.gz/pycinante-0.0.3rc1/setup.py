from setuptools import setup, find_packages
import pycinante
from pycinante import load_text

requirements = ["setuptools", "loguru"]

setup(
    name="pycinante",
    version=pycinante.__version__,
    python_requires=">=3.8",
    author="Chisheng Chen",
    author_email="chishengchen@126.com",
    url="https://github.com/gndlwch2w/pycinante",
    description="Python rocinante (Pycinante) for easily programming in Python.",
    long_description_content_type="text/markdown",
    long_description=load_text(pathname="README.md", encoding="utf-8"),
    license="MIT-0",
    packages=find_packages(),
    zip_safe=True,
    install_requires=requirements,
)
