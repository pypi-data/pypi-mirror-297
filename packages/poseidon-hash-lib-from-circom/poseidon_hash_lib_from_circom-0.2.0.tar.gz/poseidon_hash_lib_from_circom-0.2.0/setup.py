from setuptools import setup, find_packages

setup(
    name="poseidon-hash-lib-from-circom",
    version="0.2.0",
    author="erdognishe",
    author_email="khotyanmisha@gmail.com",
    description="Poseidon Hash Library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/erdoganishe/python3-poseidon-hash-lib",  # Add your repo link
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
    ],
)
