from setuptools import setup, find_packages

setup(
    name='apiverve_recipes',
    version='1.1.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'setuptools'
    ],
    description='Recipes is a simple tool for getting recipe information. It returns information on various recipes.',
    author='APIVerve',
    author_email='hello@apiverve.com',
    url='https://apiverve.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
