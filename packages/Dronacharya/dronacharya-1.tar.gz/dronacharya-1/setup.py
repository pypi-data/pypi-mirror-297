from setuptools import setup, find_packages
import os

VERSION = '1'
DESCRIPTION = '''
Dronacharya: Ultimate Guru
'''

# Read the long description from the README file
with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

# Setting up
setup(
    name="Dronacharya",
    version=VERSION,
    author="Suraj Sharma",
    author_email="Surajsharma963472@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,  # Set the long description
    long_description_content_type="text/markdown",  # Specify that the long description is in Markdown format
    packages=find_packages(),
    install_requires=[
        'pathlib',
        'colorama',
        'edge_tts',
        'pygame',
        'groq'
    ],
    keywords=['Surya', 'Vaidya', 'Dronacharya', 'python tutorial', 'Suraj', 'Teacher', 'groq'],
)
