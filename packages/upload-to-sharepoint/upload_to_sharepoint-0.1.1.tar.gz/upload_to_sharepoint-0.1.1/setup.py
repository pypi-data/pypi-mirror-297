from setuptools import setup, find_packages

setup(
    name='upload_to_sharepoint',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'office365-rest-python-client',  # Add any other dependencies here
        'keyring'
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A library to upload files to SharePoint.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://your-repository-url-or-pypi-url',  # Optional
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
