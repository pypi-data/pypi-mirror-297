from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="prettyprintplus",
    version="0.1.1",
    author="Hridesh",
    keywords="prettyprintplus print table docs pprint dataset beautify",
    author_email="hridesh.khandal@gmail.com",
    description="A Python package for beautifying terminal output and tables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hridesh-net/prettyprintplus.git",
    project_urls={
        "Bug Tracker": "https://github.com/hridesh-net/prettyprintplus/projects?query=is%3Aopen",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
)