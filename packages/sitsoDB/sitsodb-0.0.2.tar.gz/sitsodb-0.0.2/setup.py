from setuptools import setup, find_packages
classifiers = [
    "Operating System :: Microsoft :: Windows :: Windows 11",
    "Operating System :: Android",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
]
with open("README.md") as description:
    message = description.read()
with open("CHANGELOG.txt") as changelog:
    change = changelog.read()


setup(
    name="sitsoDB",
    version="0.0.2",
    description="A DataBase Managament Sys, for simple terminal/ GUI projects.",
    long_description=message +'\n'+ change,
    long_description_content_type="text/markdown",
    author="Manasseh Kpormegbe",
    author_email="manassekpormegbe@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="database",
    packages=find_packages(),
    install_requires=["pandas","twine"],
    package_data={
        'sitsoDB':['seriesDB.csv', 'shelfDB.csv', 'standardDB.csv']
    }
)