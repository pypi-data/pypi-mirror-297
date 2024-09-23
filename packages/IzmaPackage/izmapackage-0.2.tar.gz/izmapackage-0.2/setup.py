from setuptools import setup, find_packages

setup(
    name='IzmaPackage',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        # Add dependencies here
        # e.g. 'numpy>=1.11.1'
    ],
    entry_points={
        "console_scripts": [
            "izma-hello = izmahello:hello",
        ],
    },
)
