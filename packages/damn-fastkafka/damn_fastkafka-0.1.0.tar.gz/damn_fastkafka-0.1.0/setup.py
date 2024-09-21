from setuptools import find_packages, setup

def readme():
    with open("README.md", "r") as f:
        return f.read()

setup(
    name="damn_fastkafka",
    version="0.1.0",
    author="mniyazkhanov@gmail.com",
    author_email="mniyazkhanov@gmail.com",
    description="This is the simplest module for quick work with Kafka.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/nmModi/damn_fastkafka",
    packages=find_packages(),
    install_requires=[
        "aiokafka>=0.7.2",
        "pydantic>=1.8",
        "aiologger>=0.6.0",
    ],
    extras_require={},
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="kafka fastapi",
    project_urls={
        "Source": "https://gitlab.com/nmModi/damn_fastkafka",
    },
    python_requires=">=3.8",
)
