# Instructions on how to bundle and publish python package
# python setup.py sdist bdist_wheel - 
# This command will generate two distributions for us first is source and second is wheel
# Source distribution is usually python scripts
# Wheel Distribution Will contain binary information which are platform specific
# And these archives will have all the necessary files for installing and running the package.
from setuptools import setup, find_packages

with open(r"\pos-package\README.md", "r") as fh:
    description = fh.read()
    
setup(
    name = 'pos_tagging',
    version = '0.6.5',
    packages = find_packages(),
    install_requires = [
        # add dependencies here
        'langchain-google-genai>=2.0.0',
    ],
    entry_points = {
        'console_scripts': [
            'pos_tagging = pos_tagging:tagging'
        ]
    },
    long_description= description,
    long_description_content_type="text/markdown",
)
