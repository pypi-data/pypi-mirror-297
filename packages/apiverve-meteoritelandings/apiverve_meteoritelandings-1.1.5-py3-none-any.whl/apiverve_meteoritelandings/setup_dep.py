from setuptools import setup, find_packages

setup(
    name='apiverve_meteoritelandings',
    version='1.1.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'setuptools'
    ],
    description='Meteorites is a simple tool for getting meteorite data. It returns a list of meteorites that have fallen to Earth.',
    author='APIVerve',
    author_email='hello@apiverve.com',
    url='https://apiverve.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
