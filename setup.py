from setuptools import setup, find_packages

try:
    LONG_DESCRIPTION = open('README.md', 'r').read()
except IOError:
    LONG_DESCRIPTION = "Elasticsearch app for indexing GeoNode models via elasticsearch-dsl"

setup(
    name = "geonode-elasticsearch-app",
    version = "0.1.4",
    author = "tbrundage",
    author_email = "tbrundage@boundlessgeo.com",
    description = "Elasticsearch app for indexing GeoNode models via elasticsearch-dsl",
    long_description = LONG_DESCRIPTION,
    license = "GPLv2",
    url = "https://github.com/boundlessgeo/geonode-elasticsearch",
    download_url= "https://github.com/boundlessgeo/geonode-elasticsearch/archive/0.1.4.tar.gz",
    packages = find_packages(),
    classifiers = [
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    install_requires=[
        "elasticsearch>=2.0.0,<3.0.0",
        "elasticsearch-dsl>=2.0.0,<3.0.0"
    ]
)
