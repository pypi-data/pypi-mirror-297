from setuptools import setup, find_packages

setup(
    name='apiverve_usernamegenerator',
    version='1.1.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'setuptools'
    ],
    description='Username Generator is a simple tool for generating usernames. It returns a list of usernames based on the specified criteria.',
    author='APIVerve',
    author_email='hello@apiverve.com',
    url='https://apiverve.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
