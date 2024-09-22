from setuptools import setup, find_packages

setup(
    name='apiverve_textlanguage',
    version='1.1.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'setuptools'
    ],
    description='Text Language is a simple tool for detecting the language of a text. It returns the language code.',
    author='APIVerve',
    author_email='hello@apiverve.com',
    url='https://apiverve.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
