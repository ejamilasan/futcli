from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="futcli",
    version="0.2.0",
    description="A command-line interface tool for fetching FC Ultimate Team data (futgg scraper)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Edwin Amilasan Jr.",
    author_email="ejamilasan@gmail.com",
    url="https://github.com/ejamilasan/futcli",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tabulate",
    ],
    entry_points={
        "console_scripts": [
            "futcli = futcli.futcli:futcli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
