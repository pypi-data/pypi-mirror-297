from setuptools import setup, find_packages

setup (
    name='public_ip_finder',
    author='gautham',
    version='0.1.0',
    description='A simple package to find the public IP address.',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
