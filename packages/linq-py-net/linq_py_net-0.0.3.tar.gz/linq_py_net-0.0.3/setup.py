from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Extensions methods for the list, inspired in linq csharp'

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="linq_py_net", 
    version=VERSION,
    author="Wellington Junior",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements, 
    python_requires=">=3.5",
    
    keywords=['python', 'linq', 'csharp', 'c#'],
)