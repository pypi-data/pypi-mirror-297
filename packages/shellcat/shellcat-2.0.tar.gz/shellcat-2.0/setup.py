from setuptools import setup, find_packages

setup(
    name="shellcat",  # Project nam
    version="2.0",
    description="A tool to generate reverse shell payloads",
    author="serioton",
    url="https://pypi.org/project/shellcat/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
