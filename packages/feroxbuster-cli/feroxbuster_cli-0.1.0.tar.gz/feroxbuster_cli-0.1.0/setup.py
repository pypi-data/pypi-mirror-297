from setuptools import setup, find_packages

setup(
    name="feroxbuster-cli",
    version="0.1.0",
    author="Adithya A N",
    description="A Python CLI tool to download and run Feroxbuster",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "feroxbuster-cli=feroxbuster_cli.cli:main",  # maps to cli.py's main function
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
