from setuptools import setup, find_packages

setup(
    name="smartscout-api",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=1.8.0",
    ],
    author="Brian Weisberg",
    author_email="profs-brownie.0g@icloud.com",
    description="A Python client for the SmartScout API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/weisberg/smartscout-api-python",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)