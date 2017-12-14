from setuptools import setup, find_packages


setup(
    name = "geonode-elasticsearch-app",
    version = "0.1",
    author = "tbrundage",
    author_email = "tbrundage@boundlessgeo.com",
    description = "Elasticsearch app for indexing GeoNode models via elasticsearch-dsl",
    long_description = open("README.md").read(),
    license = "GPLv2",
    url = "https://github.com/boundlessgeo/geonode-elasticsearch",
    download_url= "https://github.com/boundlessgeo/geonode-elasticsearch/archive/0.1.tar.gz",
    packages = find_packages(),
    classifiers = [
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
