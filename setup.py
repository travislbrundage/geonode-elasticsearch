from setuptools import setup, find_packages


setup(
    name = "geonode-elasticsearch-app",
    version = "0.1",
    author = "tbrundage",
    author_email = "tbrundage@boundlessgeo.com",
    description = "Elasticsearch app for indexing GeoNode models via elasticsearch-dsl",
    long_description = open("README.md").read(),
    license = "GPL",
    url = "https://github.com/travislbrundage/geonode-elasticsearch",
    packages = find_packages(),
    classifiers = [
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)