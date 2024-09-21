from setuptools import setup, find_packages

setup(
    name="network_tool",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "scapy",
    ],
    author="Ayena Aurel",
    author_email="ayenaaurel15@gmail.com",
    description="Un outil simple pour effectuer des opérations réseau",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/votreusername/network_tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
