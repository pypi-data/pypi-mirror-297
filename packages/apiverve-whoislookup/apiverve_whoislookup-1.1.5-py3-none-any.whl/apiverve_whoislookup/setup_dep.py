from setuptools import setup, find_packages

setup(
    name='apiverve_whoislookup',
    version='1.1.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'setuptools'
    ],
    description='Whois Lookup is a simple tool for checking the registration of a domain name. It returns the name and contact information of the domain owner, the domain registrar, and more.',
    author='APIVerve',
    author_email='hello@apiverve.com',
    url='https://apiverve.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
