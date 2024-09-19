#!/usr/decentmesh/env python3

import os

from setuptools import setup, find_packages

# get key package details from decentmesh/__version__.py
about = {}  # type: ignore
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "decentnet", "__version__.py")) as f:
    exec(f.read(), about)

# load the README file and use it as the long_description for PyPI
with open("README.md", "r") as f:
    readme = f.read()

setup(
    name=about["__title__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.11,<4",
    install_requires=[
        "alembic==1.13.2",
        "aiosqlite==0.20.0",
        "aiohttp==3.10.5",
        "argon2-cffi==23.1.0",
        "argon2-cffi-bindings==21.2.0",
        "asn1crypto==1.5.1",
        "Brotli==1.1.0",
        "cffi==1.17.1",
        "click==8.1.7",
        "httpx==0.27.2",
        "hypercorn==0.17.3",
        "coincurve==20.0.0",
        "colorama==0.4.6",
        "pycryptodome==3.20.0",
        "cytoolz==0.12.3",
        "pynacl==1.5.0",
        "eth-hash==0.7.0",
        "eth-keys==0.5.1",
        "eth-typing==5.0.0",
        "eth-utils==5.0.0",
        "greenlet==3.1.0",
        "lz4==4.3.3",
        "Mako==1.3.5",
        "markdown-it-py==3.0.0",
        "MarkupSafe==2.1.5",
        "mdurl==0.1.2",
        "networkx==3.3",
        "pycparser==2.22",
        "Pygments==2.18.0",
        "pylzma==0.5.0",
        "rich==13.8.1",
        "setuptools==74.1.2",
        "six==1.16.0",
        "SQLAlchemy==2.0.34",
        "toolz==0.12.1",
        "httpx==0.27.2",
        "typing_extensions==4.12.2",
        "pymysql==1.1.1",
        "prometheus_client==0.20.0",
        "cbor2~=5.6.4",
        "netifaces==0.11.0",
        "qrcode==7.4.2",
        "sentry-sdk==2.14.0",
        "numpy==2.1.1",
    ],
    extras_require={
        "dev": ["black==22.*"],
    },
    license=about["__license__"],
    zip_safe=True,
    entry_points={
        "console_scripts": ["decentmesh=decentnet.main:main"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="Decentralized P2P Network",
)
