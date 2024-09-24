from setuptools import setup, find_packages

setup(
    name="vyper-client-py",
    version="0.1.5",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "requests>=2.25.1,<3",
        "websockets>=10.0,<11",
    ],
    author="Brice Lloyd",
    author_email="support@vyper.trade",
    description="A Python SDK for the Vyper API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Vyper-Terminal/vyper-client-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)