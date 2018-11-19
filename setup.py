from setuptools import find_packages, setup


with open("README.rst", "rt") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="approximate-date",
    version="0.1a1",
    url="https://github.com/funkyfuture/approximate-date",
    packages=find_packages(exclude=["*.tests", "*.tests.*"]),
    license="BSD",
    description="Python types and Django components to handle imprecise dates.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    keyworks="dates",
    author="Frank Sachsenheim",
    author_email="funkyfuture@riseup.net",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Database",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
