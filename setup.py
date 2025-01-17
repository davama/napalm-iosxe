"""setup.py file."""

import uuid

from setuptools import setup, find_packages
from pip._internal.req import parse_requirements

__author__ = 'Nick Ethier <nethier@jive.com>'

install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())
reqs = [str(ir.requirement) for ir in install_reqs]

setup(
    name="napalm-iosxe",
    version="0.1.0",
    packages=find_packages(),
    author="Nick Ethier",
    author_email="nethier@jive.com",
    description="Network Automation and Programmability Abstraction Layer with Multivendor support",
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    url="https://github.com/napalm-automation/napalm-iosxe",
    include_package_data=True,
    install_requires=reqs,
)
