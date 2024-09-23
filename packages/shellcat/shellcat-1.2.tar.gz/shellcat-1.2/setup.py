from setuptools import setup, find_packages

setup(
    name="shellcat",
    version="1.2",
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
    entry_points={
        'console_scripts': [
            'shellcat=shellcat.shellcat:main',
        ],
    },
)
