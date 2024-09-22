from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="stealthy_requests",
    version="0.2.0",
    author="DEvin",
    author_email="firi8228@gmail.com",
    description="A stealthy requests library using Selenium for bot detection bypass",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "selenium",
        "undetected-chromedriver",
        "fake-useragent",
    ],
)